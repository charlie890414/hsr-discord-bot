import time
import os

import discord
from dotenv import load_dotenv

from core.utils import (
    exact_gift_codes,
    get_all_users_cookie,
    get_user_cookie,
    redeem,
    set_user_cookie,
)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@tree.command(name="set-cookie", description="set up hoyolab cookie")
async def set_cookie(interaction: discord.Interaction, cookie: str):
    set_user_cookie(interaction.user.id, cookie)
    print(f"user {interaction.user} set cookie")
    await interaction.response.send_message("Cookie set")


@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        gift_codes = exact_gift_codes(message.content)
        cookie = get_user_cookie(message.author.id)

        if gift_codes and not cookie:
            await message.author.send("Cookie not set yet!")
            return

        for gift_code in gift_codes:
            rsp = redeem(cookie, gift_code)
            await message.author.send(gift_code + '\n' + rsp.text)
            time.sleep(5)

    elif isinstance(message.channel, discord.TextChannel) and str(message.channel.id) == os.getenv("CHANNEL_ID"):
        print(f"Channel Message from {message.author}: {message.content}")

        gift_codes = exact_gift_codes(message.content)

        for uid, cookie in get_all_users_cookie().items():
            for gift_code in gift_codes:
                rsp = redeem(cookie, gift_code)
                user = await client.fetch_user(uid)
                await user.send(gift_code + '\n' + rsp.text)
                time.sleep(5)


client.run(os.getenv("BOT_TOKEN"))
