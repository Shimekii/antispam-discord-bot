import discord
from discord.ext import commands
from utils.utils import load_config
import os
import asyncio

config = load_config()
bot = commands.Bot(command_prefix="!",
                   intents=discord.Intents.all())

token = config.get("token")

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.invisible
    )
    print("Bot running")

async def load_cogs(bot):
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("Нет прав для выполнения этой команды", ephemeral=True)
        return

@bot.event
async def setup_hook():
    await load_cogs(bot)
    await bot.tree.sync()

bot.run(token)