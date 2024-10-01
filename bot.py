import os
from dotenv import load_dotenv
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters

# Load environment variables from .env file
load_dotenv()

# Define states for conversation
FARE_ENQUIRY, SEARCH_STATION, CONTINUE_OR_STOP = range(3)

# Function to start the bot
async def start(update: Update, context) -> None:
    await show_main_menu(update.message.chat, context)

# Function to show the main menu
async def show_main_menu(chat, context):
    keyboard = [
        [InlineKeyboardButton("Fare Info", callback_data='fare_enquiry')],
        [InlineKeyboardButton("Search Station", callback_data='search_station')],
        [InlineKeyboardButton("Settings", callback_data='settings')],
        [InlineKeyboardButton("Share", callback_data='share')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await chat.send_message("Please choose an option:", reply_markup=reply_markup)

# Function to handle fare enquiry
async def fare_enquiry(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    await update.effective_chat.send_message("Please enter the train number, from station code, and to station code (e.g., 19038 ST BVI):")
    return FARE_ENQUIRY

# Function to fetch fare enquiry results
async def fetch_fare_enquiry(update: Update, context) -> int:
    fare_info = update.message.text.split()
    train_number, from_station, to_station = fare_info[0], fare_info[1], fare_info[2]

    url = "https://irctc1.p.rapidapi.com/api/v2/getFare"
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "irctc1.p.rapidapi.com"
    }
    querystring = {"trainNo": train_number, "fromStationCode": from_station, "toStationCode": to_station}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        fare_data = response.json()
        await send_fare_responses(update, fare_data)
    else:
        await update.message.reply_text("Error fetching fare information.")
    
    # After responding, prompt the user after 30 seconds
    await asyncio.sleep(30)
    await ask_continue_or_stop(update, context)
    
    return ConversationHandler.END

# Function to send fare responses
async def send_fare_responses(update: Update, fare_data):
    if not fare_data.get('status'):
        await update.message.reply_text("Error fetching fare information.")
        return

    general_fare = fare_data['data'].get('general', [])
    tatkal_fare = fare_data['data'].get('tatkal', [])

    general_response = "*General Fare Charges*\n\n"
    for fare in general_fare:
        if not fare['breakup']: 
            continue
        general_response += f"*Class Type: {fare['classType']}*\n\n"
        for item in fare['breakup']:
            general_response += f"{item['title']}  - ₹{item['cost']}\n"
        general_response += "———————\n\n"

    if general_response.strip():
        await update.message.reply_text(general_response, parse_mode='Markdown')

    tatkal_response = "*Tatkal Fare Charges*\n\n"
    for fare in tatkal_fare:
        if not fare['breakup']:
            continue
        tatkal_response += f"*Class Type: {fare['classType']}*\n\n"
        for item in fare['breakup']:
            tatkal_response += f"{item['title']}  - ₹{item['cost']}\n"
        tatkal_response += "———————\n\n"

    if tatkal_response.strip():
        await update.message.reply_text(tatkal_response, parse_mode='Markdown')

# Function to handle search station
async def search_station(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    await update.effective_chat.send_message("Please enter a station name or code:")
    return SEARCH_STATION

# Function to fetch search station results
async def fetch_search_station(update: Update, context) -> int:
    station_query = update.message.text

    url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "irctc1.p.rapidapi.com"
    }
    querystring = {"query": station_query}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        station_data = response.json()
        await send_station_responses(update, station_data)
    else:
        await update.message.reply_text("Error fetching station information.")

    # After responding, prompt the user after 30 seconds
    await asyncio.sleep(30)
    await ask_continue_or_stop(update, context)

    return ConversationHandler.END

# Function to send station search results
async def send_station_responses(update: Update, station_data):
    if not station_data.get('status'):
        await update.message.reply_text("No matching stations found.")
        return

    stations = station_data['data']
    response_text = "Matching Stations:\n\n"
    for station in stations:
        response_text += f"Name: {station['name']}\nCode: {station['code']}\nState: {station['state_name']}\n\n"
    
    await update.message.reply_text(response_text)

# Function to prompt the user whether they want to continue or stop
async def ask_continue_or_stop(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='continue')],
        [InlineKeyboardButton("No", callback_data='stop')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("What else can I help you with?", reply_markup=reply_markup)

# Function to handle user's choice to continue or stop
async def handle_continue_or_stop(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'continue':
        await show_main_menu(update.effective_chat, context)  # Show the main menu when "Yes" is clicked
    else:
        await update.effective_chat.send_message("Bot stopped. Have a nice day!")
        return ConversationHandler.END

# Function to stop the bot
async def stop(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    await update.effective_chat.send_message("Bot stopped. Have a nice day!")

# Function to handle unknown commands
async def unknown(update: Update, context) -> None:
    await update.message.reply_text("Sorry, I didn't understand that command.")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Conversation handler for fare enquiry
    fare_enquiry_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(fare_enquiry, pattern='fare_enquiry')],
        states={
            FARE_ENQUIRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_fare_enquiry)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    # Conversation handler for search station
    search_station_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(search_station, pattern='search_station')],
        states={
            SEARCH_STATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_search_station)],
            CONTINUE_OR_STOP: [CallbackQueryHandler(handle_continue_or_stop, pattern='^(continue|stop)$')]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(fare_enquiry_conv_handler)
    application.add_handler(search_station_conv_handler)
    application.add_handler(CallbackQueryHandler(stop, pattern='stop'))

    # Handle unknown messages
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()