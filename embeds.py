# EchoBot, made by gabry9110
# embeds.py: returns embeds asked by responses.py

import discord


def testEmbed(author: discord.User | discord.Member):  # Only used as reference
    name = author.display_name
    pfp = author.display_avatar
    embed = discord.Embed(title="Initialisation title", description="Initialisation description",
                          color=discord.Color.blurple())
    embed.set_author(name=f"Author name {name}", url="https://youtu.be/dQw4w9WgXcQ",
                     icon_url="https://static.wikia.nocookie.net/omori/images/9/99/Basil_%28Neutral%29.gif")
    embed.set_thumbnail(url=str(pfp))
    embed.add_field(name="Field name (inline=True)", value="Field value", inline=True)
    embed.add_field(name="Field name (inline=False)", value="Field value", inline=False)
    embed.set_footer(text="Footer")
    return embed


def hello(message: discord.Message):  # \hello command
    author = message.author
    embed = discord.Embed(title="User info", color=author.accent_color)
    embed.set_thumbnail(url=str(author.display_avatar))
    embed.add_field(name="Username", value=f"`{str(author)}`", inline=True)
    embed.add_field(name="User ID", value=f"`{author.id}`", inline=True)
    embed.add_field(name="Display name/Server Nickname", value=f"`{author.display_name}`", inline=True)
    if isinstance(author, discord.Member):
        embed.add_field(name="Command sent in", value=f"{message.guild}, {message.channel}", inline=True)
        embed.add_field(name="Joined this server on (YY-MM-DD HH-MM-SS-MS)", value=f"`{author.joined_at}`", inline=False)
    else:
        embed.add_field(name="Command sent in", value="`DM`", inline=True)
    embed.add_field(name="Account created on (YY-MM-DD HH-MM-SS-MS)", value=f"`{author.created_at}`", inline=False)
    embed.set_footer(text="Rude of me not to say hello back...👋")
    return embed


def ip_address(ip):  # \ip command
    connection = ip.get("connection", {})
    timezone = ip.get("timezone", {})
    flag = ip.get("flag", {})
    flag = flag.get("emoji")
    embed = discord.Embed(title="IP info 🌐🆔", color=discord.Color.dark_gold())
    embed.add_field(name="IP Address", value=ip.get("ip", "N/A"), inline=True)
    embed.add_field(name="IP Type", value=ip.get("type", "N/A"), inline=True)
    embed.add_field(name="Continent", value=ip.get("continent", "N/A"), inline=True)
    embed.add_field(name="Country", value=ip.get("country", "N/A") + " " + flag, inline=True)
    embed.add_field(name="Region", value=ip.get("region", "N/A"), inline=True)
    embed.add_field(name="City", value=ip.get("city", "N/A"), inline=True)
    embed.add_field(name="Latitude", value=ip.get("latitude", "N/A"), inline=True)
    embed.add_field(name="Longitude", value=ip.get("longitude", "N/A"), inline=True)
    embed.add_field(name="ZIP Code/Postal Code", value=ip.get("postal", "N/A"), inline=True)
    embed.add_field(name="Timezone", value=timezone.get("abbr", "N/A"), inline=True)
    embed.add_field(name="Time zone UTC", value=timezone.get("utc", "N/A"), inline=True)
    embed.add_field(name="Date and time in IP's timezone", value=timezone.get("current_time", "N/A"), inline=True)
    embed.add_field(name="ISP", value=connection.get("isp", "N/A"), inline=True)
    embed.set_footer(text="Latitude and Longitude data is usually not 100% accurate")
    return embed


if __name__ == '__main__':
    print("This is not the main.py file, run the bot using that instead.")
