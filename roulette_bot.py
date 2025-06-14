# ============================================
# Discord ロシアンルーレットボット
# ============================================
# Pythonでディスコードのボットを作成するために必要なライブラリを読み込み

# Discord.pyライブラリ - Discordのボットを作るためのメインライブラリ
import discord
from discord.ext import commands  # コマンド機能を使うため
from discord import app_commands  # スラッシュコマンド機能を使うため

# その他の必要なライブラリ
import random   # ランダムな数字や順番を生成するため
import asyncio  # 非同期処理（時間をかけて実行する処理）を行うため
import os       # 環境変数（設定情報）を読み取るため
from dotenv import load_dotenv  # .envファイルから設定を読み込むため

# ============================================
# 初期設定
# ============================================

# 環境変数を読み込み（.envファイルの内容を使えるようにする）
load_dotenv()

# ボットの設定
# Intentsはボットがどんな情報にアクセスできるかを決める設定
intents = discord.Intents.default()  # 基本的な機能を使用
# スラッシュコマンド専用ボットなので、message_contentインテントは不要
# intents.message_content = True  # メッセージの内容を読み取る権限（コメントアウト）

# ボットのインスタンス（実体）を作成
# command_prefix=None でメッセージコマンドは使わない（スラッシュコマンドのみ）
bot = commands.Bot(command_prefix=None, intents=intents)

# ============================================
# ルーレットゲームのクラス（設計図）
# ============================================

class RouletteGame:
    """
    ロシアンルーレットゲームを管理するクラス
    このクラスでゲームの状態や進行を管理します
    """
    
    def __init__(self):
        """
        ゲームオブジェクトを初期化する関数
        新しいゲームを作るときに最初に実行される
        """
        self.players = []           # 参加者のリスト（空の状態から開始）
        self.is_active = False      # ゲームが進行中かどうか（False = 停止中）
        self.current_chamber = 0    # 現在何発目を撃ったか（0から開始）
        self.bullet_chamber = 0     # 実弾が入っているチャンバーの位置
        self.max_chambers = 6       # リボルバーの弾倉数（6発）
        
    def start_game(self, participants):
        """
        ゲームを開始する関数
        参加者リストをもとにゲームの準備をする
        """
        self.players = participants.copy()  # 参加者リストをコピーして保存
        self.is_active = True                # ゲーム開始フラグをオンにする
        self.current_chamber = 0             # 撃った回数をリセット
        
        # 1〜6のどこに実弾があるかをランダムに決める
        self.bullet_chamber = random.randint(1, self.max_chambers)
        
        # プレイヤーの順番をランダムにシャッフル（公平性のため）
        random.shuffle(self.players)
        
    def pull_trigger(self):
        """
        引き金を引く関数
        実弾かどうかを判定して結果を返す
        """
        self.current_chamber += 1  # 撃った回数を1増やす
        
        # 現在のチャンバーが実弾の位置と同じかチェック
        return self.current_chamber == self.bullet_chamber
        
    def reset(self):
        """
        ゲームをリセットする関数
        ゲーム終了時や強制停止時に呼び出される
        """
        self.players = []           # 参加者リストを空にする
        self.is_active = False      # ゲーム停止フラグをオンにする
        self.current_chamber = 0    # 撃った回数をリセット
        self.bullet_chamber = 0     # 実弾位置をリセット

# ============================================
# ゲームのインスタンス（実体）を作成
# ============================================
# このgameオブジェクトで全てのゲーム進行を管理する
game = RouletteGame()

# ============================================
# ボットのイベント処理
# ============================================

