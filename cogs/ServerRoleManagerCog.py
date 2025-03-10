import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

from service import autoRolesService
from cogs import LogCog


class ServerRoleManagerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        LogCog.logSystem('Server role cog loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id in autoRolesService.autoroles.keys():
            roleId = autoRolesService.autoroles[member.guild.id]
            if roleId is not None:
                role = get(member.guild.roles, id=roleId)
                await member.add_roles(role)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def autorole(self, ctx, role: discord.Role):
        await autoRolesService.add_role(ctx.guild.id, role.id)
        autoRolesService.autoroles[ctx.guild.id] = role.id
        await ctx.message.add_reaction('✅')

    @commands.command(aliases=['glall'])
    @has_permissions(manage_guild=True)
    async def giveroletoall(self, ctx, role: discord.Role):
        for member in ctx.guild.members:
            await member.add_roles(role)

    @commands.command(aliases=['gluser'])
    @has_permissions(manage_guild=True)
    async def giveroletousers(self, ctx, role: discord.Role):
        for member in ctx.guild.members:
            if not member.bot:
                await member.add_roles(role)

    @commands.command(aliases=['glbot'])
    @has_permissions(manage_guild=True)
    async def giveroletobots(self, ctx, role: discord.Role):
        for member in ctx.guild.members:
            if not member.bot:
                await member.add_roles(role)