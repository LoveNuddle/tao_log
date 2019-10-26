import discord,traceback,getpass,os
from discord.ext import commands

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
                    description=f"```py\n{text}```")
            )
            text = x

    await self.get_channel(635114963698188298).send(
        embed=discord.Embed(
            title="接続BOTのError情報:",
            description=f"```py\n{text}```"
        )
    )

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        self.remove_command('help')
        for cog in ['mmo.bot','mmo.main']:
            self.load_extension(cog)

    async def on_ready(self):
        for members_in_log in self.get_guild(634702862257094656).members:
            nitro_log_server = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
            admin_log_server = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703386473922580)
            if nitro_log_server in members_in_log.roles and not admin_log_server in members_in_log.roles:
                for members_official in self.get_guild(337524390155780107).members:
                    nitro_check2 = discord.utils.get(self.get_guild(337524390155780107).roles, id=623842965747400705)
                    if members_in_log == members_official and not nitro_check2 in members_official.roles:
                        await members_in_log.remove_roles(nitro_log_server)

                    else:
                        await members_in_log.add_roles(nitro_log_server)
        try:
            await self.change_presence(
                activity=discord.Game(
                    name="TAO公式鯖と接続中 | &&help"
                )
            )

        except Exception as e:
            await send_error(self, e)

    async def on_member_join(self,member):
        try:
            if not member.guild.id == 634702862257094656:
                return

            member_list=[]
            for members in self.get_guild(337524390155780107).members:
                member_list.append(members)
                if member == members:
                    lv1 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703389573382165)
                    await member.add_roles(lv1)

                    nitro = discord.utils.get(self.get_guild(337524390155780107).roles, id=623842965747400705)
                    if nitro in members.roles:
                        lv2 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387522498610)
                        await member.add_roles(lv2)

                        lv3 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
                        await member.add_roles(lv3)

                    admin = discord.utils.get(self.get_guild(337524390155780107).roles, id=351361336308924417)
                    if admin in members.roles:
                        lv2 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387522498610)
                        await member.add_roles(lv2)

                        lv3 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
                        await member.add_roles(lv3)

                        lv4 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703386473922580)
                        await member.add_roles(lv4)

            if not member in member_list:
                lv0 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703390311710720)
                return await member.add_roles(lv0)

            embed = discord.Embed(
                title=f"{member.name}さん、よろしくお願いします～",
                description=f"`現在の鯖の人数: `{len(member.guild.members)}\n\n"
                            f"{self.get_channel(634755588147904513).mention}は読んでね～",
                color=discord.Color.dark_green()
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
            )
            await self.get_channel(634755270626639882).send(embed=embed)

        except Exception as e:
            await send_error(self, e)

    async def on_member_remove(self,member):
        try:
            if member.guild.id == 634702862257094656:
                embed = discord.Embed(
                    title="ありがとうございました！",
                    description=f"{member.name}さんが\n"
                                f"この鯖から退出しました...；；\n\n"
                                f"現在の鯖の人数: {len(member.guild.members)}名",
                    colour=discord.Color.red()
                )
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
                )
                await self.get_channel(634755270626639882).send(embed=embed)

            if member.guild.id == 337524390155780107:
                for members in self.get_guild(634702862257094656).members:
                    if member == members:
                        print(members)
                        lv1 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703389573382165)
                        if lv1 in members.roles:
                            await members.remove_roles(lv1)

                        lv2 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387522498610)
                        if lv2 in members.roles:
                            await members.remove_roles(lv2)

                        lv3 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703387119845406)
                        if lv3 in members.roles:
                            await members.remove_roles(lv3)

                        lv4 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703386473922580)
                        if lv4 in members.roles:
                            await members.remove_roles(lv4)

                        lv0 = discord.utils.get(self.get_guild(634702862257094656).roles, id=634703390311710720)
                        await members.add_roles(lv0)

                        embed = discord.Embed(
                            description=f"『{member.guild.name}』を抜けたので{self.get_guild(634702862257094656).name}のでの権限を外しました。",
                            colour=discord.Color.red()
                        )
                        return await self.get_channel(634755270626639882).send(embed=embed)


        except Exception as e:
            await send_error(self, e)

    async def on_command_error(self,ctx, error):
        await send_error(self, error)
    
if __name__ == '__main__':
    bot = MyBot(command_prefix='&&')
    bot.run(os.environ.get("TOKEN"))
