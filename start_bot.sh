#!/bin/bash

# Discord Roulette Bot 起動スクリプト

echo "🎯 Discord Roulette Bot を起動しています..."
echo ""

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境の存在確認
if [ ! -d "venv" ]; then
    echo "❌ 仮想環境が見つかりません。セットアップを実行してください："
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# .envファイルの存在確認
if [ ! -f ".env" ]; then
    echo "❌ .envファイルが見つかりません。"
    echo "DISCORD_TOKENを設定してください。"
    exit 1
fi

# トークンの設定確認
if grep -q "your_bot_token_here" .env; then
    echo "❌ ボットトークンが設定されていません。"
    echo ".envファイルでDISCORD_TOKENを設定してください。"
    exit 1
fi

# クライアントIDの設定確認
if grep -q "your_application_id_here" .env; then
    echo "❌ クライアントIDが設定されていません。"
    echo ".envファイルでCLIENT_IDを設定してください。"
    exit 1
fi

# 仮想環境を有効化
source venv/bin/activate

# 必要なパッケージがインストールされているか確認
python -c "import discord; print(f'✅ discord.py v{discord.__version__} が利用可能です')" 2>/dev/null || {
    echo "❌ discord.pyがインストールされていません。"
    echo "pip install -r requirements.txt を実行してください。"
    exit 1
}

echo "🚀 ボットを起動中..."
echo ""

# ボットを起動
python roulette_bot.py
