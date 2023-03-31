import discord
from discord.ext import commands
from discord.commands import Option
from event import Event
import itertools
import datetime
import sqlite3
import random


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents)

client.add_cog(Event(client))

shop_ = [
        {"name":"hunting-rifle", "name_":"<:hunting_rifle:1089947749681741976> Hunting Rifle", "price":20000, "description":"sample"},
        {"name":"fishing-rod", "name_":"<:fishing:1089628075890847744> Fishing Rod", "price":10000, "description":"sample"},
        {"name":"pickaxe", "name_":"<:pickaxe:1089954106531127296> Pickaxe", "price":10000, "description":"sample"},
        {"name":"shovel", "name_":"<:shovel:1089628040079872190> Shovel", "price":10000, "description":"sample"},
    ]

@client.slash_command(guild_ids=[1086006180356309043], description="Deposit money from your wallet into your bank.")
async def deposit(ctx, amount:int):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE user_id = {ctx.author.id}")
    bal = cursor.fetchone()

    try:
        wallet = bal[1]
        bank = bal[2]
    except Exception as e:
        print(e)

    if wallet < amount:
        embed = discord.Embed(description="You don't have enough money in your wallet!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)
    else:
        cursor.execute("UPDATE main SET bank = ? WHERE user_id = ?", (bank + amount, ctx.author.id))
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
        embed = discord.Embed(color=discord.Color.og_blurple())
        embed.set_author(icon_url=ctx.author.display_avatar, name=f"{ctx.author.display_name} deposited ⏣ {amount:,}")
        embed.add_field(name="New wallet balance", value=f"⏣ {wallet - amount:,}", inline=False)
        embed.add_field(name="New bank balance", value=f"⏣ {bank + amount:,}", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/9747/9747020.png")
        await ctx.respond(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.slash_command(guild_ids=[1086006180356309043], description="Withdraw money from your bank into your wallet.")
async def withdraw(ctx, amount:int):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE user_id = {ctx.author.id}")
    bal = cursor.fetchone()

    try:
        wallet = bal[1]
        bank = bal[2]
    except Exception as e:
        print(e)

    if bank < amount:
        embed = discord.Embed(description="You don't have enough money in your wallet!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)
    else:
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
        cursor.execute("UPDATE main SET bank = ? WHERE user_id = ?", (bank - amount, ctx.author.id))
        embed = discord.Embed(color=discord.Color.og_blurple())
        embed.set_author(icon_url=ctx.author.display_avatar, name=f"{ctx.author.display_name} withdrawn ⏣ {amount:,}")
        embed.add_field(name="New wallet balance", value=f"⏣ {wallet + amount:,}", inline=False)
        embed.add_field(name="New bank balance", value=f"⏣ {bank - amount:,}", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/9747/9747020.png")
        await ctx.respond(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.slash_command(guild_ids=[1086006180356309043], description="View someone's balance. Wallet, bank and net worth.")
async def balance(ctx):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {ctx.author.id}")
    bal = cursor.fetchone()

    embed = discord.Embed(color=discord.Color.og_blurple())
    embed.set_author(icon_url=ctx.author.id.display_avatar, name=f"{ctx.author.id.display_name}'s balance")
    embed.description = f"**Wallet:** ⏣ {bal[0]:,}\n**Bank:** ⏣ {bal[1]:,}\n**Net:** ⏣ {bal[0] + bal[1]:,}"
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1138/1138038.png")
    await ctx.respond(embed=embed)


@client.slash_command(guild_ids=[1086006180356309043], description="Beg for money.")
async def beg(ctx):
    earnings = random.randint(100, 500)

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()

    cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet[0] + int(earnings), ctx.author.id))
    embed = discord.Embed(color=discord.Color.og_blurple())
    embed.set_author(icon_url=ctx.author.display_avatar, name=f"{ctx.author.display_name} found ⏣ {earnings:,}")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3280/3280845.png")
    await ctx.respond(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.slash_command(guild_ids=[1086006180356309043], description="")
async def gamble(ctx, amount:int=100):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    if amount < 100:
        embed = discord.Embed(description=f"You should put at least ⏣ {100:,}!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)

    if wallet < amount:
        embed = discord.Embed(description="You don't have enough money in your wallet!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)

    user_strikes = random.randint(1, 15)
    bot_strikes = random.randint(5, 15)

    if user_strikes > bot_strikes:
        percentage = random.randint(50, 100)
        amount_won = int(amount*(percentage/100))
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet + amount_won, ctx.author.id))
        db.commit()
        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="You won", value=f"⏣ {amount_won:,}", inline=False)
        embed.add_field(name="New wallet balance", value=f"⏣ {wallet + amount_won:,}", inline=False)
        embed.set_author(icon_url=ctx.author.display_avatar, name=f"You won {ctx.author.display_name}!")

    elif user_strikes < bot_strikes:
        percentage = random.randint(0, 100)
        amount_lost = int(amount*(percentage/100))
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet - amount_lost, ctx.author.id))
        db.commit()
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="You lost", value=f"⏣ {amount_lost:,}", inline=False)
        embed.add_field(name="New wallet balance", value=f"⏣ {wallet - amount_lost:,}", inline=False)
        embed.set_author(icon_url=ctx.author.display_avatar, name=f"Shit play {ctx.author.display_name}!")
    
    else:
        embed = discord.Embed(description=f"It was a tie!", color=discord.Color.yellow())
        embed.set_author(icon_url=ctx.author.display_avatar, name=f"Shit play {ctx.author.display_name}!")

    embed.add_field(name=f"**{ctx.author.display_name.title()}**", value=f"Strikes: {user_strikes}")
    embed.add_field(name=f"**{ctx.bot.user.display_name.title()}**", value=f"Strikes: {bot_strikes}")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/659/659395.png")
    await ctx.respond(embed=embed)

    cursor.close()
    db.close()


@client.slash_command(guild_ids=[1086006180356309043], description="Spin the slots for a chance to win the jackpot.")
async def slots(ctx, amount:int=100):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    if amount < 100:
        embed = discord.Embed(description=f"You should put at least ⏣ {100:,}!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)

    if wallet < amount:
        embed = discord.Embed(description="You don't have enough money in your wallet!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)

    times_factors = random.randint(1, 5)
    earnings = int(amount*times_factors)

    final = []
    for i in range(3):
        i = random.choice(["🍉","💎","💰","⚡️","👑","🏆","🍀","**7**"])
        final.append(i)

    if final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet + earnings, ctx.author.id))
        db.commit()
        embed = discord.Embed(title=f"Slot Machine", color=discord.Color.green())
        embed.add_field(name=f"You won ⏣ {earnings:,}", value=f"{final[0]}┃{final[1]}┃{final[2]}")
        embed.add_field(name=f"------------------------------", value=f"**Multiplier:** X{times_factors}", inline=False)
        embed.add_field(name=f"------------------------------", value=f"**New balance:** ⏣ {wallet + earnings:,}", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await ctx.respond(embed=embed)

    else:
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet - earnings, ctx.author.id))
        db.commit()
        embed = discord.Embed(title=f"Slot Machine", color=discord.Color.red())
        embed.add_field(name=f"You lost ⏣ {earnings:,}", value=f"{final[0]}┃{final[1]}┃{final[2]}")
        embed.add_field(name=f"------------------------------", value=f"**Multiplier:** X{times_factors}", inline=False)
        embed.add_field(name=f"------------------------------", value=f"**New balance:** ⏣ {wallet - earnings:,}", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await ctx.respond(embed=embed)

        cursor.close()
        db.close()


@client.slash_command(guild_ids=[1086006180356309043], description="View someone's inventory.")
async def inventory(ctx):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM items WHERE user_id = {ctx.author.id}")
    items = cursor.fetchone()

    items_list = [
        None,
        "<:hunting_rifle:1089947749681741976> Hunting Rifle",
        "<:fishing:1089628075890847744> Fishing Rod",
        "<:pickaxe:1089954106531127296> Pickaxe",
        "<:shovel:1089628040079872190> Shovel",
        "🦊 Fox",
        "🐺 Wolf",
        "🦝 Raccoon",
        "🐯 Tiger",
        "🦁 Lion",
        "🦌 Deer"
    ]

    items_ = [f"{i} ─ {j}" for i, j in itertools.zip_longest(items_list, items) if j > 0 and j < 100000000000000000]

    items_ = "\n".join(items_) if len(items_) > 0 else "*No tools in inventory!*"

    embed = discord.Embed(description=items_, color=discord.Color.og_blurple())
    embed.set_author(icon_url=ctx.author.display_avatar, name=f"{ctx.author.display_name}'s inventory")
    await ctx.respond(embed=embed)


@client.slash_command(guild_ids=[1086006180356309043], description="View all shop items.")
async def shop(ctx):
    embed = discord.Embed(title="Shop", color=discord.Color.og_blurple())

    for item in shop_:
        name = item["name_"]
        price = item["price"]
        desc = item["description"]
        embed.add_field(name=f"**{name}** ─ ⏣ {price:,}", value=f"{desc}", inline=False)

    await ctx.respond(embed=embed)


@client.slash_command(guild_ids=[1086006180356309043], description="Buy an item.")
async def buy(ctx, item, amount:int=1):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()
    item = item.lower()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    for item_ in shop_:
        if item_["name"] == item:
            name = item_["name"]
            price = item_["price"]
            desc = item_["description"]
            break

    if amount < 1:
        embed = discord.Embed(description="You can only buy 1 or more!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)

    elif wallet < price * amount:
        embed = discord.Embed(description="You don't have enough money in your wallet!", color=discord.Color.red())
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4299/4299398.png")
        return await ctx.respond(embed=embed)


client.run("MTA4ODEzNjA0OTA4NTEyODcwNA.Gvchhb.1KQihd0lRy-TNaJQHNtttANvV7Y290HCx7s83s")