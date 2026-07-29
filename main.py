import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

REQUIRED_GUILD_ID = int(os.getenv('REQUIRED_GUILD_ID', 1516247978950660169))
BOOSTER_ROLE_ID = int(os.getenv('BOOSTER_ROLE_ID', 1528503609661063338))

GIFS_MENSAJES = [
    "https://media.tenor.com/QU7SQ-qgapgAAAAj/67-sixty-seven.gif",
    "https://i.pinimg.com/originals/5d/e3/e4/5de3e4037d97ccf6baff674f068f1d61.gif",
    "https://i.pinimg.com/originals/e4/55/fe/e455fe340771596cc4db7fade9cecb4e.gif",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQwXjoRIzjbj2QXucKQWkOIlkAccCdOmFQIyxa3jMRQQ&s=10",
]

async def check_booster_global(interaction: discord.Interaction):
    guild = bot.get_guild(REQUIRED_GUILD_ID)
    if guild is None:
        return "no_guild"
    member = guild.get_member(interaction.user.id)
    if member is None:
        return "no_guild"
    role = guild.get_role(BOOSTER_ROLE_ID)
    if role is None:
        return "no_role"
    if role not in member.roles:
        return "no_role"
    return "ok"

@bot.event
async def on_ready():
    print(f'BOT READY - {bot.user.name}')
    print('Hi, I\'m ready to nuke.')

@bot.tree.command(name='hi', description='say hi from the bot')
@app_commands.allowed_contexts(
    guilds=True,
    dms=True,
    private_channels=True
)
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message("@everyone Hi, I'm ready to nuke.")

@bot.tree.command(name='nuke', description='spam anywhere without admin')
@app_commands.allowed_contexts(
    guilds=True,
    dms=True,
    private_channels=True
)
async def nuke(interaction: discord.Interaction):
    view = SpamButton(is_embed=True, is_custom=False, es_premium=False)
    await interaction.response.send_message(
        "Click the button to spam:", 
        view=view, 
        ephemeral=True
    )

@bot.tree.command(name='custom', description='spam custom message (premium only)')
@app_commands.allowed_contexts(
    guilds=True,
    dms=True,
    private_channels=True
)
@app_commands.describe(message="The custom message you want to spam")
async def custom(interaction: discord.Interaction, message: str):
    status = await check_booster_global(interaction)
    if status == "no_guild":
        await interaction.response.send_message("You need to be in REZZY SCRIPTS 2.0 server and have Premium role.", ephemeral=True)
        return
    elif status == "no_role":
        await interaction.response.send_message("You need the Premium role to use this command.", ephemeral=True)
        return
    view = SpamButton(message_content=message, is_embed=True, is_custom=True, es_premium=True)
    await interaction.response.send_message(
        "Click the button to spam your custom message:", 
        view=view, 
        ephemeral=True
    )

@bot.tree.command(name='help', description='show all commands')
@app_commands.allowed_contexts(
    guilds=True,
    dms=True,
    private_channels=True
)
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="REZZY ON TOP",
        description="**Commands:**",
        color=0xFF0000
    )
    embed.add_field(name="/hi", value="Hi, I'm ready to nuke.", inline=False)
    embed.add_field(name="/nuke", value="Free nuke", inline=False)
    embed.add_field(name="/custom", value="Custom message nuke (Premium only)", inline=False)
    embed.add_field(name="/help", value="Show this help menu", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

class SpamButton(discord.ui.View):
    def __init__(self, message_content=None, is_embed=True, is_custom=False, es_premium=False):
        super().__init__(timeout=None)
        self.message_content = message_content
        self.is_embed = is_embed
        self.is_custom = is_custom
        self.es_premium = es_premium

    @discord.ui.button(label='START', style=discord.ButtonStyle.red)
    async def nuke_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Sending nuke...", ephemeral=True)

        if self.es_premium:
            delays = [1.1, 1.2]
        else:
            delays = [1.3, 1.4, 1.5]

        if self.is_embed:
            embed = discord.Embed(
                title="**NUKE BY ZenBypass and Rezzy**",
                description="﹌﹌﹌﹌﹌\n• JOIN TO RAID WITHOUT ADMIN\n• [SERVER LINK](https://discord.gg/SbcBENjn)\n• [ZenBypass](https://guns.lol/zenbypas)",
            )
            embed.set_image(url="https://images-ext-1.discordapp.net/external/-3FdgZHKwoquT7YLX2Gp8T43M07sVz6zru0Ls--BOCQ/%3Fsize%3D128/https/cdn.discordapp.com/icons/1516247978950660169/29e68598a80f8f4d05e14579dfbdd63e.png?format=webp&quality=lossless")

            if self.is_custom and self.message_content is not None:
                content_to_send = self.message_content
            else:
                content_to_send = "@everyone REZZY ON TOP"

            for i in range(3):
                gif = random.choice(GIFS_MENSAJES)
                await interaction.followup.send(content=f"{content_to_send}\n\n{gif}", embed=embed)
                if i < 2:
                    await asyncio.sleep(random.choice(delays))
        else:
            if self.is_custom and self.message_content is not None:
                content_to_send = self.message_content
            else:
                content_to_send = "@everyone REZZY ON TOP"
            
            for i in range(3):
                gif = random.choice(GIFS_MENSAJES)
                await interaction.followup.send(content=f"{content_to_send}\n\n{gif}")
                if i < 2:
                    await asyncio.sleep(random.choice(delays))

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))
