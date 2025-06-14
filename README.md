di# Discord ルーレットボット

Pythonで作成されたDiscordのロシアンルーレットボットです。

## 機能

- 🎯 ロシアンルーレットゲーム（スラッシュコマンド対応）
- 👥 複数人対応（2-10人）
- 🎲 ランダムな順番とチャンバー
- 📊 美しいEmbedメッセージ
- ⚡ リアルタイムゲーム進行
- 🔧 直感的なスラッシュコマンドUI

## セットアップ

### 🛠️ 自動セットアップ（推奨）

**Windows:**
```cmd
setup.bat
```

**macOS/Linux:**
手動セットアップを使用してください。

### 📋 手動セットアップ

### 1. 仮想環境の作成と有効化

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. 依存関係のインストール

**macOS/Linux:**
```bash
pip install -r requirements.txt
```

**Windows:**
```cmd
pip install -r requirements.txt
```

### 3. Discordボットの作成

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. 「New Application」をクリック
3. アプリケーション名を入力
4. 「Bot」タブに移動
5. 「Add Bot」をクリック
6. トークンをコピー

### 4. 環境変数の設定

`.env`ファイルを編集し、必要な情報を設定：

```
# 必須: ボットトークン
DISCORD_TOKEN=your_actual_bot_token_here

# 必須: クライアント/アプリケーションID
CLIENT_ID=your_application_id_here

# オプション: テスト用ギルドID（開発時のみ）
GUILD_ID=your_guild_id_here
```

**📋 各IDの取得方法:**
- **トークン**: Bot タブ → Token
- **クライアントID**: General Information → Application ID  
- **ギルドID**: Discord設定 → 詳細設定 → 開発者モードを有効 → サーバー右クリック → IDをコピー

### 5. ボットの権限設定

Discord Developer Portalで以下の権限を有効にしてください：

**Bot Permissions:**
- Send Messages
- Use Slash Commands
- Read Message History
- Add Reactions
- Embed Links
- Use External Emojis

**Privileged Gateway Intents:**
- ✅ **不要**: このスラッシュコマンドボットでは特権インテントは必要ありません

### 6. サーバーに招待

**Discord Developer Portal での設定:**
1. OAuth2 → URL Generator に移動
2. **Scopes**: `bot` と `applications.commands` を選択
3. **Bot Permissions**: 上記の権限を選択
4. 生成されたURLでボットを招待

**または、以下のURLテンプレートを使用:**
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274878221312&scope=bot%20applications.commands
```
`YOUR_CLIENT_ID` を実際のクライアントIDに置き換えてください。

## 使用方法

### スラッシュコマンド

- `/roulette` - ゲーム開始（参加者を選択）
- `/stop` - ゲーム停止  
- `/rules` - ルール表示

### 使用例

スラッシュコマンド `/roulette` を使用し、参加者を選択してください。

```
/roulette player1:@Alice player2:@Bob player3:@Charlie
```

## ゲームルール

1. 6発のうち1発が実弾です
2. 参加者は順番に引き金を引きます
3. 実弾を引いたプレイヤーが負けです
4. 最後まで生き残ったプレイヤーが勝者です

## 実行

### 🚀 簡単起動（推奨）

**macOS/Linux:**
```bash
./start_bot.sh
```

**Windows:**
```cmd
start_bot.bat
```

### 🔧 手動起動

**macOS/Linux:**
```bash
# 仮想環境を有効化
source venv/bin/activate

# ボットを起動
python roulette_bot.py
```

**Windows:**
```cmd
# 仮想環境を有効化
venv\Scripts\activate

# ボットを起動
python roulette_bot.py
```

## 注意事項

- `.env`ファイルは絶対に公開しないでください
- ボットトークンとクライアントIDは秘密情報です
- 適切なチャンネルでのみ使用してください

## 開発・テストのヒント

### 🔧 開発時の高速同期
`.env`ファイルで`GUILD_ID`を設定すると、特定のサーバーのみにスラッシュコマンドが同期され、即座に反映されます。

### 🌍 本番環境
`GUILD_ID`を設定しない場合、グローバルに同期され、すべてのサーバーで使用可能になりますが、反映に最大1時間かかります。

## トラブルシューティング

### よくある問題

1. **「DISCORD_TOKENが設定されていません」エラー**
   - `.env`ファイルが正しく設定されているか確認
   - トークンが正しくコピーされているか確認

2. **ボットが反応しない**
   - 適切な権限が設定されているか確認
   - スラッシュコマンドの同期完了を待つ（最大1時間）

3. **「参加者を指定してください」エラー**
   - コマンドの形式が正しいか確認
   - ユーザーをメンションしているか確認

### Windows固有の問題

4. **「python は内部コマンドまたは外部コマンドではありません」エラー**
   - Pythonがインストールされているか確認
   - PATHが正しく設定されているか確認
   - Microsoft Store版Pythonの場合は `python` コマンドを使用

5. **文字化けが発生する場合**
   - バッチファイルの最初に `chcp 65001` が含まれていることを確認
   - コマンドプロンプトのフォントを変更（例：Consolas）
