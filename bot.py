import discord
from discord.ext import commands
import os

def doBot(token: str, user_id: str, prefix: str, auto_clean: bool):
    # create the bot
    bot = commands.Bot(description="GW2 Raid Bot",
                       command_prefix=commands.when_mentioned_or(prefix))

    @bot.event
    async def on_ready():
        bot.load_extension('bosscog')
        print('Connected!')
        print('Username: ' + bot.user.name)
        print('ID: ' + bot.user.id)
        pass

    @bot.command(pass_context=True, hidden=True)
    async def unload(ctx, extension):
        """Load the given extension."""
        if not ctx.message.author.id == user_id and not user_id == "":
            await bot.say('Only the bot owner can use this command')
            return
        bot.unload_extension(extension)
        await bot.say('Unloaded extension: ' + extension)
        pass

    @bot.command(pass_context=True, hidden=True)
    async def reload(ctx, extension):
        """Reload the given extension."""
        if not ctx.message.author.id == user_id and not user_id == "":
            await bot.say('Only the bot owner can use this command')
            return
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await bot.say('Reloaded extension: ' + extension)
        pass

    @bot.command(pass_context=True, hidden=True)
    async def load(ctx, extension):
        """Unload the given extension."""
        if not ctx.message.author.id == user_id and not user_id == "":
            await bot.say('Only the bot owner can use this command')
            return
        bot.load_extension(extension)
        await bot.say('Loaded extension: ' + extension)
        pass

    @bot.command(pass_context=True, hidden=True)
    async def exit(ctx):
        """Close the bot."""
        if not ctx.message.author.id == user_id and not user_id == "":
            await bot.say('Only the bot owner can use this command')
            return
        cache_path = './cache/'
        for file_name in os.listdir(cache_path):
            path = os.path.join(cache_path,file_name)
            try:
                if os.path.isfile(path):
                    os.unlink(path)
                pass
            except Exception  as e:
                print(e)
                pass
        await bot.close()
        pass

    # run the bot
    bot.run(token)
