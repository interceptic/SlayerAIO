import subprocess
import asyncio
import json
import os
import signal
import discord
import datetime
import requests
import re
dropped_eyes = {}
dropped_eyes_hourly = {}
dictionary = {}
on_off = {}
async_tasks = {}
current_users = {}
startall_tasks = {}
with open("config.json") as cd:
    data = json.load(cd)
le_status = None

for i in data['igns']:
    dropped_eyes[f'{i}'] = 0
    dropped_eyes_hourly[f'{i}'] = 0


async def process_handler(username, on):
    global le_status
    global enabled
    enabled = on
    while True:    
        print(data['configuration']['monitor_output_manually'], data['binmaster']['operating_system'])
        
        le_status = None
        ign = username
        with open("Slayer/config.json") as conf:
            config = json.load(conf)
        position = data['igns'].index(f'{ign}')
        config['authentication']['cache_folder'] = f"./cache/{ign}"
        config['slayer']['type'] = data['slayer']['boss'][position]
        config['slayer']['tier'] = data['slayer']['tier'][position]
        config['slayer']['farm_only'] = data['slayer']['autofarm'][position]
        config['slayer']['autoslayer'] = data['slayer']['autoslayer'][position]
        config['external_indicators']['webpage_port'] = data['binmaster']['ports'][position]
        webhook = data['webhooks'][position]
        config['external_indicators']['webhook_url'] = webhook 
        config['antistaff']['watch_hotbar_slots'] = [1, 2]
        config['utility']['proxy']['enabled'] = data['proxy']['enabled'][position]
        config['utility']['proxy']['ip']  = data['proxy']['ips'][position]
        config['utility']['proxy']['port']  = data['proxy']['ports'][position]
        config['utility']['proxy']['username']= data['proxy']['usernames'][position]
        config['utility']['proxy']['password']= data['proxy']['passwords'][position]
        if enabled == True:    
            with open("Slayer/config.json", "w") as dumps:
                json.dump(config, dumps, indent=4)
            if data['configuration']['monitor_output_manually'] is False:
                if data['binmaster']['operating_system'].lower() == 'windows':
                    slayer_dir = os.path.join(os.path.dirname(__file__), 'Slayer')
                    exe_path = os.path.join(slayer_dir, 'binmaster-slayer-win.exe') 
                    try:
                        process = subprocess.Popen([exe_path], cwd=slayer_dir, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, 
                    tdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    stdin=subprocess.PIPE, 
                    text=True,)
                    except Exception as e:
                        print(e)
                    
                else:
                    process = subprocess.Popen([f"./binmaster-slayer-{data['binmaster']['operating_system']}"], cwd='Slayer/', stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True, preexec_fn=os.setsid)
                task = asyncio.create_task(handle_output(process, ign, webhook))
                async_tasks[f'{ign}'] = task
            if data['configuration']['monitor_output_manually'] is True:
                if data['binmaster']['operating_system'].lower() == 'windows':
                    slayer_dir = os.path.join(os.path.dirname(__file__), 'Slayer')
                    exe_path = os.path.join(slayer_dir, 'binmaster-slayer-win.exe') 
                    if os.path.isfile(exe_path):
                        process = subprocess.Popen([exe_path], cwd=slayer_dir, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,)
                    else:
                        print('error not path')
                else:
                    process = subprocess.Popen([f"./binmaster-slayer-{data['binmaster']['operating_system']}"], cwd='Slayer/', preexec_fn=os.setsid)

            on_off[f'{ign}'] = True
            current_users['igns'] = []
            current_users['igns'].append(username)
            timeout = data['configuration']['restart_time']
            off_time = data['configuration']['off_time']
            dictionary[ign] = process
            embed1 = discord.Embed(
                title=f"Bot Started for {data['configuration']['restart_time']} Minutes.",
                description=f"*Bot will stop in {data['configuration']['restart_time']} minutes and take a {data['configuration']['off_time']} minute break.*",
                color=0x00F3FF
            )
            a = embed1.to_dict()
            le_json = {
                "username": "interceptic",
                "avatar_url": "https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160",
                "embeds": [a]
            }
            try: 
                response = requests.post(webhook, json=le_json)
            except Exception as e:
                print(e)
            await asyncio.sleep(timeout * 60)
            le_status = 200
            embed1 = discord.Embed(
                title=f"Bot Stopped For {data['configuration']['off_time']} Minutes.",
                description=f"*Bot will restart in {data['configuration']['off_time']} minutes from now.*",
                color=0xFF001F
            )
            a = embed1.to_dict()
            le_json = {
                "username": "interceptic",
                "avatar_url": "https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160",
                "embeds": [a]
            }
            try: 
                response = requests.post(webhook, json=le_json)
                if response.status_code == 204:
                    print("Webhook sent successfully.")
                else:
                    print(f"Failed to send webhook: {response.status_code} - {response.text}")
            except Exception as e:
                print(e)
            await(process_stopper(ign, True))
            task.cancel()
            await asyncio.sleep(off_time * 60)
            emoji = None
        elif enabled == False:
            await asyncio.sleep(5)

