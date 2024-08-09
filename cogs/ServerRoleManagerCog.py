import discord
import psycopg2
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

import config
from cogs import LogCog


class ServerRoleManagerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.autoroles = {}
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("SELECT * from autoroles")
        rows = cur.fetchall()
        for row in rows:
            self.autoroles[row[0]] = row[1]
        cur.close()
        conn.close()
        LogCog.logSystem('Server role cog loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id in self.autoroles.keys():
            roleId = self.autoroles[member.guild.id]
            if roleId is not None:
                role = get(member.guild.roles, id=roleId)
                await member.add_roles(role)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def autorole(self, ctx, role: discord.Role):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("SELECT * from autoroles WHERE guild_id = %s", (ctx.guild.id,))
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO autoroles(guild_id, role_id) VALUES (%s, %s);",
                        (ctx.guild.id, role.id))
        else:
            cur.execute("UPDATE autoroles SET role_id= %s WHERE guild_id=%s", (role.id, ctx.guild.id))
        conn.commit()
        cur.close()
        conn.close()
        self.autoroles[ctx.guild.id] = role.id
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