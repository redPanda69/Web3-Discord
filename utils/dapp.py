import discord
from utils.wallet import *
from discord.ext import commands
import json
import asyncio
import os
from utils.dbquery import *
import random
bot = commands.Bot("!",intents=discord.Intents.all())
tresury = ""

@bot.event
async def on_ready():
    print("Bot has Started.")

@bot.command()
async def start(ctx):
    botmsg = await ctx.author.send("**Please enter your address: **")
    usermsg = await bot.wait_for("message",check=lambda m: m.channel.type == discord.ChannelType.private and Web3.isAddress(m.content))
    await botmsg.delete()
    address = usermsg.content
    address = connectWallet(address,ctx.author.id)
    await ctx.author.send(f"We have established a connection with {ctx.author.mention} and {address}....\nLets Gamble.....||**This is just a test bot!!!!**||")

@bot.command()
async def rps(ctx,choice:str,bet:int):
    address = getwallet(ctx.author.id)
    if address == None:
        await ctx.invoke(bot.get_command('start'))
        address = getwallet(ctx.author.id)
    if getBalance(address) < bet:
        return await ctx.reply("Insufficient Funds")
    choice = choice.lower()
    choices = ["rock","paper","scissors"]
    if choice not in choices:
        return await ctx.reply("Invalid Choice") 
    status = None
    botChoice = random.choice(choices)
    if botChoice == choice:
        await ctx.reply("Draw")
        status = "draw"
    elif (botChoice == "rock" and choice == "paper") or (botChoice == "paper" and choice == "scissors") or (botChoice == "scissors" and choice == "rock"):
        await ctx.reply("Vicrtory")
        status = "win"
    else:
        await ctx.reply("Better Luck Next time..")
        status = "lose"
    if status != "draw":
        if status == "lose":
            sendTransaction(address,tresury,bet)
        elif status == "win":
            sendTransaction(tresury,address,bet)
    
    add_details(ctx.author.id,status,bet)
    


@bot.command()
async def balance(ctx):
    address = getwallet(ctx.author.id)
    balance = getBalance(address)
    await ctx.reply(f"Balance: {balance} Ether")

@bot.command()
async def transaction(ctx,txId):
    tx = checkTransaction(txId)
    txNo = tx["nonce"]
    txfrom = tx["from"]
    txto = tx["to"]
    txValue = Web3.fromWei(tx["value"],"ether")
    txgas = tx["gas"]
    txgasprice = Web3.fromWei(tx["gasPrice"],"gwei")

    await ctx.send(f"""
**TRANSACTION ID**: {txId}
**TRANSACTION NO.**: {txNo}
**FROM**: {txfrom}
**TO**: {txto}
**VALUE**: {txValue} ETHER
**GAS**: {txgas} 
**GAS PRICE**: {txgasprice} GWEI
    """)

        
@bot.command()
async def profile(ctx):
    wins = request_profile(ctx.author.id,'win')
    lose = request_profile(ctx.author.id,'lose')
    draw = request_profile(ctx.author.id,'draw')
    address = getwallet(ctx.author.id)
    balance = getBalance(address)
    await ctx.send(
        f"""
** ADDRESS ** : {address}
** BALANCE ** : {balance}
** WINS **:{wins}
** LOSE **:{lose}
** DRAWS **:{draw}
        """
        
    )

def run(Token):
    bot.run(Token)
