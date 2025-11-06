FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Playwright base image already includes required system deps and browsers

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# Browsers are preinstalled in the Playwright base image; no extra install needed

# 复制应用代码
COPY app/ ./app/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
