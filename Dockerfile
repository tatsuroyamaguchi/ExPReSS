FROM python:3.11-slim

# 作業ディレクトリをコンテナ内で /app に設定
WORKDIR /app

# 必要ファイルをすべて /app にコピー
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY README.md ./README.md

CMD ["streamlit", "run", "app/ExPReSS.py", "--server.port=8503", "--server.address=0.0.0.0"]
