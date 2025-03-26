import discord
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"✅ Comandos slash registrados en el servidor {GUILD_ID}")

bot = MyClient()

@bot.tree.command(name="play", description="Reproduce una canción en tu canal de voz")
@app_commands.describe(query="Nombre o URL de la canción")
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.send_message(f"🎶 Buscando: {query}")

@bot.tree.command(name="pause", description="Pausa la música actual")
async def pause(interaction: discord.Interaction):
    await interaction.response.send_message("⏸ Música pausada.")

@bot.tree.command(name="resume", description="Reanuda la música pausada")
async def resume(interaction: discord.Interaction):
    await interaction.response.send_message("▶ Música reanudada.")

@bot.tree.command(name="stop", description="Detiene la música y desconecta el bot")
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message("⏹ Bot desconectado.")

@bot.tree.command(name="skip", description="Salta la canción actual")
async def skip(interaction: discord.Interaction):
    await interaction.response.send_message("⏭ Canción saltada.")

@bot.tree.command(name="queue_list", description="Muestra la cola de canciones")
async def queue_list(interaction: discord.Interaction):
    await interaction.response.send_message("📜 Mostrando la lista de reproducción...")

bot.run(TOKEN)