import requests
from BrandrdXMusic import app
from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode
from MukeshAPI import api
import time

# YouTube API Key (Directly in chatgpt.py)
YOUTUBE_API_KEY = "AIzaSyBzGflkz5ieSID9DiDsc-bDrQrbSxbDsAA"  # Replace with your key
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# Store last 5 played songs
last_played_songs = []
autoplay_enabled = False

@app.on_message(filters.command(["autoplay"], prefixes=[".", "J", "j", "s", "", "/"]))
async def enable_autoplay(bot, message):
    """Enable autoplay"""
    global autoplay_enabled
    autoplay_enabled = True
    await message.reply_text(f"✅ **Autoplay has been enabled.**")

    # If autoplay is enabled and at least 1 song has been played, start autoplay
    if last_played_songs:
        next_song = fetch_next_track(last_played_songs[-1])  # Last played song se fetch karo
        await bot.send_message(message.chat.id, f"🎵 Now playing: {next_song}")
        update_song_history(next_song)

        # Here, add code to play the next song in VC

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
        next_song = fetch_next_track(last_played_songs[-1])  # Last played song ke basis pe
        await bot.send_message(message.chat.id, f"🎵 Now playing: {next_song}")
        update_song_history(next_song)

        # Add code here to play the next song in VC

def update_song_history(song):
    """Maintain last 5 played songs"""
    last_played_songs.append(song)
    if len(last_played_songs) > 5:
        last_played_songs.pop(0)

def fetch_next_track(last_song):
    """Fetch next track using YouTube API"""
    params = {
        "part": "snippet",
        "maxResults": 1,
        "q": f"{last_song} song",  # Adjust query as needed
        "type": "video",
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params).json()
    
    if "items" in response and response["items"]:
        video_title = response["items"][0]["snippet"]["title"]
        return video_title
    else:
        return "No related track found"

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
