FROM python:3-alpine

LABEL org.opencontainers.image.source=https://github.com/cumal/huawei_lte_api_web

# Install poetry and update pip/wheel
RUN pip install --upgrade pip nicegui huawei_lte_api

# Copy web page
COPY web.py /

# Entrypoint command
ENTRYPOINT ["python", "/web.py"]
