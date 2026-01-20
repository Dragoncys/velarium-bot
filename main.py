import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import ssl
import aiohttp
import certifi

# Load environment variables
load_dotenv()

# SSL configuration using certifi certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=",", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def load_cogs():
    """Load all cogs from the cogs folder"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")

async def main():
    # Create custom connector with certifi SSL context
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with bot:
            bot.http._session = session  
            await load_cogs()
            TOKEN = os.getenv("DISCORD_TOKEN")
            if not TOKEN:
                raise ValueError("DISCORD_TOKEN not found in .env file!")
            await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
