from django.core.management.base import BaseCommand
import discord
from discord.ext import commands
from datacenter.models import DiscordUser
from bot.settings import TOKEN, ADMIN_ROLE, MUTE_ROLE, SERVER_ID, USER_ID, SERVER_ADDRESS
import asyncio
from django.utils import timezone
import mcstatus

class Command(BaseCommand):
    help = 'Telegram bot'


    def handle(self, *args, **options):
        print('Start')
        bot1()


def bot1():

    # aicheck = aioify(check)
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    bot.remove_command('help')
    
    def check():
        users = []
        guild = bot.get_guild(int(SERVER_ID))

        for i in DiscordUser.objects.all():
            users.append(i.nick_name)
        for author in guild.members:
            if author.name != 'Ботяня':
                if str(author) not in users:
                    user = DiscordUser.objects.create(nick_name=author, karma=0)

    def del_user(member):
        user = DiscordUser.objects.get(nick_name=str(member))
        user.delete()


    def add_carma(member):
        user = DiscordUser.objects.get(nick_name=str(member))
        if (timezone.now().day - user.last_karma.day) > 0 or (timezone.now().hour - user.last_karma.hour) > 0 or (timezone.now().minute - int(user.last_karma.minute)) > 0:
            user.karma += 1
            user.last_karma = timezone.now()
            user.save()
            return user.karma
        else:
            return False


    def minus_karma(member, count):
        user = DiscordUser.objects.get(nick_name=str(member))
        user.karma -= count
        user.save()
        return user.karma
    
    def my_carma_2(member):
        user = DiscordUser.objects.get(nick_name=str(member))
        return user.karma


    @bot.event
    async def on_ready():
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, check)

    @bot.event
    async def on_member_join(member):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, check)
        guild = bot.get_guild(int(SERVER_ID))
        user = guild.get_member(member.id)
        user_role = guild.get_role(USER_ID)
        await user.add_roles(user_role)

    @bot.command()
    async def help(ctx, mes='everyone'):
        if mes == 'everyone':
            text = '''
    ***For everyone***
!help - помощь
!carma - Узнать свою карму
!thanks <user> - Сказать спасибо участнику и повысить его карму
!server - информауия о сервере
'''
            await ctx.reply(text)
        elif mes == 'moder':
            text = '''
    ***Moderator only***
!ban <user> <reason> - забанить участника
!kick <user> <reason> - кикнуть участника
!mute <user> <reason> - замутить участника
!unmute <user> <reason> - размутить участника
!warn <user> <reason> <count> - выдать предупреждение пользователю
'''
            await ctx.reply(text)
        elif mes == 'all':
            text = '''
    ***For everyone***
!help - помощь
!carma - Узнать свою карму
!thanks <user> - Сказать спасибо участнику и повысить его карму
!server - информауия о сервере


***Moderator only***
!ban <user> <reason> - забанить участника
!kick <user> <reason> - кикнуть участника
!mute <user> <reason> - замутить участника
!unmute <user> <reason> - размутить участника
!warn <user> <reason> <count> - выдать предупреждение пользователю
'''
            await ctx.reply(text)



    @bot.command(name='echo')
    async def start(message):
        loop = asyncio.get_running_loop()
        author = message.message.author
        await loop.run_in_executor(None, check)

        await message.reply(f'Hello, {author.name}')


    @bot.command()
    async def mute(ctx, user: discord.Member = None, *, reason='По приколу:)'):
        if user is None:
            await ctx.reply('И кого мне мутить? Укажи пользователя')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
                role = guild.get_role(int(MUTE_ROLE)) # получаем объект роли*
                await user.add_roles(role, reason=reason)
                await user.edit(mute=True)
                await ctx.reply(f'{user.name} был заткнут {author.name} на сервере по причине: {reason}')
                await user.send(f'Тебя замутил {author.name} на сервере "{guild.name}" по причине: {reason}')
            else:
                await ctx.reply(f'Ты не модератор! У тебя нет права на лево:)')


    @bot.command()
    async def unmute(ctx, user: discord.Member = None):
        if user is None:
            await ctx.reply('И кого мне отмучивать? Укажи пользователя')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
                role = guild.get_role(int(MUTE_ROLE)) # получаем объект роли*
                user_roles = [i.id for i in user.roles]
                if int(MUTE_ROLE) in user_roles:
                    await user.remove_roles(role)
                    await user.edit(mute=False)
                    await ctx.reply(f'{user.name} был отткнут {author.name} на сервере:) Поздравляю, {user.name}:)')
                    await user.send(f'Поздравляю! Ты можешь говорить на сервере {guild.name}! Но больше не шали:)')
                else:
                    await ctx.reply(f'{user.name} не заткнут! Но я могу устроить:)')
            else:
                await ctx.reply(f'Ты не модератор! У тебя нет права на лево:)')

    @bot.command()
    async def warn(ctx, user: discord.Member = None, reason='По приколу:)', count=5):
        if user is None:
            await ctx.reply('Я не обладаю даром телепатии:) Кого ругать?')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
                loop = asyncio.get_running_loop()
                new_carma = await loop.run_in_executor(None, minus_karma, user, count)
                await user.send(f'Тебя поругал {author.name} на сервере {guild.name} по причине: {reason}. Твоя карма уменьшилась на {count} и теперь составляет {new_carma}. Больше не шали:)')
                await ctx.reply(f'{user.name} предупреждён! Теперь его карма составляет {new_carma}.')
            else:
                await ctx.reply(f'Ты не модератор! У тебя нет права на лево:)')
    

    @bot.command()
    async def carma(ctx):
        author = ctx.message.author
        loop = asyncio.get_running_loop()
        carma = await loop.run_in_executor(None, my_carma_2, author)
        await ctx.reply(f'Эй! Твоя карма составляет {carma}!')


    @bot.command()
    async def kick(ctx, user: discord.Member = None, *, reason='Админ рулит'):
        if user is None:
            await ctx.reply('И кого мне кикать? Укажи пользователя')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, del_user, user)
                await user.send(f'Тебя кикнул {author.name} с сервера "{guild.name}" по причине: {reason}')
                await user.kick(reason=reason)
                await ctx.reply(f'{user.name} был кикнут с сервера по причине: {reason}')
            else:
                await ctx.reply(f'Ты не модератор! У тебя нет права на лево:)')


    @bot.command()
    async def ban(ctx, user: discord.Member = None, *, reason='Админ рулит'):
        if user is None:
            await ctx.reply('И кого мне банить? Укажи пользователя')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, del_user, user)
                await user.send(f'Тебя забанил {author.name} на сервере "{guild.name}" по причине: {reason}')
                await user.ban(reason=reason)
                await ctx.reply(f'{user.name} был забанен на сервере по причине: {reason}')
            else:
                await ctx.reply(f'Вы не модератор! У Вас нет права на лево:)')

    
    @bot.command()
    async def thanks(ctx, user: discord.Member = None):
        if user is None:
            await ctx.reply('И кому говорить спасибо?')
        else:
            author = ctx.message.author
            if user == author:
                await ctx.reply('Сам себя не похвалишь, никто не похвалит:)')
            else:
                loop = asyncio.get_running_loop()
                new_carma = await loop.run_in_executor(None, add_carma, user)
                if new_carma == False:
                    await ctx.reply(f'Я не могу так часто благодарить {user.name}! Давай попозже:)')
                else:
                    await user.send(f'Тебе сказал спасибо {author.name}! Теперь твоя карма {new_carma}')
                    await ctx.reply(f'Ладно, я повышу карму {user.name}:) Теперь его карма {new_carma}!')


    @bot.command()
    async def server(ctx):
        server = mcstatus.JavaServer.lookup(SERVER_ADDRESS)
        status = server.status()
        count_players = "Количество игроков: {}/{}".format(status.players.online, status.players.max)
        users = [i.name for i in status.players.sample]
        all_players = f'Игроки на сервере: {", ".join(users)}'
        await ctx.reply(f'Вот текущее положение сервера:\nВерсия: {status.version.name}\n{count_players}\n{all_players}')


    @bot.command()
    async def tell_moder(ctx, message='', user: discord.Member = None):
        author = ctx.message.author
        if message == '':
            await ctx.reply('Ты не написал, что нужно передать!')
        else:
            if user is None:
                moders = []
                guild = bot.get_guild(int(SERVER_ID))
                role = guild.get_role(ADMIN_ROLE)
                moders = role.members
                print(moders)
            else:
                user_roles = [i.id for i in user.roles]
                if ADMIN_ROLE in user_roles:
                    await user.send(f'{')


    @bot.command()
    async def gay(ctx):
        await ctx.send('Гоша гей:)')


    bot.run(TOKEN)



# from mcstatus import MinecraftServer

# # адрес сервера в формате "IP:порт"

# server_address = "127.0.0.1:25565"

# # создаем объект сервера

# server = MinecraftServer.lookup(server_address)

# # получаем объект статуса сервера

# status = server.status()

# # получаем информацию о сервере

# print("Протокол: {}".format(status.version.protocol))

# print("Ядро: {}".format(status.version.name))

# print("Количество игроков: {}/{}".format(status.players.online, status.players.max))