@bot.event
async def on_ready():
    """
    ボットがDiscordに接続完了したときに実行される関数
    スラッシュコマンドの同期もここで行う
    """
    print(f'{bot.user} がログインしました！')
    print(f'ボットID: {bot.user.id}')
    print('スラッシュコマンドの同期を開始...')
    
    # スラッシュコマンドを同期（Discordサーバーに登録）
    try:
        guild_id = os.getenv('GUILD_ID')  # .envファイルからギルドIDを取得
        print(f'GUILD_ID環境変数: {guild_id}')
        
        if guild_id and guild_id != 'your_guild_id_here':
            # 特定のサーバー（ギルド）にのみ同期（開発・テスト用）
            # この方法だと即座に反映される
            print(f'ギルド {guild_id} への同期を実行中...')
            guild = discord.Object(id=int(guild_id))
            synced = await bot.tree.sync(guild=guild)
            print(f'✅ ギルド {guild_id} に同期されたコマンド数: {len(synced)}')
        else:
            # グローバル同期（全てのサーバーで使用可能）
            # この方法だと反映に最大1時間かかる
            print('グローバル同期を実行中...')
            synced = await bot.tree.sync()
            print(f'✅ グローバルに同期されたコマンド数: {len(synced)}')
            print('⚠️  グローバル同期は反映に最大1時間かかる場合があります')
            
    except Exception as e:
        # エラーが発生した場合の処理
        print(f'❌ コマンド同期エラー: {e}')
        import traceback
        traceback.print_exc()  # 詳細なエラー情報を表示
    
    print('------')
    print('🎯 ボットが正常に起動しました！')

# ============================================
# スラッシュコマンドの定義
# ============================================

# /roulette コマンドの定義
@bot.tree.command(name="roulette", description="ロシアンルーレットを開始します")
@app_commands.describe(
    # 各引数の説明（ユーザーがコマンドを使うときに表示される）
    player1="参加者1 (必須)",
    player2="参加者2 (必須)", 
    player3="参加者3 (オプション)",
    player4="参加者4 (オプション)",
    player5="参加者5 (オプション)",
    player6="参加者6 (オプション)",
    player7="参加者7 (オプション)",
    player8="参加者8 (オプション)",
    player9="参加者9 (オプション)",
    player10="参加者10 (オプション)"
)
async def start_roulette(interaction: discord.Interaction, 
                        player1: discord.Member,
                        player2: discord.Member,
                        player3: discord.Member = None,
                        player4: discord.Member = None,
                        player5: discord.Member = None,
                        player6: discord.Member = None,
                        player7: discord.Member = None,
                        player8: discord.Member = None,
                        player9: discord.Member = None,
                        player10: discord.Member = None):
    """
    ロシアンルーレットを開始するスラッシュコマンド
    
    Parameters:
    - interaction: Discordからの操作情報
    - player1, player2: 必須参加者
    - player3-10: オプション参加者
    """
    
    # ============================================
    # ゲーム開始前のチェック
    # ============================================
    
    # すでにゲームが進行中かチェック
    if game.is_active:
        # ephemeral=True でこのメッセージは実行者にのみ見える
        await interaction.response.send_message("❌ すでにゲームが進行中です！", ephemeral=True)
        return  # 関数を終了
    
    # ============================================
    # 参加者リストの作成と整理
    # ============================================
    
    # 必須参加者（player1, player2）をリストに追加
    players = [player1, player2]
    
    # オプション参加者のリストを作成
    optional_players = [player3, player4, player5, player6, player7, player8, player9, player10]
    
    # オプション参加者の中でNone（未選択）でないものをリストに追加
    for player in optional_players:
        if player is not None:  # 参加者が選択されている場合
            players.append(player)
    
    # ============================================
    # 重複チェックと無効な参加者の除外
    # ============================================
    
    # 重複を避けるための処理
    unique_players = []     # 重複のない参加者リスト
    seen_ids = set()        # すでに追加したユーザーのIDを記録
    
    for player in players:
        # 同じユーザーが複数回選択されていないか & ボット自身が選択されていないかチェック
        if player.id not in seen_ids and player != bot.user:
            unique_players.append(player)
            seen_ids.add(player.id)  # このユーザーを記録
    
    # 参加者が2人未満の場合はエラー
    if len(unique_players) < 2:
        await interaction.response.send_message("❌ 最低2人の異なる参加者が必要です！", ephemeral=True)
        return
    
    
    # ============================================
    # ゲーム開始処理
    # ============================================
    
    # Discord.Member オブジェクトから表示名（ニックネーム）を取得
    player_names = [player.display_name for player in unique_players]
    
    # ゲームクラスでゲームを開始（実弾位置決定、順番シャッフルなど）
    game.start_game(player_names)
    
    # ============================================
    # 開始メッセージの作成と送信
    # ============================================
    
    # Embedメッセージ（装飾されたメッセージ）を作成
    embed = discord.Embed(
        title="🎯 ロシアンルーレット開始！",
        description=f"参加者: {', '.join(player_names)}\n\n6発中1発が実弾です...",
        color=discord.Color.red()  # 赤色のテーマ
    )
    
    # ルール説明のフィールドを追加
    embed.add_field(
        name="ルール",
        value="順番に引き金を引きます。実弾を引いたプレイヤーが負けです！",
        inline=False  # フィールドを横並びにしない
    )
    
    # ユーザーにメッセージを送信
    await interaction.response.send_message(embed=embed)
    
    # ============================================
    # ゲーム進行開始
    # ============================================
    await play_roulette(interaction)

