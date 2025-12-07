# Python 3.13のベースイメージを使用
FROM python:3.13-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Node.jsをインストール（Claude CLIに必要）
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Claude CLIをグローバルにインストール
RUN npm install -g @anthropic-ai/claude-code

# 作業ディレクトリを設定
WORKDIR /app

# Poetryをインストール
RUN pip install --no-cache-dir poetry

# poetryの設定: 仮想環境を作成しない（コンテナ内では不要）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# 依存関係をインストール
RUN poetry install --no-root --no-interaction --no-ansi

# アプリケーションのコードをコピー
COPY . .

# デフォルトのコマンド（必要に応じて変更してください）
CMD ["python", "--version"]