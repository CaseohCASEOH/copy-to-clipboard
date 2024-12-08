import discord
from discord.ext import commands
from discord import app_commands
import os
import random

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

@bot.tree.command(name="send_embed", description="Send a custom embed.")
@app_commands.describe(
    title="The title of the embed",
    description="The description of the embed",
    color="The color of the embed (red, blue, green)",
    footer="The footer of the embed (optional)",
    image_url="The image URL for the embed (optional)"
)
async def send_embed(interaction: discord.Interaction, title: str, description: str, color: str, footer: str = None, image_url: str = None):
    embed = discord.Embed(title=title, description=description)
    if color.lower() == "red":
        embed.color = discord.Color.red()
    elif color.lower() == "blue":
        embed.color = discord.Color.blue()
    elif color.lower() == "green":
        embed.color = discord.Color.green()
    else:
        embed.color = discord.Color.default()
    if footer:
        embed.set_footer(text=footer)
    if image_url:
        embed.set_image(url=image_url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="random_fact", description="Get a random interesting fact.")
async def random_fact(interaction: discord.Interaction):
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries are not.",
        "Octopuses have three hearts.",
        "The Eiffel Tower grows taller in summer.",
        "Sharks existed before trees.",
        "A day on Venus is longer than a year on Venus.",
        "Wombat poop is cube-shaped.",
        "Sloths can hold their breath longer than dolphins.",
        "The human nose can detect about 1 trillion smells.",
        "The speed of a computer mouse is measured in 'Mickeys.'"
    ]
    fact = random.choice(facts)
    await interaction.response.send_message(f"📚 Random Fact: {fact}")

@bot.tree.command(name="server_info", description="Get server information.")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.blurple())
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=f"{guild.owner}", inline=False)
    embed.add_field(name="Member Count", value=f"{guild.member_count} members", inline=False)
    embed.add_field(name="Online Members", value=sum(member.status != discord.Status.offline for member in guild.members), inline=True)
    embed.add_field(name="Boost Level", value=f"Tier {guild.premium_tier}", inline=True)
    embed.add_field(name="Boost Count", value=f"{guild.premium_subscription_count} boosts", inline=True)
    embed.add_field(name="Text Channels", value=f"{len(guild.text_channels)}", inline=True)
    embed.add_field(name="Voice Channels", value=f"{len(guild.voice_channels)}", inline=True)
    embed.add_field(name="Role Count", value=f"{len(guild.roles)}", inline=True)
    embed.add_field(name="Emoji Count", value=f"{len(guild.emojis)} emojis", inline=True)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%B %d, %Y at %H:%M:%S"), inline=False)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rizz_checker", description="Check someone's Rizz level.")
@app_commands.describe(user="The user to check Rizz level.")
async def rizz_checker(interaction: discord.Interaction, user: discord.User):
    rizz_level = random.randint(0, 100)
    remark = "🔥 OMG! Rizz Master!" if rizz_level >= 90 else "😎 Good Rizz!" if rizz_level >= 70 else "👌 Decent Rizz" if rizz_level >= 40 else "🤷 Needs Rizz School" if rizz_level >= 10 else "💀 No Rizz"
    await interaction.response.send_message(f"{user.mention} has a Rizz level of **{rizz_level}**! {remark}")

@bot.tree.command(name="invite_bot", description="Get the bot's invite link.")
async def invite_bot(interaction: discord.Interaction):
    perms = discord.Permissions(administrator=True)
    invite_link = discord.utils.oauth_url(bot.user.id, permissions=perms)
    await interaction.response.send_message(f"Invite me to your server using this link: {invite_link}")
