from typing import Final
import os

from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import datetime
import asyncio

# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Persistent active flag
active = True


async def send_message(message: Message, user_message: str) -> None:
    global active
    if not user_message or user_message[0] != '.':
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    # If bot is inactive, ignore all messages
    if not active:
        return

    try:
        response: str = get_response(user_message, active)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


# Handle startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')


# Handling messages
ALLOWED_CHANNELS = {1158397312758976593, 1339714686589079694}
ADMIN = 957639097042731088


@client.event
async def on_message(message: Message) -> None:
    global active

    if message.author == client.user:
        return

    if message.channel.id not in ALLOWED_CHANNELS:
        return

    # Toggle bot silence
    if message.content.lower() == 'hai rotto il cazzo':
        active = False
        await message.channel.send("Fine, I'll shut up.")
        return

    if message.content.lower() == 'parla':
        active = True
        await message.channel.send("I'm back 😈")
        return

    # If bot is inactive, ignore all messages
    if not active:
        return

        # Special responses
    if message.content == 'kys':
        if message.author.id == ADMIN:
            await message.channel.send('I would listen to what my master says....')
        else:
            await message.channel.send(f'no u kys {message.author.mention}')
        return

    if "good night" in message.content.lower() or message.content == 'gn':
        current_hour = datetime.datetime.now().hour
        if current_hour <= 23:
            await message.channel.send("So early? 😲")
        else:
            await message.channel.send("Good night! :heart_on_fire:")

    if message.content == 'ok':
        await message.channel.send('why so dry? im not one of your bitches :(')

    # Spam feature
    if '.spam' in message.content.lower():
        parts = message.content.split(' ')

        if len(parts) < 2:
            await message.channel.send("Usage: `.spam <message> <optional: count>`")
            return

        spam_message = parts[1]
        count = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10  # Default count = 10

        for _ in range(count):
            try:
                exit_message = await client.wait_for(
                    "message",
                    timeout=0.5,
                    check=lambda m: m.author.id == ADMIN and m.content.lower() == "exit"
                )
                if exit_message:
                    await message.channel.send("Spamming stopped by admin.")
                    break
            except asyncio.TimeoutError:
                pass

            await message.channel.send(spam_message)

    # Bot shutdown by admin
    if message.author.id == ADMIN and message.content == 'die':
        await message.channel.send('meanie :(')
        await client.close()
        return

    # Debug log
    print(f'{message.author} in {message.channel} said: {message.content}')
    await send_message(message, message.content)


# Main entry point
def main() -> None:
    client.run(TOKEN)


if __name__ == '__main__':
    main()
