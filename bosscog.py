import discord
from discord.ext import commands
from bossfight import BossFight

sabetha: BossFight = BossFight('sabetha')
slothasor: BossFight = BossFight('slothasor')
matthias: BossFight = BossFight('matthias')
cairnB: BossFight = BossFight('cairn')
dhuumB: BossFight = BossFight('dhuum')

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

class BossCog:
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    async def _summon(self, ctx):
        summoned_channel = ctx.message.author.voice_channel 
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return None
        try:          
            return await self.bot.join_voice_channel(summoned_channel)
        except discord.ClientException:            
            server = ctx.message.server
            vc = self.bot.voice_client_in(server)
            if vc.server == server:
                return vc
            await vc.move_to(summoned_channel)
            return vc
        return None

    async def _leave(self, ctx):
        server = ctx.message.server
        for x in self.bot.voice_clients:
            if(x.server == server):
                return await x.disconnect()

    @commands.command(pass_context=True)
    async def sab(self, ctx):
        """Launches Sabetha boss fight"""
        vc = await self._summon(ctx)
        if vc is None:
            await self.bot.say("Can not start boss fight")
            return
        sabetha.start(self.bot, ctx.message.channel, vc)
        await self.bot.say("Sabetha started")
        return

    @commands.command(pass_context=True)
    async def sloth(self, ctx):
        """Launches Slothasor boss fight"""
        vc = await self._summon(ctx)
        if vc is None:
            await self.bot.say("Can not start boss fight")
            return
        slothasor.start(self.bot, ctx.message.channel, vc)
        await self.bot.say("Slothasor started")
        return

    @commands.command(pass_context=True)
    async def matt(self, ctx):
        """Launches Matthias boss fight"""
        vc = await self._summon(ctx)
        if vc is None:
            await self.bot.say("Can not start boss fight")
            return
        matthias.start(self.bot, ctx.message.channel, vc)
        await self.bot.say("Matthias started")
        return
    
    @commands.command(pass_context=True)
    async def cairn(self, ctx):
        """Launches Cairn boss fight"""
        vc = await self._summon(ctx)
        if vc is None:
            await self.bot.say("Can not start boss fight")
            return
        cairnB.start(self.bot, ctx.message.channel, vc)
        await self.bot.say("Cairn started")
        return

    @commands.command(pass_context=True)
    async def dhuum(self, ctx):
        """Launches Dhuum boss fight"""
        vc = await self._summon(ctx)
        if vc is None:
            await self.bot.say("Can not start boss fight")
            return
        dhuumB.start(self.bot, ctx.message.channel, vc)
        await self.bot.say("Dhuum started")
        return

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stop every boss fights"""
        sabetha.stop()
        slothasor.stop()
        matthias.stop()
        cairnB.stop()
        dhuumB.stop()
        await self._leave(ctx)
        await self.bot.say("Boss fights stopped")
        pass

def setup(bot):
    bot.add_cog(BossCog(bot))