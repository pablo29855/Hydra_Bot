import discord
from discord import app_commands
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

queue = []


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k'
}

def get_audio_url(query):
    """Obtiene la mejor URL de audio posible en máxima calidad."""
    ydl_opts = {
        'format': 'bestaudio[ext=webm]/bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch' if not query.startswith("http") else None,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        return info.get('url')

async def play_next(interaction: discord.Interaction):
    """Reproduce la siguiente canción en la cola."""
    if queue and interaction.guild.voice_client:
        next_song = queue.pop(0)
        audio_url = get_audio_url(next_song)
        if not audio_url:
            await interaction.response.send_message("❌ Error al obtener el audio.")
            return await play_next(interaction)

        interaction.guild.voice_client.stop()
        interaction.guild.voice_client.play(
            discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(play_next(interaction), bot.loop)
        )
        await interaction.followup.send(f"🎶 Reproduciendo: {next_song}")
    else:
        await interaction.guild.voice_client.disconnect()

@tree.command(name="play", description="Reproduce una canción en tu canal de voz")
async def play(interaction: discord.Interaction, query: str):
    """Reproduce una canción desde YouTube (por nombre o URL) con la mejor calidad."""
    await interaction.response.defer()
    if not interaction.user.voice:
        await interaction.followup.send("⚠️ Debes estar en un canal de voz.")
        return

    channel = interaction.user.voice.channel
    if not interaction.guild.voice_client:
        await channel.connect()

    audio_url = get_audio_url(query)
    if not audio_url:
        await interaction.followup.send("❌ No se pudo obtener la canción.")
        return

    if interaction.guild.voice_client.is_playing():
        queue.append(query)
        await interaction.followup.send(f"📥 Agregado a la cola: {query}")
    else:
        interaction.guild.voice_client.stop()
        interaction.guild.voice_client.play(
            discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(play_next(interaction), bot.loop)
        )
        await interaction.followup.send(f"🎵 Reproduciendo ahora: {query}")

@tree.command(name="pause", description="Pausa la música actual")
async def pause(interaction: discord.Interaction):
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        await interaction.response.send_message("⏸ Música pausada.")

@tree.command(name="resume", description="Reanuda la música pausada")
async def resume(interaction: discord.Interaction):
    if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        await interaction.response.send_message("▶ Música reanudada.")

@tree.command(name="stop", description="Detiene la música y desconecta el bot")
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        queue.clear()
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("⏹ Bot desconectado y cola vaciada.")

@tree.command(name="skip", description="Salta la canción actual")
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("⏭ Canción saltada.")
        await play_next(interaction)

@tree.command(name="queue_list", description="Muestra la cola de canciones")
async def queue_list(interaction: discord.Interaction):
    if queue:
        queue_msg = "\n".join([f"{i+1}. {song}" for i, song in enumerate(queue)])
        await interaction.response.send_message(f"📜 **Lista de reproducción:**\n{queue_msg}")
    else:
        await interaction.response.send_message("📭 La cola está vacía.")

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

bot.run(TOKEN)
