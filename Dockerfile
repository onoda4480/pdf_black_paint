# Python 3.13のベースイメージを使用
FROM python:3.13-slim

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