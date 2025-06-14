@echo off
chcp 65001 >nul
echo 🔧 Discord Roulette Bot セットアップスクリプト
echo.

REM スクリプトのディレクトリに移動
cd /d "%~dp0"

echo 📦 仮想環境を作成中...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ 仮想環境の作成に失敗しました。
    echo Pythonがインストールされているか確認してください。
    pause
    exit /b 1
)

echo ✅ 仮想環境が作成されました。

echo 📋 仮想環境を有効化中...
call venv\Scripts\activate.bat

echo 📦 依存関係をインストール中...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依存関係のインストールに失敗しました。
    pause
    exit /b 1
)

echo.
echo ✅ セットアップが完了しました！
echo.
echo 次の手順：
echo 1. Discord Developer Portal でボットを作成
echo 2. .env ファイルでトークンとクライアントIDを設定
echo 3. start_bot.bat を実行してボットを起動
echo.
echo 詳細な手順は README.md を参照してください。
echo.
pause