async def play_roulette(interaction):
    """
    ルーレットゲームの進行を管理する関数
    各プレイヤーが順番に引き金を引き、勝敗が決まるまで繰り返す
    
    Parameters:
    - interaction: Discordからの操作情報（フォローアップメッセージ送信用）
    """
    round_num = 1  # 現在のラウンド数
    
    # ゲームが進行中 かつ 参加者が2人以上いる限り続行
    while game.is_active and len(game.players) > 1:
        
        # ============================================
        # 現在のターンのプレイヤーを取得
        # ============================================
        current_player = game.players[0]  # 先頭のプレイヤーが現在のターン
        
        # ============================================
        # ターン開始メッセージの作成
        # ============================================
        embed = discord.Embed(
            title=f"🎯 第{round_num}ラウンド",
            description=f"**{current_player}** の番です！",
            color=discord.Color.orange()  # オレンジ色で緊張感を演出
        )
        
        # 現在の状況を表示するフィールドを追加
        embed.add_field(
            name="残り参加者",
            value=f"{len(game.players)}人: {', '.join(game.players)}",
            inline=False  # 横並びにしない
        )
        embed.add_field(
            name="チャンバー",
            value=f"{game.current_chamber}/{game.max_chambers}",
            inline=True  # 横並びにする（コンパクト表示）
        )
        
        # メッセージを送信（followupは最初のresponse後に使用）
        await interaction.followup.send(embed=embed)
        
        # 緊張感を演出するための2秒待機
        await asyncio.sleep(2)
        
        # ============================================
        # 引き金を引く処理
        # ============================================
        is_bullet = game.pull_trigger()  # GameクラスのメソッドでTrue/Falseを判定
        
        if is_bullet:
            # ============================================
            # 実弾を引いた場合の処理（ゲーム終了）
            # ============================================
            
            # 敗北メッセージの作成
            embed = discord.Embed(
                title="💥 BANG!",
                description=f"**{current_player}** が実弾を引きました！",
                color=discord.Color.dark_red()  # 濃い赤色で危険を表現
            )
            embed.add_field(
                name="ゲーム終了",
                value=f"**{current_player}** の負けです！",
                inline=False
            )
            
            # 勝者の発表
            if len(game.players) > 2:
                # 3人以上の場合は「生存者」として表示
                winners = [p for p in game.players if p != current_player]
                embed.add_field(
                    name="🏆 生存者",
                    value=f"{', '.join(winners)}",
                    inline=False
                )
            else:
                # 2人の場合は「勝者」として表示
                winner = [p for p in game.players if p != current_player][0]
                embed.add_field(
                    name="🏆 勝者",
                    value=f"**{winner}**",
                    inline=False
                )
            
            # ゲーム終了処理
            await interaction.followup.send(embed=embed)
            game.reset()  # ゲーム状態をリセット
            return  # 関数を終了してゲームを完全に終了
            
        else:
            # ============================================
            # 空砲の場合の処理（ゲーム継続）
            # ============================================
            
            # セーフティメッセージの作成
            embed = discord.Embed(
                title="🔫 カチッ...",
                description=f"**{current_player}** はセーフ！",
                color=discord.Color.green()  # 緑色で安全を表現
            )
            await interaction.followup.send(embed=embed)
            
            # ============================================
            # 次のターンの準備
            # ============================================
            
            # 現在のプレイヤーをリストの最後に移動（順番を回す）
            game.players.append(game.players.pop(0))
            round_num += 1  # ラウンド数を増加
            
            # 次のターンまでの間隔を設ける
            await asyncio.sleep(1.5)

