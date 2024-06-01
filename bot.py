import discord
import json
import aiohttp
from discord.ext import commands
import asyncio
from get_data.info import thingg 
import datetime
from process import process_handler, process_stopper, process_status, message_handler, killall, startall, dropped_eyes, dropped_eyes_hourly

message_id = None
timeout_period = 0
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(intents=intents, slash_command_prefix='/')  

with open("config.json") as config:
    data = json.load(config)

async def main(timeout):
    while True:
        if message_id is None:
            await send_embed()
            await asyncio.sleep(timeout * 60)
        else:
            try:
                await update_message()
            except Exception as e:
                print(e)
            await asyncio.sleep(timeout * 60) 

async def send_embed():
    global message_id
    if message_id is not None:
        await main()
    else: 
        embed = discord.Embed(
            title='Account Statistics:',
            description='',
            color=0x1D0FC7,
            )
        lists = data['igns']
        for i in range(0, len(lists)):
            purse, level, rank = await thingg(lists[i])
            if level < 40 and level >= 1:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m{level}[0m[2;37m[0m
```"""
            elif level  < 80 and level >= 40:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m{level}[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 120 and level >= 80:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m{level}[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 160 and level >= 120:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m{level}[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 200 and level >= 160:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m{level}[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 240 and level >= 200:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m[2;34m{level}[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 280 and level >= 240:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m[2;34m[2;36m{level}[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            
            
            purse = f"""```ansi
[2;37m[0m[2;37mPurse: [2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[2;31m[2;45m[2;30m[2;47m[2;40m[2;33m{purse}[0m[2;30m[2;40m[0m[2;30m[2;47m[0m[2;30m[2;45m[0m[2;31m[2;45m[0m[2;31m[0m[2;35m[2;30m[0m[2;35m[0m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
           
            
            if rank == 'VIP+' or rank == 'VIP':
                rank = f"""```ansi
[2;37m[0m[2;37m[2;32m{rank}[0m[2;37m[2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif rank == 'MVP' or rank == 'MVP+':
                rank = f"""```ansi
[2;37m[0m[2;37m[2;32m[2;34m{rank}[0m[2;32m[0m[2;37m[2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif rank == 'NON':
                rank = f"""```ansi
[2;37m[0m[2;37m[2;32m[2;34m[2;30m{rank}[0m[2;34m[0m[2;32m[0m[2;37m[2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            if 'B' in purse:
                embed.add_field(name=f"``{lists[i]}``", value=f'{rank} \n{purse} \n{level}', inline=True)
            else:
                embed.add_field(name=f"``{lists[i]}``", value=f'{rank} \n{purse} \n{level}', inline=True)
        channel = bot.get_channel(data['bot']['channel'])
        embed1 = await process_status(channel)
        embed2 = discord.Embed(title="Runtime Statistics", description='', color=0x1D0FC7)
        embed2.add_field(name=f"**Total Eyes**", value=''.join([f':eye_in_speech_bubble: **``{lists[i]}``: {dropped_eyes[lists[i]]}** \n' for i in range(len(lists))]))
        embed2.add_field(name=f"**Hourly Eyes**", value=''.join([f':eye_in_speech_bubble: **``{lists[i]}``: {dropped_eyes_hourly[lists[i]]}** \n' for i in range(len(lists))]))
        embed2.set_footer(text='Made by interceptic', icon_url='https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160')
        embed2.timestamp = datetime.datetime.now()
        message = await channel.send(embeds=[embed, embed1, embed2])
        message_id = message.id
        print(message_id)
        return

async def update_message():
    channel = bot.get_channel(data['bot']['channel'])
    try:
        message = await channel.fetch_message(message_id)
        embed = discord.Embed(
            title='Account Statistics:',
            description='',
            color=0x1D0FC7,
        )
        lists = data['igns']
        for i in range(len(lists)):
            purse, level, rank = await thingg(lists[i])
            if level < 40 and level >= 1:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m{level}[0m[2;37m[0m
```"""
            elif level  < 80 and level >= 40:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m{level}[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 120 and level >= 80:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m{level}[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 160 and level >= 120:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m{level}[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 200 and level >= 160:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m{level}[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 240 and level >= 200:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m[2;34m{level}[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif level < 280 and level >= 240:
                level = f"""```ansi
[2;37m[0m[2;37mLevel: [2;30m[2;37m[2;33m[2;32m[2;34m[2;36m{level}[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            
            
            purse = f"""```ansi
[2;37m[0m[2;37mPurse: [2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[2;31m[2;45m[2;30m[2;47m[2;40m[2;33m{purse}[0m[2;30m[2;40m[0m[2;30m[2;47m[0m[2;30m[2;45m[0m[2;31m[2;45m[0m[2;31m[0m[2;35m[2;30m[0m[2;35m[0m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""            
            if rank == 'VIP+' or rank == 'VIP':
                rank = f"""```ansi
[2;37m[0m[2;37m[2;32m{rank}[0m[2;37m[2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif rank == 'MVP' or rank == 'MVP+':
                rank = f"""```ansi
[2;37m[0m[2;37m[2;32m[2;34m{rank}[0m[2;32m[0m[2;37m[2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            elif rank == 'NON':
                rank = f"""```ansi
[2;37m[0m[2;37m[2;32m[2;34m[2;30m{rank}[0m[2;34m[0m[2;32m[0m[2;37m[2;30m[2;37m[2;33m[2;32m[2;34m[2;36m[2;33m[2;35m[0m[2;33m[0m[2;36m[0m[2;34m[0m[2;32m[0m[2;33m[0m[2;37m[0m[2;30m[0m[2;37m[0m
```"""
            if 'B' in purse:
                embed.add_field(name=f"``{lists[i]}``", value=f'{rank} \n{purse} \n{level}', inline=True)
            else:
                embed.add_field(name=f"``{lists[i]}``", value=f'{rank} \n{purse} \n{level}', inline=True)
        embed1 = await process_status(channel)
        embed2 = discord.Embed(title="Runtime Statistics", description='', color=0x1D0FC7)
        embed2.add_field(name=f"**Total Eyes**", value=''.join([f':eye_in_speech_bubble: **``{lists[i]}``: {dropped_eyes[lists[i]]}** \n' for i in range(len(lists))]))
        embed2.add_field(name=f"**Hourly Eyes**", value=''.join([f':eye_in_speech_bubble: **``{lists[i]}``: {dropped_eyes_hourly[lists[i]]}** \n' for i in range(len(lists))]))
        embed2.set_footer(text='Made by interceptic', icon_url='https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160')
        embed2.timestamp = datetime.datetime.now()
        await message.edit(embeds=[embed,embed1, embed2])
        print(f"Message with ID {message_id} has been updated")
    except discord.NotFound:
        print(f"Message with ID {message_id} not found")
    return



@bot.event
async def on_ready():
    print('Logged in!')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Made by Interceptic"))
    await bot.sync_commands()

def user_choices(ctx: discord.AutocompleteContext):
    return [discord.OptionChoice(name=ign, value=ign) for ign in data['igns']]

@bot.slash_command(name='start', description="Start slayer processes.",)
async def start(interaction: discord.Interaction, username: discord.Option(str, "Which user would you like to start?", autocomplete=user_choices)):
    if interaction.author.id == data['bot']['your_id']:
        await interaction.response.defer()
        await interaction.followup.send(f"Starting username: ``{username}``, with timeout period of {data['configuration']['restart_time']} minutes", ephemeral=False)
        await process_handler(username, on=True)
    else: 
        await interaction.response.send_message(f"Sorry, only <@{data['bot']['your_id']}> is able to use this command :( ", ephemeral=True)

@bot.slash_command(name='stop', description='Stop a slayer process')
async def stop(interaction: discord.Interaction, username: discord.Option(str, "Which user would you like to stop?", autocomplete=user_choices)):
    if interaction.author.id == data['bot']['your_id']:
        await interaction.response.defer()
        await interaction.followup.send(f'Stopping {username}...', ephemeral=True)
        await process_stopper(username, False)
    else: 
        await interaction.response.send_message(f"Sorry, only <@{data['bot']['your_id']}> is able to use this command :( ", ephemeral=True)


@bot.slash_command(name="stats", description="Start tracking the stats of your accounts!")
async def purse(interaction: discord.Interaction, timeout: int,):
    if interaction.author.id == data['bot']['your_id']:
        await interaction.response.defer()
        await interaction.followup.send(f"Starting update embed coroutine with timeout period of {timeout} minutes", ephemeral=True)
        await main(timeout)
    else: 
        await interaction.response.send_message(f"Sorry, only <@{data['bot']['your_id']}> is able to use this command :( ", ephemeral=True)

@bot.slash_command(name='chat', description='Send something in chat...')
async def chat(interaction: discord.Interaction, username: discord.Option(str, "Which user?", autocomplete=user_choices), text: discord.Option(str,'What would you like to say?')):
    if interaction.author.id == data['bot']['your_id']:
        await interaction.response.defer()
        await interaction.followup.send(f'Sending message...', ephemeral=False)
        await message_handler(username, text)
    else: 
        await interaction.response.send_message(f"Sorry, only <@{data['bot']['your_id']}> is able to use this command :( ", ephemeral=False)

@bot.slash_command(name='kill', description="Kill all of your slayer processes.")
async def kill(interaction: discord.Interaction):
    if interaction.author.id == data['bot']['your_id']:
        await interaction.response.defer()
        await killall()
        await interaction.followup.send('Processes terminated.', ephemeral=False)
    else:
        await interaction.response.send_message(f"Sorry, only <@{data['bot']['your_id']}> is able to use this command :( ", ephemeral=True)

@bot.slash_command(name="all", description='Start all slayer processes at once.')
async def all(interaction: discord.Interaction):
    if interaction.author.id == data['bot']['your_id']:
        await interaction.response.defer()
        await startall()
        await interaction.followup.send('Starting all processes', ephemeral=False)
    else:
        await interaction.response.send_message(f"Sorry, only <@{data['bot']['your_id']}> is able to use this command :( ", ephemeral=True)
