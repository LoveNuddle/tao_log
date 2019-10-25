import getpass,asyncio,traceback,discord
from discord.ext import commands

left = '⏪'
right = '⏩'

async def send_error(self,error):
    text = ""
    for x in traceback.format_exception(type(error), error, error.__traceback__):
        x = x.replace(f"\\{getpass.getuser()}\\", "\\*\\")
        if len(text + x) < 2000 - 9:
            text += x
        else:
            await self.get_channel(635114963698188298).send(
                embed=discord.Embed(
                    title="接続BOTのError情報:",
                    description=f"```py\n{text}```"
                )
            )
            text = x

    await self.get_channel(635114963698188298).send(
        embed=discord.Embed(
            title="接続BOTのError情報:",
            description=f"```py\n{text}```")
    )


def predicate(message, l, r, bot):
    def check(reaction, user):
        if reaction.message.id != message.id or user == bot.user:
            return False

        if l and reaction.emoji == left or r and reaction.emoji == right:
            return True
    return check

class auto_bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help',description='このBOTのすべての機能を書いた',hidden=True)
    async def this_bot_help(self,ctx):
        try:
            help_message = [f"```"
                            f"[&&member 役職名] | その役職が誰に付与されているのかを全て表示します\n"
                            f"[&&all] | 鯖の全ての役職を表示します\n"
                            f"[&&self] | 自分が付与されている役職を表示します\n"
                            f"[&&ping] | BOTの反応速度の速さ確認```",]

            embed = discord.Embed(
                title=f"{self.bot.user}の説明:",
                description="このBOTは公式鯖との接続用です。\n" + help_message[0],
                colour=discord.Color.dark_magenta()
            )
            embed.set_thumbnail(
                url=self.bot.user.avatar_url
            )
            embed.set_footer(
                text=f"このBOTの製作者:『{self.bot.get_user(304932786286886912)}』"
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await send_error(self.bot, e)


    @commands.command(name='member',description='役職付与されてるメンバーリスト',hidden=True)
    async def list_of_role(self,ctx,*,role_name=""):
        try:
            if not role_name:
                msg = discord.Embed(
                    description=f"{ctx.message.author.mention}さん\n"
                                f"役職名はちゃんと入力して下さい！",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=msg)

            elif not discord.utils.get(ctx.message.guild.roles,name=role_name):
                msg = discord.Embed(
                    description=f"{ctx.message.author.mention}さん\n"
                                f"その名前の役職は存在してないそうですよ？",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=msg)

            else:
                async def send(member_data):
                    page = 1
                    embed = discord.Embed(
                        title=f"『{role_name}』役職を持っているメンバー！！",
                        description="".join(
                            member_data[(page - 1) * 20:page * 20]
                        ),
                        colour=discord.Color.dark_gold()
                    )
                    msg =  await ctx.send(embed=embed)

                    while True:
                        l = page != 1
                        r = page < len(member_data) / 20
                        if l:
                            await msg.add_reaction(left)

                        if r:
                            await msg.add_reaction(right)

                        try:
                            react,user = await self.bot.wait_for('reaction_add',timeout=10,check=predicate(msg,l,r,self.bot))
                            if react.emoji == left:
                                page -= 1

                            elif react.emoji == right:
                                page += 1

                            embeds = discord.Embed(
                                title=f"『{role_name}』役職を持っているメンバー！！",
                                description="".join(
                                    member_data[(page - 1) * 20:page * 20]
                                ),
                                colour=discord.Color.dark_gold()
                            )

                            await msg.edit(embed=embeds)
                            await msg.remove_reaction(left, self.bot.user)
                            await msg.remove_reaction(right, self.bot.user)
                            await msg.remove_reaction(react.emoji, user)

                        except asyncio.TimeoutError:
                            return

                i = 1
                member_data = []
                role = discord.utils.get(ctx.message.guild.roles,name=role_name)
                for member in ctx.message.guild.members:
                    if role in member.roles:
                        member_data.append(
                            "".join("{0}人目:『{1}』\n".format(
                                i,member.name)
                            )
                        )
                        i += 1

                return await send(member_data)

        except Exception as e:
            await send_error(self.bot, e)


    @commands.command(name='all',description='鯖の役職全て',hidden=True)
    async def all_role(self,ctx):

        def slice(li,n):
            while li:
                yield li[:n]
                li = li[n:]

        page = 1
        for roles in slice(ctx.message.guild.roles[::-1],250):

            role = [f'{i}: {role.mention}' for (i,role) in enumerate(roles,start=1)]

            userembed = discord.Embed(
                description="\n".join(
                    role[(page - 1) * 50:page * 50]
                )
            )
            userembed.set_thumbnail(
                url=ctx.message.guild.icon_url
            )
            userembed.set_author(
                name=ctx.message.guild.name + "の全役職情報:"
            )
            userembed.set_footer(
                text="この鯖の役職の合計の数は[{}]です！".format(
                    str(len(ctx.message.guild.roles))
                )
            )
            msg = await ctx.send(embed=userembed)
            while True:
                l = page != 1
                r = page < len(role) / 50
                if l:
                    await msg.add_reaction(left)

                if r:
                    await msg.add_reaction(right)

                try:
                    react,user = await self.bot.wait_for('reaction_add',timeout=10,check=predicate(msg,l,r,self.bot))
                    if react.emoji == left:
                        page -= 1

                    elif react.emoji == right:
                        page += 1

                    for roles in slice(ctx.message.guild.roles[::-1],250):
                        role = [f'{i}: {role.mention}' for (i,role) in enumerate(roles,start=1)]

                    embed = discord.Embed(
                        description="\n".join(
                            role[(page - 1) * 50:page * 50]
                        )
                    )
                    embed.set_thumbnail(
                        url=ctx.message.guild.icon_url
                    )
                    embed.set_author(
                        name=ctx.message.guild.name + "の全役職情報:"
                    )
                    embed.set_footer(
                        text="この鯖の役職の合計の数は[{}]です！".format(
                            str(len(ctx.message.guild.roles))
                        )
                    )

                    await msg.edit(embed=embed)
                    await msg.remove_reaction(left, self.bot.user)
                    await msg.remove_reaction(right, self.bot.user)
                    await msg.remove_reaction(react.emoji, user)

                except asyncio.TimeoutError:
                    return


    @commands.command(name='self',description='自分の役職',hidden=True)
    async def author_role(self,ctx):
        page = 1
        role = [r.mention for r in ctx.message.author.roles][::-1]

        embed = discord.Embed(
            title=f"{ctx.message.author}に付与されてる役職一覧:",
            description="\n".join(
                role[(page - 1) * 25:page * 25]
            )
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                ctx.message.author
            )
        )
        msg = await ctx.send(embed=embed)

        while True:
            l = page != 1
            r = page < len(role) / 20

            if l:
                await msg.add_reaction(left)

            if r:
                await msg.add_reaction(right)

            try:
                react,user = await self.bot.wait_for('reaction_add',timeout=10,check=predicate(msg,l,r,self.bot))

                if react.emoji == left:
                    page -= 1

                elif react.emoji == right:
                    page += 1

                role = [r.mention for r in ctx.message.author.roles][::-1]
                embeds = discord.Embed(
                    title=f"{ctx.message.author}に付与されてる役職一覧:",
                    description="\n".join(
                        role[(page - 1) * 25:page * 25]
                    )
                )
                embeds.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(
                        ctx.message.author
                    )
                )

                await msg.edit(embed=embeds)
                await msg.remove_reaction(left, self.bot.user)
                await msg.remove_reaction(right, self.bot.user)
                await msg.remove_reaction(react.emoji, user)

            except asyncio.TimeoutError:
                return


def setup(bot):
    bot.add_cog(auto_bot(bot))
