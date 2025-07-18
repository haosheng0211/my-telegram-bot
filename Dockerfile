# 使用官方Python runtime作為父映像檔
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 複製requirements文件
COPY requirements.txt .

# 安裝Python依賴
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 創建非root用戶
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# 暴露端口
EXPOSE 8000



# 啟動命令
CMD ["python", "app.py"] 