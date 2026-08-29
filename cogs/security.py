import discord
from datetime import timedelta
from discord import app_commands
from discord.ext import commands
from utils.utils import load_config, load_guilds, save_guilds
config = load_config()

class SecurityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = load_guilds()

    @app_commands.command(
            name="set-timeout",
            description="Задает время (В МИНУТАХ) таймаута для спамеров. По умолчанию 15"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_timeout(self, 
                          interaction: discord.Interaction,
                          minutes: int):
        guild_id = str(interaction.guild.id)
        guild_settings = self.guilds.get(guild_id)
        if guild_settings.get("timeout") is None:
            await interaction.response.send_message("Канал с ловушкой не настроен", ephemeral=True)
            return
        await interaction.response.send_message(f"Таймаут установлен на {minutes} {plural_minutes(minutes)}", ephemeral=True)
        self.guilds[guild_id]["timeout"] = minutes
        save_guilds(self.guilds)

    @app_commands.command(
            name='set-trap',
            description='Любое написанное сообщение в выбранный канал будет расцениваться как спам, а значит бан'
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_trap(self,
                       interaction: discord.Interaction,
                       channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.guilds:
            self.guilds[guild_id] = {}

        self.guilds[guild_id]["trap_channel"] = channel.id
        self.guilds[guild_id]["timeout"] = 15

        save_guilds(self.guilds)
        await interaction.response.send_message(f"Канал {channel.mention} назначен ловушкой", ephemeral=True)

    @app_commands.command(
            name='remove-trap',
            description='Удалить ловишку с сервера'
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def revome_trap(self,
                          interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id in self.guilds:
            self.guilds[guild_id] = {}
        else:
            await interaction.response.send_message(f"Ловушка не установлена", ephemeral=True)

        save_guilds(self.guilds)
        await interaction.response.send_message(f"Ловушка с данного сервера удалена", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        guild_id = str(message.guild.id)
        guild_settings = self.guilds.get(guild_id)

        if guild_settings is None:
            return

        trap_channel = guild_settings.get("trap_channel")
        timeout = guild_settings.get("timeout")
        if message.channel.id != trap_channel:
            return

        try:
            await message.delete()
            await message.author.timeout(
                timedelta(minutes=timeout),
                reason="Спамит мелстроем дэбил"
            )
        except discord.Forbidden:
            print("Нет прав")

        await message.channel.send(f"{message.author.mention} пойман с мелстроем")


def plural_minutes(minutes: int) -> str:
    if minutes % 100 in (11, 12, 13, 14):
        return "минут"

    last_digit = minutes % 10

    if last_digit == 1:
        return "минуту"
    elif last_digit in (2, 3, 4):
        return "минуты"
    else:
        return "минут"

async def setup(bot):
    print("Loading SecurityCog")
    await bot.add_cog(SecurityCog(bot))