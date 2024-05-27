import discord
import json
import aiohttp
from discord.ext import commands
import asyncio
from get_data.info import thingg 
import datetime
from modules.process import process_handler
from modules.process import process_stopper
from modules.process import process_status
from modules.process import message_handler
from modules.process import killall
from modules.process import startall

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
            title='Account Purse:',
            description='',
            color=0x1D0FC7,
            )
        list = data['igns']
        for i in range(0, len(list)):
            purse = await thingg(list[i])
            if 'B' in purse:
                embed.add_field(name=f"``{list[i]}`` purse: \n {purse}", value='', inline=False)
            else:
                embed.add_field(name=f"``{list[i]}`` purse: \n {purse}", value='', inline=False)
        channel = bot.get_channel(data['bot']['channel'])
        embed1 = await process_status(channel)
        message = await channel.send(embeds=[embed, embed1])
        message_id = message.id
        print(message_id)
        return

async def update_message():
    channel = bot.get_channel(data['bot']['channel'])
    try:
        message = await channel.fetch_message(message_id)
        embed = discord.Embed(
            title='Account Purse:',
            description='',
            color=0x1D0FC7,
        )
        list = data['igns']
        for i in range(len(list)):
            purse = await thingg(list[i])
            if 'B' in purse:
                embed.add_field(name=f"``{list[i]}`` purse: \n {purse}", value='', inline=False)
            else:
                embed.add_field(name=f"``{list[i]}`` purse: \n{purse}", value='', inline=False)
        embed1 = await process_status(channel)
        await message.edit(embeds=[embed,embed1])
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