# ============================================
# その他のスラッシュコマンド
# ============================================

@bot.tree.command(name="stop", description="進行中のロシアンルーレットを停止します")
async def stop_roulette(interaction: discord.Interaction):
    """
    進行中のゲームを強制停止するコマンド
    ゲームが進行中でない場合はエラーメッセージを表示
    """
    
    # ゲームが進行中でない場合はエラー
    if not game.is_active:
        await interaction.response.send_message("❌ 進行中のゲームがありません。", ephemeral=True)
        return
    
    # ゲームを停止してリセット
    game.reset()
    
    # 停止完了メッセージを作成
    embed = discord.Embed(
        title="⛔ ゲーム停止",
        description="ロシアンルーレットが停止されました。",
        color=discord.Color.blue()  # 青色で情報メッセージを表現
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rules", description="ロシアンルーレットのルールを表示します")
async def roulette_rules(interaction: discord.Interaction):
    """
    ルールとコマンドの使い方を表示するコマンド
    初心者向けにゲームの説明を提供
    """
    
    # ルール説明用のEmbedメッセージを作成
    embed = discord.Embed(
        title="🎯 ロシアンルーレット ルール",
        color=discord.Color.blue()  # 青色で情報メッセージを表現
    )
    
    # 基本ルールの説明
    embed.add_field(
        name="基本ルール",
        value="6発のうち1発が実弾です。順番に引き金を引き、実弾を引いたプレイヤーが負けです。",
        inline=False  # フィールドを横並びにしない
    )
    
    # 利用可能なコマンドの説明
    embed.add_field(
        name="スラッシュコマンド",
        value="`/roulette` - ゲーム開始 (参加者を選択)\n`/stop` - ゲーム停止\n`/rules` - ルール表示",
        inline=False
    )
    
    # 参加者数の制限
    embed.add_field(
        name="参加者数",
        value="最低2人〜最大10人",
        inline=True  # コンパクトに表示
    )
    
    # ルールメッセージをユーザーに送信
    await interaction.response.send_message(embed=embed)

# ============================================
# エラーハンドリング
# ============================================

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """
    スラッシュコマンドでエラーが発生した際の処理
    ユーザーにわかりやすいエラーメッセージを表示
    """
    
    if isinstance(error, app_commands.CommandOnCooldown):
        # コマンド使用制限エラーの場合
        await interaction.response.send_message(
            f"❌ コマンドはクールダウン中です。{error.retry_after:.1f}秒後に再試行してください。",
            ephemeral=True  # 実行者にのみ表示
        )
    elif isinstance(error, app_commands.MissingPermissions):
        # 権限不足エラーの場合
        await interaction.response.send_message(
            "❌ このコマンドを使用する権限がありません。",
            ephemeral=True
        )
    else:
        # その他のエラーの場合
        embed = discord.Embed(
            title="❌ エラー",
            description=f"コマンドの実行中にエラーが発生しました: {str(error)}",
            color=discord.Color.red()  # 赤色でエラーを表現
        )
        
        # レスポンス済みかどうかで送信方法を変える
        if interaction.response.is_done():
            # すでにレスポンス済みの場合はfollowupを使用
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            # まだレスポンスしていない場合は通常のresponseを使用
            await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================
# ボット起動処理
# ============================================

# このスクリプトが直接実行された場合のみボットを起動
# （他のファイルからimportされた場合は起動しない）
if __name__ == "__main__":
    # 環境変数からDiscordボットのトークンを取得
    token = os.getenv('DISCORD_TOKEN')
    
    # トークンが設定されているかチェック
    if not token:
        print("❌ DISCORD_TOKENが設定されていません！")
        print(".envファイルにトークンを設定してください。")
    else:
        # トークンが設定されている場合、ボットを起動
        print("🚀 ボットを起動しています...")
        bot.run(token)
