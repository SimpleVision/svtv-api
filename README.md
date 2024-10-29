# svtv-api

> `jianshi-tv` 桌面客户端 `api` 接口服务，自行搭建 `m3u` 源转换及 `epg` 解析服务。

### 安装及使用说明

```bash
# 目前在 Python 3.12 环境下运行测试无问题，其它环境请自行测试
git clone https://github.com/simple-vision/svtv-api
cd svtv-api
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
# 启动 http 服务，指定端口 10000 （可修改为其它端口）
python3 app.py 10000
# m3u 直播频道信息接口：频道分类且支持多源的响应结果
http://localhost:10000/svtv/m3u-parser?url=https://ghp.ci/raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u
# 如果解析没有异常，会回显新的静态文件地址（按天缓存，避免目标 `m3u` 更新）
# 然后访问该静态地址即可，如
http://localhost:10000/static/20241028_3aa586d1511102767d7bc7d238d547d9.json
# epg 信息接口：默认使用 https://live.fanmingming.com/e.xml epg
http://localhost:10000/svtv/tv-guide?channel_id=CCTV1 
# 为了性能优化，channel_id 是完全匹配的，不支持模糊匹配
# 如 'CCTV综合', '中央一套', '中央一台' 等均重定向到 'CCTV1'
# 不同 epg 提供商的 channel_id 是不同的，有些是频道名（字符串形式），有些是自定义的频道id（数字形式）
# 如果 channel_id 完全命中，则会响应完整的 xml 格式节目单，请客户端自行解析处理
# epg 信息解析依赖于 xq 组件
# mac 下请使用 `brew install xq` 安装依赖，其它环境参考官网 ref: https://github.com/sibprogrammer/xq
# docker 镜像已内置 xq 组件
# 服务器推荐 `docker` 部署运行
docker run -p 10000:10000 registry.cn-hangzhou.aliyuncs.com/douyasi/svtv-api:latest
```

### 响应示例

直播频道信息接口响应结果如下（仅展示一个节点）：

```json
[
    {
        "category": "央视频道",
        "channels": [
            {
                "name": "CCTV-1 综合",
                "logo": "https://live.fanmingming.com/tv/CCTV1.png",
                "url": "http://[2409:8087:1a01:df::7005]:80/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226559/index.m3u8",
                "sources": [
                    {
                        "name": "IPV6 - 源1",
                        "url": "http://[2409:8087:1a01:df::7005]:80/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226559/index.m3u8"
                    },
                    {
                        "name": "IPV6 - 源2",
                        "url": "http://[2409:8087:5e00:24::1e]:6060/200000001898/460000089800010144/1.m3u8"
                    }
                ],
                "category": "央视频道",
                "tvg": {
                    "id": "CCTV1",
                    "name": "CCTV1"
                }
            }
        ]
    }
]
```

电子节目单信息接口响应结果如下：

