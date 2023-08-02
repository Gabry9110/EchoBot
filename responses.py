# EchoBot, made by gabry9110
# responses.py: returns responses asked by bot.py


# Discord text formatting cheatsheet:
# `monospaced/code text`
# **text in bold**
# ~~text crossed out~~
# *text in italic*
# <URLs without embeds>
# ||Text sent as spoiler|| (covered until you click it)
# # Text written bigger and in bold
# <@397362462380261376> User ping

import discord
import requests
from random import randint
import embeds  # embeds.py
import moderation  # moderation.py


help_msg = """
# EchoBot Help 🆘❓
**Add a prefix to the following commands to run them**
Use `\\` to get the response sent in the same channel or `_` to get the response sent in DM
# Commands:
**Fun and Miscellaneous:**
👋🫡 `hello` -> Say hello to the user
🆘❓ `help` -> List all commands *(The command you ran right now!)*
😸😺 `cat` -> Send an image of a cat using `thecatapi.com`
▶️♻️ `repeat {text}` -> Repeats given text *(Cannot repeat pings like @‎everyone or @‎member)*
😂⚫ `joke` -> Send a joke using `jokeapi.dev` *(⚠️ May contain inappropriate/dark jokes, read here for more information <https://jokeapi.dev/#safe-mode> ⚠️)*
😂🟢 `pcjoke` -> Send politically correct jokes using `jokeapi.dev` *(⚠️ May still contain inappropriate/dark jokes, read here for more information <https://jokeapi.dev/#safe-mode> ⚠️)*
😂🧑‍💻 `programmingjoke` -> Send a joke for programmers using `jokeapi.dev`
🌐🆔 `ip {IPv4/IPv6 address or domain}` -> Get info about an IP address or domain (using the "ipwhois.io" API)

**Random and Math:**
🎰🔢 `roll {n1} {n2}` -> Generate a random number between n1 and n2
🎲❓ `dice` -> Roll a dice
🪙❓`coinflip` -> Flip a coin
💸🈹 `sale {percentage} {price}` -> Calculate a discounted price with discount percentage and full price
🔢➡️ `baseconvert {number} {base1} {base2}` -> Convert number from base1 to base2 (e.g., binary to hex)

**Server Management (Moderator Stuff):**
❎ `kick {user}` -> Kick the specified user from the server *(Note: you need the `kick_members` permission)*
⛔ `ban {user}` -> Ban the specified user from the server *(Note: you need the `ban_members` permission)*
✅ `unban {user}️` -> Unban the specified banned user from the server *(Note: you need the `ban_members` permission)*


*EchoBot is written by @gabry9110, have fun 🎉*
"""  # TODO: Update list for each command added


def roll(command):
    try:
        _, n1, n2 = command.split()
        n1 = int(n1)
        n2 = int(n2)
        result = str(randint(n1, n2))
        print("Rolled " + result)
        return result
    except ValueError:
        return "Error: Wrong input"


def sale(command):
    try:
        _, percentage, price = command.split()
        percentage = float(percentage)

        if not (0 <= percentage <= 100):  # Discount percentage obviously has to be 0-100%
            raise ValueError

        price = float(price)
        discounted_price = price - (price * (percentage / 100))
        return str(discounted_price)

    except ValueError:
        return "Syntax error (make sure you're writing numbers without % or currency signs and that the discount " \
               "percentage is between 0 and 100)"


def check_ip(ip) -> str | discord.Embed:
    print(ip)
    url = f"http://ipwho.is/{ip}"
    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        data = response.json()
        print(data)
        success = data.get("success", "N/A")  # This api has a variable that checks if the request was successful
        message = data.get("message", "N/A")  # We also have a message variable if the request was not successful
        if success:
            print(success)
            return embeds.ip_address(data)
        elif message == "Invalid IP address":
            return "Invalid IP address"
        else:
            print(success)
            return "Failed to get IP info"
    else:
        return f"Error {response.status_code} (not your fault)"


def cat():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        content = response.json()
        print(content[0].get("id"))
        return content[0].get("url", "Couldn't get cat (not your fault)")
        # dict.get() function returns second parameter if the first one doesn't exist in the dict


