import discord
from discord.ext import commands
import typing
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

#Comando realizado en clase
@bot.command()
async def lucky(ctx, eleccion: str = None):
    """Elige par o impar y compara con un número aleatorio."""
    if eleccion is None:
        await ctx.send("Elige: **par** o **impar**")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)
        eleccion = msg.content.lower()
    else:
        eleccion = eleccion.lower()

    if eleccion not in ("par", "impar"):
        await ctx.send("Debes escribir `par` o `impar`.")
        return

    numero = random.randint(1, 10)
    resultado = "par" if numero % 2 == 0 else "impar"

    if eleccion == resultado:
        await ctx.send(f"¡Salió **{resultado}** con el número {numero}. Ganaste!")
    else:
        await ctx.send(f"Salió **{resultado}** con el número {numero}. Perdiste")

# Agregando un comando actualizado
# Tarea agregando el comando help (no predeterminado)
@bot.command()
async def help(ctx):
    """Muestra la lista de comandos disponibles en un embed."""
    embed = discord.Embed(
        title="Lista de Comandos del Bot",
        description="Aquí tienes todos los comandos disponibles:",
        color=discord.Color.blue()
    )

    # Cada campo es un comando
    embed.add_field(name="➕ `?add <num1> <num2>`", value="Suma dos números.", inline=False)
    embed.add_field(name="🎲 `?roll NdN`", value="Lanza dados en formato NdN.", inline=False)
    embed.add_field(name="🤔 `?choose <opción1> <opción2> ...`", value="Elige entre múltiples opciones.", inline=False)
    embed.add_field(name="🔁 `?repeat <veces> <mensaje>`", value="Repite un mensaje varias veces.", inline=False)
    embed.add_field(name="👤 `?joined @miembro`", value="Muestra cuándo se unió un miembro.", inline=False)
    embed.add_field(name="😎 `?cool [subcomando]`", value="Verifica si un usuario es genial.", inline=False)
    embed.add_field(name="🍀 `?lucky [par/impar]`", value="Juega a par o impar con un número aleatorio.", inline=False)

    #Agregando imágenes personalizadas
    embed.set_footer(text="Usa ?comando para interactuar con el bot")
    embed.set_thumbnail(url="https://i1.sndcdn.com/artworks-rNd3E2INYdfCMZ3D-y3CP3A-t500x500.jpg")

    await ctx.send(embed=embed)

bot.run("TU-TOKEN-AQUí")
