# EchoBot, made by gabry9110
# bot.py: handles discord bot

import discord
import responses  # responses.py


async def send_message(message: discord.Message, is_private):
    try:
        response = await responses.handle_response(message=message)  # Calls responses.py

        if response and is_private:  # Checks if the response is empty and if the user wants the message to be sent in DM
            if isinstance(response, str):  # Check if response type is embed or string and sets parameters accordingly
                await message.author.send(response)
            elif isinstance(response, discord.Embed):
                await message.author.send(embed=response)
        elif response:  # If response is empty, don't do anything
            if isinstance(response, str):
                await message.channel.send(response)
            elif isinstance(response, discord.Embed):
                await message.channel.send(embed=response)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = "INSERT TOKEN"
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    activity = discord.Activity(name="\\help", type=discord.ActivityType.listening)
    client = discord.Client(activity=activity, intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_guild_join(guild: discord.Guild):
        channel = discord.utils.get(guild.text_channels, name='general')

        if channel:  # Try to send a welcome message in #general chat
            welcome_message = "Hello everyone, I am EchoBot, type the `\\help` command to see what I can do! 👋"
            await channel.send(welcome_message)

        else:
            # If no #general channel was found, try to send the message in the first available text channel
            text_channels = guild.text_channels
            if text_channels:
                first_text_channel = text_channels[0]
                welcome_message = "Hello everyone, I am EchoBot, type the `\\help` command to see what I can do! 👋"
                await first_text_channel.send(welcome_message)

        print(f"Joined {guild.name} {guild.id}")

    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return

        try:
            if message.content[0] == "\\":
                print(f"\"{message.content}\" command ran in the \"{message.channel}\" channel of the \"{message.guild}\" server by {message.author}")
                await send_message(message, is_private=False)

            elif message.content[0] == "_":
                print(f"\"{message.content}\" command ran in the \"{message.channel}\" channel of the \"{message.guild}\" server by {message.author}")
                await send_message(message, is_private=True)
        except IndexError:
            pass

    client.run(TOKEN)


if __name__ == '__main__':
    print("This is not the main.py file, run the bot using that instead.")
