import os
import pytz
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from keep_alive import keep_alive

intents = discord.Intents.all()
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")
  await check_activity()


user_id_to_monitor = [763581985410121769, 936264687262249050, 1058431535965016215, 791746422546104362]
last_played_game = {}

# ... (other parts of your code)

async def check_activity():
    user_status = {}
    user_activity = {}
    user_activity_type = {}

    while True:
        await asyncio.sleep(5)
        for user_id in user_id_to_monitor:
            guild = client.get_guild(957952395424436244)
            member = guild.get_member(user_id)
            if member:
                if member.activity:
                    activity_name = member.activity.name
                    activity_type = "playing"
                    if isinstance(member.activity, discord.Spotify):
                        activity_type = "listening to"
                    elif isinstance(member.activity, discord.Streaming):
                        activity_type = "streaming"
                    if (
                        user_id not in user_status
                        or not user_status[user_id]
                        or (user_activity.get(user_id) != activity_name)
                        or (user_activity_type.get(user_id) != activity_type)
                    ):
                        channel = client.get_channel(1228718954940465262)
                        if channel:
                            game_icon_url = member.avatar.url
                            embed = discord.Embed(color=0x3be0c3)
                            embed.add_field(
                                name=f"{member.name}",
                                value=f"Started {activity_type} **{activity_name}**",
                                inline=True,
                            )
                            embed.set_thumbnail(url=game_icon_url)
                            embed.set_footer(
                                text=datetime.now(pytz.timezone("Asia/Singapore")).strftime(
                                    "%H:%M at %Y-%m-%d"
                                )
                            )
                            await channel.send(embed=embed)
                            user_status[user_id] = True
                            user_activity[user_id] = activity_name
                            user_activity_type[user_id] = activity_type
                else:
                    # User stopped an activity
                    if user_id in user_status and user_status[user_id]:
                        # Send a notification indicating the activity has stopped
                        channel = client.get_channel(1228718954940465262)
                        if channel:
                            embed = discord.Embed(color=0xff0000)  # Red color for stopped activity
                            embed.add_field(
                                name=f"{member.name}",
                                value=f"Stopped {activity_type} **{activity_name}**",
                                inline=True,
                            )
                            embed.set_thumbnail(url=game_icon_url)
                            embed.set_footer(
                                text=datetime.now(pytz.timezone("Asia/Singapore")).strftime(
                                    "%H:%M at %Y-%m-%d"
                                )
                            )
                            await channel.send(embed=embed)
                            user_status[user_id] = False
                            user_activity[user_id] = None
                            user_activity_type[user_id] = None


@client.command()
async def ping(ctx, pass_context=True):
  await ctx.typing()
  ping = client.latency*1000
  embed = discord.Embed(title="🏓 Pong!", description=f"Latency:\n{round(client.latency * 1000)}ms", color=ctx.author.color)
  await ctx.send(embed=embed)

keep_alive()
TOKEN = os.environ['TOKEN']
client.run(TOKEN)
