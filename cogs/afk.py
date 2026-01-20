from discord.ext import commands
import discord
import time
from datetime import datetime, timedelta
from discord import app_commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}  # guild_id: {user_id: {reason, since, pings: [(author, msg)]}}

    @commands.command()
    async def afk(self, ctx, *, reason: str = "AFK"):
        """Set your AFK status with an optional reason."""
        await self.set_afk(ctx, reason)

    @app_commands.command(name="afk", description="Set your AFK status with an optional reason.")
    @app_commands.describe(reason="Reason for going AFK (optional)")
    async def afk_slash(self, interaction: discord.Interaction, reason: str = None):
        if not reason:
            reason = "AFK"
        class DummyCtx:
            def __init__(self, interaction):
                self.author = interaction.user
                self.guild = interaction.guild
                self.send = interaction.response.send_message
            async def send(self, *args, **kwargs):
                await interaction.response.send_message(*args, **kwargs)
        ctx = DummyCtx(interaction)
        await self.set_afk(ctx, reason)

    async def set_afk(self, ctx, reason):
        guild_id = ctx.guild.id
        if guild_id not in self.afk_users:
            self.afk_users[guild_id] = {}
        self.afk_users[guild_id][ctx.author.id] = {
            "reason": reason,
            "since": time.time(),
            "pings": []
        }
        embed = discord.Embed(title="AFK Set", description=f"You are now AFK: **{reason}**", color=0x2F3136)
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.set_footer(text=datetime.now().strftime("Today at %H:%M"))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        guild_id = message.guild.id
        # Remove AFK if user returns (but not if they just used the afk command)
        if guild_id in self.afk_users and message.author.id in self.afk_users[guild_id]:
            ctx = await self.bot.get_context(message)
            if ctx.valid and ctx.command and ctx.command.name == "afk":
                return  # Don't remove AFK if the user just used the afk command
            afk_data = self.afk_users[guild_id].pop(message.author.id)
            since = afk_data["since"]
            reason = afk_data["reason"]
            pings = afk_data["pings"]
            afk_time = str(timedelta(seconds=int(time.time() - since)))
            embed = discord.Embed(title="AFK Removed", color=0x43b581)
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
            embed.add_field(name="Welcome back!", value=f"You were AFK for **{afk_time}**.\nYou received **{len(pings)}** ping(s) while AFK.", inline=False)
            if pings:
                mention_list = []
                for i, (author, msg, jump_url) in enumerate(pings, 1):
                    mention_list.append(f"**{i}.** [{author.display_name}]({jump_url})")
                
                # Limit to 10 most recent pings to avoid embed limit
                if len(mention_list) > 10:
                    mention_list = mention_list[-10:]
                    mention_text = "\n".join(mention_list)
                    mention_text = f"*Showing last 10 pings (total: {len(pings)})*\n\n" + mention_text
                else:
                    mention_text = "\n".join(mention_list)
                
                embed.add_field(name="Mentions While AFK:", value=mention_text, inline=False)
            embed.set_footer(text=datetime.now().strftime("Today at %H:%M"))
            await message.channel.send(embed=embed)
        # Notify if mentioned user is AFK and track pings
        if guild_id in self.afk_users:
            for user in message.mentions:
                if user.id in self.afk_users[guild_id]:
                    afk_data = self.afk_users[guild_id][user.id]
                    reason = afk_data["reason"]
                    embed = discord.Embed(title="AFK Notice", description=f"{user.display_name} is AFK: **{reason}**", color=0x2F3136)
                    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
                    embed.set_footer(text=datetime.now().strftime("Today at %H:%M"))
                    await message.channel.send(embed=embed)
                    afk_data["pings"].append((message.author, message.content, message.jump_url))

async def setup(bot):
    await bot.add_cog(AFK(bot))
