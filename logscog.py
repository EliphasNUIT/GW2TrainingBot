import discord
from discord.ext import commands
from config import config
from autologger import AutoLogger

class LogsCog:
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.autologger = AutoLogger()

    @commands.group(pass_context=True, aliases=['l'])
    async def logs(self, ctx):
        """Logs commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Check <prefix>help logs to see how to use this command")
        pass

    @logs.command(pass_context=True, name="success", aliases=['s'])
    async def logs_display_new_success(self, ctx):
        """Display new evtc files since the listening started"""
        await self.autologger.display_success(self.bot, ctx.message.channel)
        return

    @logs.command(pass_context=True, name="listen")
    async def logs_listen(self, ctx):
        """Listen and parse new logs"""
        if not (config.arc_enabled() and config.gw2el_enabled()):          
            await self.bot.say("You must give a valid gw2 arc dps path and gw2el path")
            return
        self.autologger.start(self.bot, ctx.message.channel)
        await self.bot.say("Listening started")
        return

    @logs.command(pass_context=True, name="regroup", aliases=['r'])
    async def logs_regroup(self, ctx):
        """Regroup new successful logs"""
        if config.diff_id(ctx.message.author.id):
            await self.bot.say('Only the bot owner can use this command')
            return       
        if not (config.arc_enabled() and config.gw2el_enabled()):          
            await self.bot.say("You must give a valid gw2 arc dps path and gw2el path")
            return
        self.autologger.regroup()
        await self.bot.say("Logs regrouped")
        return

    @logs.command(pass_context=True, name="clean", aliases=['c'])
    async def logs_clean(self, ctx):
        """Clean new faled logs"""
        if config.diff_id(ctx.message.author.id):
            await self.bot.say('Only the bot owner can use this command')
            return       
        if not (config.arc_enabled() and config.gw2el_enabled()):          
            await self.bot.say("You must give a valid gw2 arc dps path and gw2el path")
            return
        self.autologger.clean()
        await self.bot.say("Logs cleaned")
        return

    @logs.command(pass_context=True, name="stop")
    async def logs_stop(self, ctx):
        """Stop automatic logging"""
        if config.diff_id(ctx.message.author.id):
            await self.bot.say('Only the bot owner can use this command')
            return      
        if not (config.arc_enabled() and config.gw2el_enabled()):          
            await self.bot.say("You must give a valid gw2 arc dps path and gw2el path")
            return
        self.autologger.stop()
        await self.bot.say("Logs listening stopped")
        pass


def setup(bot):
    if not (config.arc_enabled() and config.gw2el_enabled()):          
        print("You must give a valid gw2 arc dps path and gw2el path")
        return   
    bot.add_cog(LogsCog(bot))
