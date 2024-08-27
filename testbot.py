import logging
from flask import Flask, request
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import nest_asyncio
from environment import BOT_TOKEN, NGROK_URL, NGROK_PORT

# Initialize Flask app
app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

# Initialize the bot application
application = Application.builder().token(BOT_TOKEN).build()

# Add command handlers to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set the new event loop
    loop.run_until_complete(application.process_update(update))
    return 'ok'

if __name__ == '__main__':
    async def set_webhook_and_run():
        logger.info("starting the application")
        await application.initialize()  # Ensure the application is initialized
        logger.info("setting the webhook")
        await application.bot.set_webhook(url=NGROK_URL + '/webhook')
        logger.info("starting the Flask app")
        app.run(port=NGROK_PORT)

    # Run the asynchronous function
    nest_asyncio.apply()
    asyncio.run(set_webhook_and_run())