```json
{
  "c": 200,
  "m": "√",
  "d": "<tv><programme channel=\"CCTV1\" start=\"20241029011500 +0800\" stop=\"20241029014300 +0800\">\n  <title lang=\"zh\">今日说法-2024-271</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029014300 +0800\" stop=\"20241029021200 +0800\">\n  <title lang=\"zh\">人与自然-2024-113</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029021200 +0800\" stop=\"20241029024200 +0800\">\n  <title lang=\"zh\">晚间新闻</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029024200 +0800\" stop=\"20241029024800 +0800\">\n  <title lang=\"zh\">山水间的家-主题曲</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029024800 +0800\" stop=\"20241029042300 +0800\">\n  <title lang=\"zh\">非遗里的中国（第二季）-10</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029042300 +0800\" stop=\"20241029042500 +0800\">\n  <title lang=\"zh\">泱泱中华-美丽湿地2</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029042500 +0800\" stop=\"20241029045600 +0800\">\n  <title lang=\"zh\">今日说法-2024-271</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029045600 +0800\" stop=\"20241029053000 +0800\">\n  <title lang=\"zh\">新闻联播</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029053000 +0800\" stop=\"20241029060000 +0800\">\n  <title lang=\"zh\">人与自然-2024-114</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029060000 +0800\" stop=\"20241029080000 +0800\">\n  <title lang=\"zh\">朝闻天下</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029080000 +0800\" stop=\"20241029100000 +0800\">\n  <title lang=\"zh\">新闻直播间</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029100000 +0800\" stop=\"20241029110000 +0800\">\n  <title lang=\"zh\">新闻直播间</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029110000 +0800\" stop=\"20241029115600 +0800\">\n  <title lang=\"zh\">人民警察第38集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029115600 +0800\" stop=\"20241029120000 +0800\">\n  <title lang=\"zh\">2024秘境之眼-291</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029120000 +0800\" stop=\"20241029123500 +0800\">\n  <title lang=\"zh\">新闻30分</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029123500 +0800\" stop=\"20241029130900 +0800\">\n  <title lang=\"zh\">今日说法-2024-272</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029130900 +0800\" stop=\"20241029135600 +0800\">\n  <title lang=\"zh\">特赦1959第15集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029135600 +0800\" stop=\"20241029144900 +0800\">\n  <title lang=\"zh\">特赦1959第16集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029144900 +0800\" stop=\"20241029153800 +0800\">\n  <title lang=\"zh\">特赦1959第17集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029153800 +0800\" stop=\"20241029162600 +0800\">\n  <title lang=\"zh\">特赦1959第18集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029162600 +0800\" stop=\"20241029172000 +0800\">\n  <title lang=\"zh\">特赦1959第19集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029172000 +0800\" stop=\"20241029175500 +0800\">\n  <title lang=\"zh\">第一动画乐园-2024-441</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029175500 +0800\" stop=\"20241029181900 +0800\">\n  <title lang=\"zh\">第一动画乐园-2024-442</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029181900 +0800\" stop=\"20241029184900 +0800\">\n  <title lang=\"zh\">文脉春秋-2024-5</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029184900 +0800\" stop=\"20241029190000 +0800\">\n  <title lang=\"zh\">2024秘境之眼-291</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029190000 +0800\" stop=\"20241029193900 +0800\">\n  <title lang=\"zh\">新闻联播</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029193900 +0800\" stop=\"20241029200100 +0800\">\n  <title lang=\"zh\">焦点访谈</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029200100 +0800\" stop=\"20241029200600 +0800\">\n  <title lang=\"zh\">前情提要-上甘岭-第22集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029200600 +0800\" stop=\"20241029205600 +0800\">\n  <title lang=\"zh\">上甘岭22/24</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029205600 +0800\" stop=\"20241029210000 +0800\">\n  <title lang=\"zh\">前情提要-上甘岭-第23集</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029210000 +0800\" stop=\"20241029214900 +0800\">\n  <title lang=\"zh\">上甘岭23/24</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029214900 +0800\" stop=\"20241029220000 +0800\">\n  <title lang=\"zh\">山水间的家-主题曲</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029220000 +0800\" stop=\"20241029223500 +0800\">\n  <title lang=\"zh\">晚间新闻</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029223500 +0800\" stop=\"20241029230300 +0800\">\n  <title lang=\"zh\">精彩一刻-三大战役5</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029230300 +0800\" stop=\"20241029233100 +0800\">\n  <title lang=\"zh\">精彩一刻-三大战役6</title>\n</programme>\n<programme channel=\"CCTV1\" start=\"20241029233100 +0800\" stop=\"20241029235900 +0800\">\n  <title lang=\"zh\">今日说法-2024-272</title>\n</programme>\n</tv>"
}
```

直接返回 `xml` 的节目单，需要前端自行处理，如根据当前时间解析出正在播放的电视节目。

### 参考资料

`GitHub` 上一些 `IPTV` 源，不保证最新且可用，请自行验证。

- [yuanzl77/IPTV](https://github.com/yuanzl77/IPTV)
- [suxuang/myIPTV](https://github.com/suxuang/myIPTV)
- [HerbertHe/iptv-sources](https://github.com/HerbertHe/iptv-sources)
- [fanmingming/live](https://github.com/fanmingming/live)
- [SPX372928/MyIPTV](https://github.com/SPX372928/MyIPTV)