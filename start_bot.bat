@echo off
chcp 65001 >nul
echo 🎯 Discord Roulette Bot を起動しています...
echo.

REM スクリプトのディレクトリに移動
cd /d "%~dp0"

REM 仮想環境の存在確認
if not exist "venv" (
    echo ❌ 仮想環境が見つかりません。セットアップを実行してください：
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM .envファイルの存在確認
if not exist ".env" (
    echo ❌ .envファイルが見つかりません。
    echo DISCORD_TOKENを設定してください。
    pause
    exit /b 1
)

REM トークンの設定確認
findstr /c:"your_bot_token_here" .env >nul
if %errorlevel% equ 0 (
    echo ❌ ボットトークンが設定されていません。
    echo .envファイルでDISCORD_TOKENを設定してください。
    pause
    exit /b 1
)

REM クライアントIDの設定確認
findstr /c:"your_application_id_here" .env >nul
if %errorlevel% equ 0 (
    echo ❌ クライアントIDが設定されていません。
    echo .envファイルでCLIENT_IDを設定してください。
    pause
    exit /b 1
)

REM 仮想環境を有効化
call venv\Scripts\activate.bat

REM 必要なパッケージがインストールされているか確認
python -c "import discord; print(f'✅ discord.py v{discord.__version__} が利用可能です')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ discord.pyがインストールされていません。
    echo pip install -r requirements.txt を実行してください。
    pause
    exit /b 1
)

echo 🚀 ボットを起動中...
echo.

REM ボットを起動
python roulette_bot.py

REM エラーが発生した場合の処理
if %errorlevel% neq 0 (
    echo.
    echo ❌ ボットの起動中にエラーが発生しました。
    echo 上記のエラーメッセージを確認してください。
    pause
)
