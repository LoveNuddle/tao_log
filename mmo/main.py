import discord,time,os,sys
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='ping',description='BOTの速度を測ることができる',pass_context=True)
    async def pings(self,ctx):
        before = time.monotonic()

        msg = await ctx.send(
            embed=discord.Embed(
                description="```TAO接続BOT全体の反応速度```\nPong!"
            )
        )

        return await msg.edit(
            embed=discord.Embed(
                description=f"```TAO接続BOT全体の反応速度```\nPong! `{int((time.monotonic() - before) * 1000)}ms`"
            )
        )


    @commands.command(name='restart',description='BOTを再起動',pass_context=True)
    async def restart(self,ctx):
        if not ctx.message.author.id in [304932786286886912,460208854362357770,574166391071047694,294362309558534144]:
            return await ctx.send(
                embed=discord.Embed(
                    description=f"指定ユーザーしか使えません。",
                    color=0xC41415)
            )

        await ctx.send(
            embed=discord.Embed(
                description=f"{ctx.message.author.mention}さんが強制再起動を開始しました！",
                color=0xC41415
            )
        )

        os.execl(sys.executable, sys.executable, *sys.argv)


def setup(bot):
    bot.add_cog(Main(bot))