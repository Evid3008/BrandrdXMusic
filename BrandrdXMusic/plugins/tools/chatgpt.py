import requests
import random
from BrandrdXMusic import app
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from MukeshAPI import api

# Store last 5 played songs
last_played_songs = []
autoplay_enabled = False

@app.on_message(filters.command(["autoplay"], prefixes=[".", "J", "j", "s", "", "/"]))
async def enable_autoplay(bot, message):
    """Enable autoplay"""
    global autoplay_enabled
    autoplay_enabled = True
    await message.reply_text(f"✅ **Autoplay has been enabled.**")

    # If autoplay enabled & at least 1 song played, fetch next
    if last_played_songs:
        next_song = fetch_next_track(last_played_songs)
        await bot.send_message(message.chat.id, f"🎵 Now playing: {next_song}")
        update_song_history(next_song)

@app.on_message(filters.command(["stopautoplay"], prefixes=[".", "J", "j", "s", "", "/"]))
async def disable_autoplay(bot, message):
    """Disable autoplay"""
    global autoplay_enabled
    autoplay_enabled = False
    await message.reply_text(f"❌ **Autoplay has been disabled.**")

@app.on_message(filters.command(["play"], prefixes=[".", "J", "j", "s", "", "/"]))
async def play_music(bot, message):
    """Play music and track history"""
    song_name = message.text.split(" ", 1)[1]
    update_song_history(song_name)
    
    await bot.send_message(message.chat.id, f"🎶 Now playing: {song_name}")

    # If autoplay is enabled and enough songs exist, play next
    if autoplay_enabled and len(last_played_songs) >= 1:
        next_song = fetch_next_track(last_played_songs)
        await bot.send_message(message.chat.id, f"🎵 Now playing: {next_song}")
        update_song_history(next_song)

def update_song_history(song):
    """Maintain last 5 played songs"""
    last_played_songs.append(song)
    if len(last_played_songs) > 5:
        last_played_songs.pop(0)

def fetch_next_track(last_songs):
    """Fetch next track based on last played songs (Dummy logic)"""
    return "Related Track to " + random.choice(last_songs)

@app.on_message(filters.command(["chatgpt", "ai", "ask", "", "iri"], prefixes=[".", "J", "j", "s", "", "/"]))
async def chat_gpt(bot, message):
    """ChatGPT AI integration"""
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        # Check if name is defined, if not, set a default value
        name = message.from_user.first_name if message.from_user else "User"

        if len(message.command) < 2:
            await message.reply_text(f"**Hello {name}, How can I help you today?**")
        else:
            query = message.text.split(' ', 1)[1]
            response = api.gemini(query)["results"]
            await message.reply_text(f"{response}", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply_text(f"**Error: {e}**")
