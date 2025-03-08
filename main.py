from typing import Final
import os

from discord.ext.commands import check_any
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import datetime

# load token to save place
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

# Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message or user_message[0] != '.':
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')

# handlich messages

ALLOWED_CHANNELS = {1158397312758976593, 1339714686589079694    }
ADMIN = 957639097042731088
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    if message.channel.id not in ALLOWED_CHANNELS:
        return

    if message.content == 'kys':
        if message.author.id == ADMIN: await message.channel.send('I would listen to what my master says....')
        else: await message.channel.send(f'no u kys {message.author.mention}')
        return

    if "good night" or "gn" in message.content.lower():
        current_hour = datetime.datetime.now().hour
        if current_hour <= 23:  # Before 10 PM
            await message.channel.send("So early? 😲")
        else: # After 10 PM
            await message.channel.send("Good night! :heart_on_fire:")

    if message.author.id == ADMIN and message.content == 'die':
        await message.channel.send('meanie :(')
        await client.close()
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'{username} in {channel} said: {user_message}')
    await send_message(message, user_message)

# main entry point
def main() -> None:
    client.run(token = TOKEN)

if __name__ == '__main__':
    main()

