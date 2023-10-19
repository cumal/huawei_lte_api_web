FROM python:3.10.12-alpine

LABEL org.opencontainers.image.source=https://github.com/cumal/huawei_lte_api_web

COPY requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir /front
COPY web.py /front/
WORKDIR /front
ENTRYPOINT ["python", "web.py"]
