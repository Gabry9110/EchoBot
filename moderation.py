# EchoBot, made by gabry9110
# moderation.py: Handles moderator functions (e.g., ban users, kick users...)

import discord


async def ban(command: discord.Message) -> str:
    _, username = command.content.split()
    guild = command.guild

    try:
        if username.startswith("<@") & username.endswith(">"):  # Check if user to ban is specified as ping or ID
            # Pings actually return an ID (<@397362462380261376> is a ping, 397362462380261376 is an ID)
            discord_id = username[2:-1]
        else:
            discord_id = int(username)  # In case the user just bans an ID and not a ping
        user = discord.Object(int(discord_id))  # Check if ID is correct and throw ValueError if it isn't
    except ValueError:
        return "Invalid ID or ping"

    print(f"Banning {discord_id} from {guild.name}")
    perms = command.author.guild_permissions
    try:
        if perms.ban_members:
            await discord.Guild.ban(self=guild, user=user)
            print("Banned " + username)
            return "Banned " + username
        else:
            return "Error: You don't have the `ban_members` permission"
    except discord.NotFound:
        print("User not found")
        return "User not found"
    except discord.Forbidden:
        print("Forbidden")
        return "Forbidden (most likely an issue with my permissions)"
    except Exception as e:
        print(e)


async def unban(command: discord.Message) -> str:
    _, username = command.content.split()
    guild = command.guild

    try:
        if username.startswith("<@") & username.endswith(">"):
            discord_id = username[2:-1]
        else:
            discord_id = int(username)  # If the user just bans

        user = discord.Object(int(discord_id))
    except ValueError:
        return "Invalid ID or ping"

    print(f"Unbanning {discord_id} from {guild.name}")
    perms = command.author.guild_permissions
    try:
        if perms.ban_members:
            await discord.Guild.unban(self=guild, user=user)
            return f"Unbanned {username} (remember that they need an invite to join back here)"
        else:
            return "Error: You don't have the `ban_members` permission"
    except discord.NotFound:
        return "User not found"
    except discord.Forbidden:
        return "Forbidden (most likely an issue with my permissions)"
    except Exception as e:
        print(e)
        return "Syntax error"


async def kick(command: discord.Message) -> str:
    _, username = command.content.split()
    guild = command.guild

    try:
        if username.startswith("<@") & username.endswith(">"):
            discord_id = username[2:-1]
        else:
            discord_id = int(username)
        user = discord.Object(int(discord_id))
    except ValueError:
        return "Invalid ID or ping"

    print(f"Kicking {discord_id} from {guild.name}")
    perms = command.author.guild_permissions
    try:
        if perms.kick_members:
            await discord.Guild.kick(self=guild, user=user)
            return "Kicked " + username
        else:
            return "Error: You don't have the `kick_members` permission"
    except discord.NotFound:
        return "User not found"
    except discord.Forbidden:
        return "Forbidden (most likely an issue with my permissions)"
    except Exception as e:
        print(e)
        return "Syntax error"

