import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix="t!", intents=discord.Intents.all())  # Префикс бота
bot.remove_command("help")  # Удаление ds хелп

# logs
async def log_action(action, moderator, target):
    guild = moderator.guild
    log_channel = guild.get_channel(config.LOG_CHANNEL_ID)
    if log_channel is not None:
        await log_channel.send(f'Администратор {moderator} выполнил {action} над {target}')
    else:
        print("Ошибка: Канал логирования не найден!")

# запретки
forbidden_words = ["test2", "test1", "test"]  

# help
@bot.command()
async def help(ctx):
    await ctx.send('Вызвать данное меню - t!help.')
    await ctx.send('Список доступных команд для модерации: t!mute , t!kick , t!ban , t!clear')
    await ctx.send('Список доступных команд для развлечения: t!say')

# tech_on
@bot.event
async def on_ready():
    print("Бот готов к работе!")
    # Активность
    await bot.change_presence(
        status=discord.Status.idle, activity=discord.Game("Помощь: t!help")
    )

# ban
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("[ОШИБКА!] Укажите пользователя")
    await member.ban()
    await log_action('Бан', ctx.author, member)
    message = await ctx.send(f"Пользователь {member} успешно забанен!")
    await message.add_reaction("✔️")

# kick
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("[ОШИБКА!] Укажите пользователя")
    await member.kick()
    await log_action('Кик', ctx.author, member)
    message = await ctx.send(f"Пользователь {member} успешно кикнут!")
    await message.add_reaction("✔️")

# say
@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()
    await log_action('Команда say', ctx.author, ctx.channel)

# запретки
@bot.event
async def on_message(message):
    # Проверка, отправлено ли сообщение в канал и не является ли оно сообщением бота
    if message.guild is not None and message.author != bot.user:
        # Проверка запреток
        for word in forbidden_words:
            if word in message.content.lower():
                # Удаление сообщения
                await message.delete()
                # Оповещение об удалении сообщения
                await message.channel.send(f"{message.author.mention}, в вашем сообщении содержится запрещенное слово, настоятельно рекомендуем ознакомиться с правилами сервера и впредь не нарушать!")
                break  # Выход из цикла после удаления сообщения
    await bot.process_commands(message)  # Обработка команд

# RUN
bot.run(config.TOKEN)
