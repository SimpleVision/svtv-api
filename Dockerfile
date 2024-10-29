# FROM python:3.13-alpine
FROM registry.cn-hangzhou.aliyuncs.com/go-to-mirror/python:3.12-alpine

WORKDIR /app
COPY app.py .
COPY requirements.txt .
ADD tmp/xq_1.2.5_linux_amd64.tar.gz /tmp/
RUN chmod +x /tmp/xq && mv -f /tmp/xq /usr/local/bin/xq  \
    && mkdir static && mkdir download  \
    && echo 'bad request' > /app/static/index.html \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT [ "python", "/app/app.py", "10000" ]