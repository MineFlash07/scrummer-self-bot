import discord
import json
import asyncio
from random import randrange


client = discord.Client()
config = {
    "token": "",
    "emoji": "scrummermoustache",
    "target_server_id": 0,
    "mindelay": 0,
    "maxdelay": 10000
}


def main():
    global config
    try:
        with open("settings.json") as file:
            loaded_config = json.load(file)
    except FileNotFoundError:
        print("Settings file doesn't exist")
        write_file(config)
        return
    for key in config.keys():
        if key in loaded_config:
            continue
        print(f"Settings {key} doesn't exist")
        loaded_config[key] = config[key]
        write_file(loaded_config)
        return
    config = loaded_config
    client.run(config["token"], bot=False)


def write_file(file_data):
    with open("settings.json", "w") as file_out:
        file_out.write(json.dumps(file_data, indent=4))


@client.event
async def on_ready():
    print("Bot stated")


@client.event
async def on_message(message: discord.Message):
    if message.guild is None:
        return
    if message.guild.id != config["target_server_id"]:
        return
    if client.user == message.author:
        return
    emoji_name = config["emoji"]
    if f":{emoji_name}:" not in message.content:
        return

    await asyncio.sleep(randrange(config["mindelay"], config["maxdelay"]))

    for emoji in message.guild.emojis:
        if emoji.name == emoji_name:
            await message.add_reaction(emoji)
            break


if __name__ == "__main__":
    main()