async def strip_ansi_codes(text):
    ansi_escape = re.compile(r'''
        \x1B              # ESC
        (?:[@-Z\\-_]      # 7-bit C1 Fe (except CSI)
        | \[ [0-?]* [ -/]* [@-~])  # or CSI ... Cmd
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)

async def process_stopper(username, on_or_off):
    process = dictionary.get(username)
    global enabled

    if process:
        try:
            if data['binmaster']['operating_system'].lower() == 'windows':
                process.terminate()
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
            task = async_tasks[f'{username}']
            task.cancel()

            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print(f"Process for {username} did not terminate within timeout, forcefully killing it.")
                if data['binmaster']['operating_system'].lower() == 'windows':
                    process.kill()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)

            while process.poll() is None:
                await asyncio.sleep(1)

            if on_or_off == True:
                pass
            elif on_or_off == False:
                enabled = False
            del dictionary[username]
            print(f"Process for {username} terminated.")
        except Exception as e:
            print(f"Error terminating process for {username}: {e}")
    else:
        print(f"No process found for {username}")

async def process_status(channel):
    with open("config.json") as conf:
        status = json.load(conf)
    accounts = status['igns']
    embed = discord.Embed(
            title='Account Status',
            description='',
            color=0x1D0FC7,
            )
    for i in range(0,len(accounts)):
        process = dictionary.get(accounts[i])
        if le_status is None:
            if process is None:
                emoji = ":red_circle:"
            else:    
                if process.poll() is None:
                    emoji = ":green_circle:"
                else:
                    emoji = ":red_circle:"
        else:
            emoji = ":yellow_circle:"
        embed.add_field(name=f"{emoji} Status of: ``{accounts[i]}``", value='', inline=False)
    return embed

async def message_handler(username, text):
    process = dictionary.get(username)
    process.stdin.write(f'chat {text}')
    process.stdin.flush()

keywords= (
    'client timed out', 
    "you haven't unlocked this fast travel destination!", 
    'limbo',
    'no path to goal', 
    'ratelimiter', 
    'uncaught exception', 
    'out of sync', 
    'possible stall', 
    'you were killed',  
    'microsoft'
)
critical_keywords = (
    'banned for',
    'phoenix',
    'hes macroing'
)

drop_keyword = 'A special Zealot has spawned nearby'


async def handle_output(process, username, webhook):
    while True:
        for line in process.stdout:
            stripped = await strip_ansi_codes(line)
            if any(keyword in stripped.lower() for keyword in keywords): 
                embed = discord.Embed(
                    title = f"{username}",
                    description = f"{stripped}",
                    color = 0xFF001F
                    )   
                value = embed.to_dict()
                le_json = {
                "username": "interceptic",
                "avatar_url": "https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160",
                "embeds": [value]
                }
                requests.post(webhook, json=le_json)
            if any(critical_keyword in line.lower() for critical_keyword in critical_keywords):
                embed = discord.Embed(
                    title = f"{username}",
                    description = f"{stripped}",
                    color = 0xFF001F
                    )   
                value = embed.to_dict()
                le_json = {
                    "username": "interceptic",
                    "avatar_url": "https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160",
                    "embeds": [value],
                    "content": f"<@{data['bot']['your_id']}>"
                    }
                requests.post(webhook, json=le_json)
            if 'A special Zealot has spawned nearby' in line:
                dropped_eyes[username] += 1
                print(dropped_eyes)
                dropped_eyes_hourly[f'{username}'] += 1
                asyncio.create_task(remove_eye(username))
            await asyncio.sleep(0.6)

async def killall():
    global enabled
    for i in data['igns']:
        task = async_tasks[f'{i}']
        task2 = startall_tasks[f'{i}']
        task.cancel()
        task2.cancel()
    user_range = len(data['igns'])
    for i in range(0, user_range):
        process = dictionary.get(data['igns'][i])
        if process:
            try:
                if data['binmaster']['operating_system'].lower() == 'windows':
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print(f"Process did not terminate within timeout, forcefully killing it.")
                    if data['binmaster']['operating_system'].lower() == 'windows':
                        process.kill()
                    else:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)

                while process.poll() is None:
                    await asyncio.sleep(1)

                enabled = False
                del dictionary[process]
                print(f"Processes terminated.")
            except Exception as e:
                print(f"Error terminating process: {e}")
        else:
            print(f"No process found")

async def startall():
    for i in data['igns']:
        task = asyncio.create_task(process_handler(i, True))
        startall_tasks[f'{i}'] = task
        await asyncio.sleep(7)


async def remove_eye(username):
    await asyncio.sleep(3600)
    dropped_eyes_hourly[f'{username}'] -= 1