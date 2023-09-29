FROM python:3-alpine

LABEL org.opencontainers.image.source=https://github.com/cumal/huawei_lte_api_web

RUN pip install nicegui==1.3.15 huawei_lte_api==1.7.3
RUN mkdir /front
COPY web.py /front/
WORKDIR /front
ENTRYPOINT ["python", "web.py"]
