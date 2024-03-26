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

word = pyfiglet.figlet_format('SERVER IS ONLINE')
print(word)

@bot.message_handler(commands=['start'])
def start(message):
    """Greets the user and asks what they would like to watch."""
    user_first_name = message.from_user.first_name
    greeting_message = f"Hi {user_first_name}!\n Send me the name of movie."
    logger.info(f"User {user_first_name} started the conversation.")
    bot.send_message(message.chat.id, greeting_message)
    bot.register_next_step_handler(message, movies_handler)

def movies_handler(message):
    """Fetches the movie data and sends it with the poster to the user."""
    user_input = message.text
    bot.send_message(message.chat.id, "Getting  data... Hold on... !")

    try:
        # Fetch the movie data from IMDb
        ia = imdb.IMDb()
        search_results = ia.search_movie(user_input)
        movie_id = search_results[0].getID()  # Get the first search result (assuming it's the correct movie).
        

        movie = ia.get_movie(movie_id)
        for director in movie['directors']:
        	(director['name'])
        plot = movie['plot'][0][:200] + '...'
        ia = Cinemagoer()
        
        


         
        
        poster_url = movie['full-size cover url']
        poster_response = requests.get(poster_url)
        if poster_response.status_code == 200:
            with open('poster.png', 'wb') as poster_file:
                poster_file.write(poster_response.content)
            # Prepare the message to send both poster and movie data
      
            movie_info = (
            f"Title: {movie['title']}\n\n"
    f"Year: {movie['year']}\n\n"
     f"Director: {director['name']}\n\n"
    f"Genres: {', '.join(movie['genres'])}\n\n"
    f"Runtime: {movie['runtime'][0]} minutes\n\n"
    f"Rating: {movie['rating']}\n\n"
    f"Plot: {plot}"
  
                
            )
            bot.send_photo(message.chat.id, open('poster.png', 'rb'), caption=movie_info, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "Sorry, unable to fetch the poster.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong while fetching the movie data.")

bot.polling()
