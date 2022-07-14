from random import random
import discord
from discord.ext import commands
from asyncio import sleep
import pymongo
from pymongo import MongoClient
import re
import os
#import message_handel
#onm = message_handel


maindb = MongoClient(os.environ["mongo_url"])    
db = maindb["tourneydb"]
dbc = db["tourneydbc"]
tourneydbc=dbc


class Esports(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0



    @commands.command(aliases=['tsetup'])
    @commands.dm_only()
    @commands.cooldown(2, 20, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels=True, manage_messages=True, send_messages=True)
    @commands.has_permissions(manage_channels=True)
    async def ts(self, ctx, front, total_slot, mentions, *, name):
        guild_id = ctx.guild.id
        reason= f'Created by {ctx.author.name}'   #reason for auditlog
        category = await ctx.guild.create_category(name, reason=f"{ctx.author.name} created")
        await category.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.guild.create_text_channel(str(front)+"info", category=category, reason=reason)
        await ctx.guild.create_text_channel(str(front)+"updates", category=category,reason=reason)
        await ctx.guild.create_text_channel(str(front)+"roadmap", category=category,reason=reason)
        await ctx.guild.create_text_channel(str(front)+"how-to-register", category=category, reason=reason)
        r_ch = await ctx.guild.create_text_channel(str(front)+"register-here", category=category, reason=reason)    #registration Channel
        c_ch = await ctx.guild.create_text_channel(str(front)+"confirmed-teams", category=category, reason=reason)    #confirmation_channel
        await ctx.guild.create_text_channel(str(front)+"groups", category=category, reason=reason)
        await ctx.guild.create_text_channel(str(front)+"queries", category=category, reason=reason)

        role_name = front + "Confirmed"
        c_role = await ctx.guild.create_role(name=role_name, reason=f"Created by {ctx.author}") #role
        await r_ch.set_permissions(c_role, send_messages=False)
        tour = {"tid" : int(r_ch.id%1000000000000), "rch" : int(r_ch.id),"cch" : int(c_ch.id),"crole" : int(c_role.id),"tslot" : int(total_slot),"reged" : 1,"mentions" : int(mentions),"slotpg" : 12}
        

        dbc.insert_one(tour)
        return await ctx.send('**<:vf:947194381172084767>Successfully Created**',delete_after=5)


    







def setup(bot):
    bot.add_cog(Esports(bot))
