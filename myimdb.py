import telebot
import logging
import pyfiglet
import imdb
import requests
from telebot import types
from imdb import Cinemagoer

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate bot
bot = telebot.TeleBot('6495814879:AAH7ysEj6oQvpHn0R2VA3cRhMcWpnkg7C04')

# Display the server online message
word = pyfiglet.figlet_format('SERVER IS ONLINE')
print(word)

@bot.message_handler(commands=['start'])
def start(message):
    """Greets the user and asks what they would like to watch."""
    user_first_name = message.from_user.first_name
    greeting_message = f"Hi {user_first_name}!\nSend me the name of a movie."
    logger.info(f"User {user_first_name} started the conversation.")
    bot.send_message(message.chat.id, greeting_message)
    bot.register_next_step_handler(message, movies_handler)

def movies_handler(message):
    """Fetches the movie data and sends it with the poster to the user."""
    user_input = message.text
    bot.send_message(message.chat.id, "Getting data... Hold on...!")

    try:
        # Fetch the movie data from IMDb
        ia = Cinemagoer()
        search_results = ia.search_movie(user_input)
        
        if not search_results:
            bot.send_message(message.chat.id, "Sorry, no results found for the movie name.")
            return

        movie_id = search_results[0].movieID  # Get the first search result (assuming it's the correct movie).
        movie = ia.get_movie(movie_id)
        
        director_names = ', '.join([director['name'] for director in movie.get('directors', [])])
        plot = movie.get('plot outline', 'Plot not available')[:200] + '...'

        poster_url = movie.get('full-size cover url')
        if poster_url:
            poster_response = requests.get(poster_url)
            if poster_response.status_code == 200:
                with open('poster.png', 'wb') as poster_file:
                    poster_file.write(poster_response.content)
                
                # Prepare the message to send both poster and movie data
                movie_info = (
                    f"Title: {movie.get('title', 'N/A')}\n"
                    f"Year: {movie.get('year', 'N/A')}\n"
                    f"Director: {director_names if director_names else 'N/A'}\n"
                    f"Genres: {', '.join(movie.get('genres', []))}\n"
                    f"Runtime: {movie.get('runtime', ['N/A'])[0]} minutes\n"
                    f"Rating: {movie.get('rating', 'N/A')}\n"
                    f"Plot: {plot}"
                )
                bot.send_photo(message.chat.id, open('poster.png', 'rb'), caption=movie_info, parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "Sorry, unable to fetch the poster.")
        else:
            bot.send_message(message.chat.id, "Sorry, poster not available.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong while fetching the movie data.")

bot.polling()
                
