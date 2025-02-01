import discord
from discord.ext import commands
from discord import app_commands

# Botトークン
TOKEN = "とーくん"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # メンバー情報の取得に必要

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Treeを同期
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="say", description="指定されたユーザー風のメッセージを送信します")
@app_commands.describe(user="メッセージを送信する際のユーザー", message="送信するメッセージ内容")
async def say(interaction: discord.Interaction, user: discord.Member, message: str):
    """
    指定されたチャンネルにウェブフックを作成して送信し、
    実行者にのみ結果を表示する
    """
    try:
        # 実行されたチャンネル
        channel = interaction.channel

        # チャンネルにWebhookを作成
        webhook = await channel.create_webhook(name=f"{user.display_name}'s webhook")

        # ユーザーの名前とアバターURLを取得
        username = user.display_name
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        # Webhookでメッセージを送信
        await webhook.send(
            content=message,  # メッセージ内容
            username=username,  # Webhookの名前をユーザー名に設定
            avatar_url=avatar_url  # Webhookのアイコンをユーザーのアイコンに設定
        )

        # Webhookを削除
        await webhook.delete()

        # 実行者のみに応答
        await interaction.response.send_message("メッセージを送信しました！", ephemeral=True)

    except Exception as e:
        # エラーハンドリング（実行者のみに表示）
        await interaction.response.send_message(f"エラーが発生しました: {str(e)}", ephemeral=True)


bot.run(TOKEN)
