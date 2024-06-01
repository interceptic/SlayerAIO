# Binmaster Controller
THIS ONLY WORKS FOR THE SLAYER MACRO
DO NOT DELETE THE CONFIG.JSON FILE IN THE SLAYER FOLDER

# Startup
- Download this from github and open the directory called Slayer (type git clone this repository if on virtual server, you may need to type apt install git)
- Download the Binmaster loader for the system youre using (windows/macos/linux)
- Put the binmaster files into the Slayer directory

# Configuration
- Open the config.json file in the Binmaster_Controller directory.
- ``igns`` is your minecraft slayer account, if you have multiple, seperate each one with a comma (for example, "SamMaybe", "Interceptic" - The last should not have a comma)
- ``webhooks`` is your discord webhook, if you dont know how to make a webhook, go [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) if you have multiple, seperate each one with a comma (for example, "webhook1", "webhook2" - The last should not have a comma)
- ``keys`` put in your binmaster key here. if you have multiple, seperate each one with a comma (for example, "key1", "key2" - The last should not have a comma)
- ``ports`` put your binmaster webpage ports here, this should be an integer (for example, 6969 - not "6969") if you have multiple, seperate each one with a comma (for example, 420, 6969 - The last should not have a comma)
- ``operating_system`` pick your operating system, either linux, macos, or windows.
- ``restart_time`` this is how long your bot will run, if you have this at 30 minutes, the bot will run for 30 minutes.
- ``off_time`` this is how long your bot will take a break for after restart time, it will then start again with the normal restart time
- ``token`` your discord bot token, enable intents.
- ``channel`` a discord channel for sending updates, such as status of your accounts, and their purse, you need to do the /stats command for this to start
- ``your_id`` this will let only you use the commands for your bot
The rest is self explanatory.

Enjoy :)
(code may or may not be updated) 30% of credit goes to chat gpt
