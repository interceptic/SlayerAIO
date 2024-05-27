import aiohttp


async def updated_api(username):
    try:
        async with aiohttp.ClientSession() as shiyu:
            async with shiyu.get(f'https://sky.shiiyu.moe/stats/{username}/') as abcd:
                s
    except Exception as e:
         return e
    
async def get_username_info(username):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return await response.json()

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

async def get_shiiyu_info(uuid):
    TIMEOUT = 30
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://sky.shiiyu.moe/api/v2/profile/{uuid}", timeout=TIMEOUT) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except aiohttp.ClientError as e:
        # Log or print the specific error
        print(f"Error fetching Shiiyu info: {e}")
        return None
    

async def resolve_biggest_profile(shiiyu_info: dict):
	"""
	Returns the profile ID of the profile with the highest net-worth, given a user's shiiyu_info
	"""
	biggest_profile_id = 0
	biggest_profile_networth = 0

	for profile_id in shiiyu_info["profiles"]:
		if shiiyu_info["profiles"][profile_id]["data"]["networth"]["networth"] > biggest_profile_networth:
			biggest_profile_networth = shiiyu_info["profiles"][profile_id]["data"]["networth"]["networth"]
			biggest_profile_id = shiiyu_info["profiles"][profile_id]["profile_id"]

	return biggest_profile_id

    