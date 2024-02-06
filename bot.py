import os, telegram, requests, logging
from dotenv import load_dotenv
from omdb import get_movie_info
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

load_dotenv()

api_token = os.getenv('BOT_TOKEN')
bot = telegram.Bot(api_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am your cinemarecsbot")


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def ratings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text
    movie_info = get_movie_info(movie_name)

    message_text = ''

    if movie_info:
        rating_string = f"IMDB Rating: {movie_info['imdb_rating']}\n"
        for rating in movie_info['ratings']:
            rating_string += f"{rating['Source']}: {rating['Value']}\n"

        message_text = (f"{movie_info['title']} ({movie_info['year']}):\n\n" + 
            f"Genre:\n{movie_info['genre']} \n\n" +
            f"Plot:\n{movie_info['plot']}\n\n" +
            f"Starring:\n{movie_info['actors']}\n\n" +
            f"Ratings:\n{rating_string} \n" +
            f"Director:\n{movie_info['director']}\n\n" +
            f"Runtime:\n{movie_info['runtime']}" 
            ) 

        await context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(movie_info['poster'])])
    else:
        message_text = f"Movie '{movie_name}' not found. Check for typos and try again."
    
    await context.bot.send_message(chat_id = update.effective_chat.id, text = message_text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(api_token).build()
    
    start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    ratings_handler = MessageHandler(filters.TEXT, ratings)

    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(ratings_handler)
    
    application.run_polling()