def joke(message):
    if message == "joke":
        response = requests.get("https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun")
    elif message == "pcjoke":
        response = requests.get("https://v2.jokeapi.dev/joke/Miscellaneous,Pun?safe-mode")
    elif message == "programmingjoke":
        response = requests.get("https://v2.jokeapi.dev/joke/Programming")
    else:
        return "Couldn't get joke (not your fault)"  # Function not meant to be called in this case

    print(response.status_code)
    if response.status_code == 200:
        content = response.json()
        print(content)
        if content.get("error"):
            return "Couldn't get joke (not your fault)"
        if content.get("type") == "twopart":
            return content.get("setup") + "\n||" + content.get("delivery") + "||"  # Final part of joke gets sent as spoiler
        else:
            return content.get("joke")
    else:
        return "Couldn't get joke (not your fault)"


def base_conversion(number, from_base, to_base):
    # If user enters e.g. "bin" or "hex" instead of 2 or 16, automatically convert it to the proper int base
    base_mapping = {
        "bin": 2,
        "oct": 8,
        "dec": 10,
        "hex": 16
    }
    from_base = base_mapping[from_base]
    to_base = base_mapping[to_base]

    def to_base_10(num, base):
        result = 0
        power = 0
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for digit in reversed(str(num)):
            value = digits.index(digit)
            result += value * (base ** power)
            power += 1

        return result

    def from_base_10(num, base):
        result = ""
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        while num > 0:
            digit = digits[num % base]
            result = digit + result
            num //= base

        return result

    if from_base | to_base > 36:
        return "Base can't be higher than 36"

    base_10_number = to_base_10(number, from_base)

    converted_number = from_base_10(base_10_number, to_base)

    return converted_number


async def handle_response(message: discord.Message) -> str | discord.Embed:
    command = str(message.content.lower())
    command = command[1:]

    if command == "hello":  # Says hello to the user
        return embeds.hello(message)

    elif command == "ping":
        return "Pong!"

    elif command.startswith("roll"):  # Random Number Generator
        return "🎰 " + roll(command)

    elif command == "dice":  # Dice Roll
        return "🎲 " + str(randint(1, 6))

    elif command == "coinflip":  # Coin Flip
        flip = "🪙 Heads!" if randint(1, 2) == 1 else "🪙 Tails!"
        print(flip)
        return flip

    elif command == "help":  # Display every command
        return help_msg

    elif command.startswith("sale"):  # Calculates sale having price and discount %
        return sale(command)

    elif command.startswith("ban"):  # Bans a server member, needs ban_members permission
        if str(message.channel).startswith("Direct Message"):
            print("Command not available in DM")
            return "Command not available in DM"
        else:
            return await moderation.ban(message)

    elif command.startswith("kick"):  # Kicks a server member, needs kick_members permission
        if str(message.channel).startswith("Direct Message"):
            print("Command not available in DM")
            return "Command not available in DM"
        else:
            return await moderation.kick(message)

    elif command.startswith("unban"):
        return await moderation.unban(message)

    elif command.startswith("repeat"):
        command = command[6:]
        if command.find("<@") != -1:
            return "I can't repeat pings!"
        if command.find("@everyone") != -1:
            return "I can't ping @‎everyone!"
        if command.find("@here") != -1:
            return "I can't ping @‎here!"
        return command

    elif command == "cat":
        return cat()

    elif command.startswith("ip"):
        return check_ip(message.content[4:])

    elif (command == "joke") | (command == "pcjoke") | (command == "programmingjoke"):
        return joke(command)

    elif command.startswith("baseconvert"):
        _, number, base_a, base_b = command.split()  # Number to convert, number's base, base to convert number to
        return base_conversion(number, base_a, base_b)

    else:  # If command does not exist, return an empty response
        print("Not a command")
        return ""

    # TODO: implement more moderation (unban, temp ban, usercheck, mute, lock channel, vc) and color pick commands


if __name__ == '__main__':
    print("This is not the main.py file, run the bot using that instead.")
