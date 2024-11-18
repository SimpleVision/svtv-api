import json
import web
import hashlib
import requests
from m3u_parser import M3uParser
import time
import os
import xml.etree.ElementTree as EleTree
from urllib.parse import urlparse

def download_file(url, ext='.xml'):
    datetime_str = time.strftime('%Y%m%d%H', time.localtime(time.time()))
    hash_file_name = hashlib.md5((url + datetime_str).encode('utf-8')).hexdigest()
    file_path = './download/' + datetime_str + '_' + hash_file_name + ext
    re = os.path.exists(file_path)
    if re:
        return file_path
    else:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    return file_path

def get_hash_file(url):
    date_str = time.strftime('%Y%m%d', time.localtime(time.time()))
    hash_file_name = hashlib.md5((url + date_str).encode('utf-8')).hexdigest()
    out_file_name = '/' + date_str + '_' + hash_file_name + '.json'
    re = os.path.exists('./static' + out_file_name)
    return out_file_name, re

def write_to_file(url, res_data):
    out_file_name, re = get_hash_file(url)
    if re:
        return out_file_name
    else:
        data = json.dumps(res_data, indent=4)
        with open('./static' + out_file_name, mode='w', encoding='utf-8') as fp:
            fp.write(data)
        fp.close()
    return out_file_name

class Parser:

    def GET(self):
        # https://ghp.ci/raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u
        url = web.input().get('url')
        out_file, re = get_hash_file(url)
        if re:
            return json.dumps({
                'c': 200,
                'm': '√',
                'd': '/static' + out_file
            }, sort_keys=False)
        # rsp = requests.get(url)
        # content = rsp.text
        parser = M3uParser(timeout=5)
        # ref: https://github.com/pawanpaudel93/m3u-parser
        # Parse the m3u file

        # sometimes fetch web url maybe got error
        # so, just download it first
        local_m3u_file = download_file(url, '.m3u')
        parser.parse_m3u(local_m3u_file, schemes=['http', 'https'], check_live=False)
        items = parser.get_list()
        categories = dict()
        grouped_channels = dict()
        for item in items:
            category_hash_key = hashlib.md5(item['category'].encode('utf-8')).hexdigest()
            if category_hash_key not in categories:
                categories[category_hash_key] = {
                    'name': item['category'],
                    'channels': []
                }
            hash_key = hashlib.md5(item['name'].encode('utf-8')).hexdigest()
            if hash_key not in grouped_channels:
                grouped_channels[hash_key] = {
                    'name': item['name'],
                    'logo': item['logo'],
                    'url': item['url'],
                    'category': item['category'],
                    'sources': [],
                    'tvg': {
                        'id': item['tvg']['id'],
                        'name': item['tvg']['name'],
                    },
                }
            if hash_key in grouped_channels:
                grouped_channels[hash_key]['sources'].append({
                    'name': '',
                    'url': item['url'],
                })

        for channel_key in grouped_channels:
            category_hash_key = hashlib.md5(grouped_channels[channel_key]['category'].encode('utf-8')).hexdigest()
            categories[category_hash_key]['channels'].append(grouped_channels[channel_key])

        resp_data = []
        for category_key in categories:
            resp_data.append(categories[category_key])
        # 将解析之后的 data 保存为本地 json 文件，以加快性能
        out_file = write_to_file(url, resp_data)

        resp = {
            'c': 200,
            'm': '√',
            # 'data': resp_data
            'd': '/static' + out_file
        }
        return json.dumps(resp, sort_keys=False)

class Guide:
    def GET(self):
        # CCTV1
        # 为了性能优化，不支持模糊匹配（如 'CCTV综合', '中央一套', '中央一台' 等均重定向到 'CCTV1' ）
        channel_id = web.input().get('channel_id')
        # epg parser
        # 仅使用 fanmingming epg 接口
        epg_url = web.input().get('epg_url')
        if epg_url is None:
            epg_url = 'https://live.fanmingming.com/e.xml'
        # 每小时缓存一次，避免过时
        xml_file = download_file(epg_url)
        f = os.popen('cat ' + xml_file + ' | xq -x "//programme[@channel=\'' + channel_id + '\']" -n')
        # xml 结构，按道理需要进一步解析的，这里略去，由客户端解析吧
        resp = f.read()
        return json.dumps({
            'c': 200,
            'm': '√',
            'd': '<tv>' + resp + '</tv>'
        }, sort_keys=False)

if __name__ == "__main__":
    urls = (
        '/svtv/m3u-parser', 'Parser',
        '/svtv/tv-guide', 'Guide',
    )
    app = web.application(urls, globals())
    app.run()

