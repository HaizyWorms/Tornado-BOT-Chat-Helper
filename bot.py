import discord
import random
from discord import Game
import asyncio
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions 
from discord import utils
from discord.ext import commands

import config

client = commands.Bot(command_prefix="t!", intents=discord.Intents.all())  # Префикс бота
client.remove_command("help") # Удаление стандарт Хелп


# Надпись при включении бота
@client.event
async def on_ready():
    print("Бот готов к работе!")

    # Активность бота
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game("Помощь: t!help")
    )


# Бан пользователя
@client.command(pass_context=True, name="ban")
@commands.has_permissions( administrator = True )
async def ban(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("[ОШИБКА!] Укажите пользователя")
    await member.ban()
    message: Discord.Message = await ctx.send(f"Пользователь {member} успешно забанен!")
    await message.add_reaction("✔️")


# Исключение пользователя
@commands.has_permissions( administrator = True )
@client.command(pass_context=True, name="kick")
async def kick(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("[ОШИБКА!] Укажите пользователя")
    await member.kick()
    message: Discord.Message = await ctx.send(f"Пользователь {member} успешно кикнут!")
    await message.add_reaction("✔️")


# Мут пользователя
@client.command(pass_context=True, name="mute")
@commands.has_permissions( administrator = True )
async def mute(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("[ОШИБКА!] Проверьте правильность написания команды!")
    role = discord.utils.get(ctx.guild.roles, id=1113127519634342064)
    await member.add_roles(role)
    message: Discord.Message = await ctx.send(f"Пользователь {member} успешно замучен!")
    await message.add_reaction("✔️")


# Очистка чата
@client.command()
@commands.has_permissions( administrator = True )
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    message: Discord.Message = await ctx.send(f"Сообщения успешно удалены!")
    await message.add_reaction("✔️")


# Сказать от имени бота
@client.command(pass_context=True, name="say")
@commands.has_permissions( administrator = True )
async def say(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()


# RUN
client.run(config.TOKEN)
