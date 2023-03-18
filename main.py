import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

bot = commands.Bot(command_prefix='!')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
DiscordComponents(client)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def save(ctx, *, content):
    with open("saved_links.txt", "a") as f:
        f.write(content + "\n")
    await ctx.send(f"Content saved: {content}")


@bot.command()
async def list(ctx):
    with open("saved_links.txt", "r") as f:
        content = f.read()
    if content:
        await ctx.send(content)
    else:
        await ctx.send("No saved content.")


@bot.command()
async def clear(ctx):
    open("saved_links.txt", "w").close()
    await ctx.send("Content cleared.")


@bot.command()
async def help(ctx):
    help_message = """**Bot Commands:**
    !save [content] - saves the specified content
    !list - lists all saved content
    !clear - clears all saved content"""
    await ctx.send(help_message)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.command()
async def sum(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)

    
@bot.command()
async def save_button(ctx, *, content):
    button = Button(style=ButtonStyle.green, label="Save")
    message = await ctx.send(f"Content: {content}", components=[[button]])

    def check(res):
        return res.user == ctx.author and res.channel == ctx.channel and res.message.id == message.id

    try:
        res = await client.wait_for("button_click", check=check, timeout=15)
        if res.component.label == "Save":
            with open("saved_links.txt", "a") as f:
                f.write(content + "\n")
            await res.respond(type=6)
            await ctx.send(f"Content saved: {content}")
    except TimeoutError:
        await message.edit(content="Timed out", components=[])

bot.run('your-token-here')
