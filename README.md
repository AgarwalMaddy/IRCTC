Here's a **GitHub README template** based on your current bot features and the RapidAPI integration.

---

# 🚆 Indian Railways Telegram Bot

A fully functional Telegram bot for fetching Indian Railway information like fare details, station search, train status, and seat availability. This bot uses the [IRCTC API on RapidAPI](https://rapidapi.com/IRCTCAPI/api/irctc1/playground/apiendpoint_3cdbbdeb-1ef6-44de-9515-38d253e9b9de) for real-time data.

## 📜 Features

- **Fare Enquiry**: Fetch fare details for any train between two stations.
- **Search Station**: Search for Indian railway stations using station names or codes.
- **Train Status**: Retrieve the live running status of trains.
- **Seat Availability**: Check the availability of seats in trains.
- **Settings**: Customize the bot settings as per user preferences.
- **Automated Prompts**: After a response, the bot will ask after 30 seconds if you need further assistance. It allows the user to continue or stop the session based on their response.

## 🛠️ Tech Stack

- **Python**: Core language for the bot.
- **Telegram Bot API**: Interact with users through Telegram.
- **RapidAPI**: Provides data related to Indian Railways via the IRCTC API.

## 📦 API Used

- **IRCTC API on RapidAPI**:
  - [API Documentation](https://rapidapi.com/IRCTCAPI/api/irctc1/playground/apiendpoint_3cdbbdeb-1ef6-44de-9515-38d253e9b9de)
  - Used to fetch train fare, station search results, seat availability, and more.
  
## ⚙️ Prerequisites

Before running this project, ensure you have the following:

1. **Telegram Bot Token**: Get one by creating a bot using [BotFather](https://core.telegram.org/bots#botfather).
2. **RapidAPI Key**: Sign up at [RapidAPI](https://rapidapi.com) and subscribe to the IRCTC API to obtain the key.

## 🔧 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/railway-telegram-bot.git
    cd railway-telegram-bot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
   - Create a `.env` file and add your credentials:
    ```env
    TELEGRAM_BOT_TOKEN=your-telegram-bot-token
    RAPID_API_KEY=your-rapid-api-key
    ```

4. **Run the bot**:
    ```bash
    python bot.py
    ```

## 🚀 How to Use

1. **Start the Bot**: Type `/start` to begin.
2. **Use Menu**: Choose from the available options (Fare Info, Train Status, etc.).
3. **Search Station**: Type the station code or name to search for stations.
4. **Fare Enquiry**: Enter the train number, from station, and to station to get fare details.

### Automated Prompt
- After 30 seconds of inactivity, the bot will ask:
  ```
  What else can I help you with?
  ```
  If you respond **Yes**, the bot shows the main menu again. If you respond **No**, the bot stops.

## 🐛 Troubleshooting

If you encounter any issues, make sure:
- The bot token and RapidAPI key are correct.
- The API quota has not been exceeded.

## 📝 License

This project is licensed under the MIT License.

---

Feel free to modify the template as needed!
