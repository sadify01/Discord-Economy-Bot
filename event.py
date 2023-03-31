import discord
from discord.ext import commands
import sqlite3


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS main (user_id INTEGER, wallet INTEGER, bank INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS items ("user_id", "rifle", "pickaxe", "rod", "shovel", "fox", "wolf", "raccoon", "tiger", "lion", "deer")''')

        print("Bot is running!")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        author = message.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO main(user_id, wallet, bank) VALUES (?,?,?)", (author.id,100,0))

        cursor.execute(f"SELECT user_id FROM items WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO items(user_id, rifle, pickaxe, rod, shovel, fox, wolf, raccoon, tiger, lion, deer) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (author.id,1,1,1,1,0,0,0,0,0,0))

        db.commit()
        cursor.close()
        db.close()