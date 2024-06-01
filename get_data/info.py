import asyncio
from get_data.minecraft import get_username_info
from get_data.minecraft import get_shiiyu_info
from get_data.values import representTBMK
from get_data.minecraft import resolve_biggest_profile
from get_data.minecraft import updated_api
import time
import json

with open('config.json', 'r') as file:
    data = json.load(file)


async def thingg(username):
    await updated_api(username)
    list = data['igns']
    if username == list[-1]:
        time.sleep(5)
        username_info = await get_username_info(username)
        print(username_info)
        shiiyu_info = await get_shiiyu_info(username_info['id'])
        zamn = await resolve_biggest_profile(shiiyu_info)
        purse = shiiyu_info["profiles"][zamn]["data"]["networth"]["purse"]
        level = shiiyu_info['profiles'][zamn]['data']['skyblock_level']['level']
        if 'MVP' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'MVP+'
        elif 'MVP' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' not in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'MVP'
        elif 'VIP+' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'VIP+'
        elif 'VIP' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' not in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'VIP'
        else:
            rank = 'NON'
        aaa = (representTBMK(purse))
    else:
        username_info = await get_username_info(username)
        shiiyu_info = await get_shiiyu_info(username_info['id'])
        zamn = await resolve_biggest_profile(shiiyu_info)
        purse = shiiyu_info["profiles"][zamn]["data"]["networth"]["purse"]
        level = shiiyu_info['profiles'][zamn]['data']['skyblock_level']['level']
        if 'MVP' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'MVP+'
        elif 'MVP' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' not in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'MVP'
        elif 'VIP+' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'VIP+'
        elif 'VIP' in shiiyu_info['profiles'][zamn]['data']['rank_prefix'] and 'rank-plus' not in shiiyu_info['profiles'][zamn]['data']['rank_prefix']:
            rank = 'VIP'
        else:
            rank = 'NON'
        aaa = (representTBMK(purse))

        
    return aaa, level, rank