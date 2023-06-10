from django.core.management.base import BaseCommand
import discord
from discord.ext import commands
from datacenter.models import DiscordUser
from bot.settings import TOKEN, ADMIN_ROLE, MUTE_ROLE, SERVER_ID


class Command(BaseCommand):
    help = 'Telegram bot'


    def handle(self, *args, **options):
        print('Start')
        bot1()


def check(author):
    users = [i.nick_name for i in DiscordUser.objects.all()]
    if author not in users:
        user = DiscordUser.objects.create(
            nick_name=author,
            karma=0
        )



def bot1():


    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    bot.remove_command('help')


    @bot.command()
    async def help(ctx):
        text = '''
***Moderator only***
!ban <user> <reason> - забанить участника
!kick <user> <reason> - кикнуть участника
!mute <user> <reason> - замутить участника
!unmute <user> <reason> - размутить участника
***For everyone***
!help - помощь
    '''
        await ctx.reply(text)



    @bot.command(name='echo')
    async def start(message):
        author = message.message.author
        check(author)

        await message.reply(f'Hello, {author.name}')


    @bot.command()
    async def mute(ctx, user: discord.Member = None, *, reason='По прколу:)'):
        if user is None:
            await ctx.reply('И кого мне мутить? Укажи пользователя')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
                role = guild.get_role(int(MUTE_ROLE)) # получаем объект роли*
                await user.add_roles(role, reason=reason)
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
                    await ctx.reply(f'{user.name} был отткнут {author.name} на сервере:) Поздравляю, {user.name}:)')
                    await user.send(f'Поздравляю! Ты можешь говорить на сервере {guild.name}! Но больше не шали:)')
                else:
                    await ctx.reply(f'{user.name} не заткнут! Но я могу устроить:)')
            else:
                await ctx.reply(f'Ты не модератор! У тебя нет права на лево:)')


    @bot.command()
    async def kick(ctx, user: discord.Member = None, *, reason='Админ рулит'):
        if user is None:
            await ctx.reply('И кого мне кикать? Укажи пользователя')
        else:
            author = ctx.message.author
            roles = [i.id for i in author.roles]
            if int(ADMIN_ROLE) in roles:
                guild = bot.get_guild(int(SERVER_ID)) # получаем объект сервера*
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
                await user.send(f'Тебя забанил {author.name} на сервере "{guild.name}" по причине: {reason}')
                await user.ban(reason=reason)
                await ctx.reply(f'{user.name} был забанен на сервере по причине: {reason}')
            else:
                await ctx.reply(f'Вы не модератор! У Вас нет права на лево:)')

    # @bot.command()
    # async def unban(ctx, user: discord.Member = None, *, reason='Я добрый'):
    #     if user is None:
    #         await ctx.reply('И кого мне разбанивать? Укажи пользователя')
    #     else:
    #         author = ctx.message.author
    #         roles = [i.name for i in author.roles]
    #         if os.getenv("ADMIN_ROLE") in roles:
    #             await user.unban(reason=reason)
    #             await ctx.reply(f'{user.name} был разбанен на сервере')
    #         else:
    #             await ctx.reply(f'Вы не модератор! У Вас нет права на лево:)')



    @bot.command()
    async def gay(ctx):
        await ctx.send('Гоша гей:)')


    bot.run(TOKEN)