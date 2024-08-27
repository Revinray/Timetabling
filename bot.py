import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from check import freenow, freeuntil, freewhen
from visual import generate_timetable_image
import json
from flask import Flask, request
import asyncio
import nest_asyncio
from environment import BOT_TOKEN, NGROK_URL, NGROK_PORT

# Initialize Flask app
app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states for the ConversationHandler
NAME, COLOR, URL = range(3)

def get_timetables_info(chat_id):
    """Read and return the timetable information from the chat store."""
    try:
        with open(f'chat_store/{chat_id}_timetables_info.json', 'r') as file:
            timetables_info = json.load(file)
    except FileNotFoundError:
        timetables_info = {}
    return timetables_info

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Available commands:\n/freenow - Check who is free now\n/freeuntil - Check who is free and until when\n/freewhen <name> - Check when a specific person is free next\n/timetable - Generate and display the timetable\n/maketimetable - Create a new timetable")

async def freenow_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the list of students who are free now."""
    free_students = freenow()
    await update.message.reply_text(f"Students who are free now: {', '.join(free_students)}")

async def freeuntil_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the list of students who are free and until when."""
    free_until = freeuntil()
    response = "\n".join([f"{name} is free until {time}" for name, time in free_until.items()])
    await update.message.reply_text(f"Students who are free and until when:\n{response}")

async def freewhen_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the next free time for a specific student."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /freewhen <name>")
        return
    name = context.args[0]
    next_free_time = freewhen(name)
    await update.message.reply_text(f"{name} is next free at: {next_free_time}")

async def timetable_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate and send the timetable image."""
    chat_id = update.message.chat_id
    timetables_info = get_timetables_info(chat_id)
    image_path = generate_timetable_image(timetables_info)
    await update.message.reply_photo(photo=open(image_path, 'rb'))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text("An error occurred. Please try again later.")

async def maketimetable_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the maketimetable conversation and ask for the name."""
    await update.message.reply_text("Please provide the name for the timetable:")
    return NAME

async def received_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the name and ask for the color."""
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Received name. Please provide the color for the timetable:")
    return COLOR

async def received_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the color and ask for the NUS URL."""
    context.user_data['color'] = update.message.text
    await update.message.reply_text("Received color. Please provide the NUS URL for the timetable:")
    return URL

async def received_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the NUS URL and save the timetable information."""
    context.user_data['url'] = update.message.text
    chat_id = update.message.chat_id
    timetables_info = get_timetables_info(chat_id)
    timetables_info[context.user_data['name']] = {
        'url': context.user_data['url'],
        'name': context.user_data['name'],
        'color': context.user_data['color']
    }
    with open(f'chat_store/{chat_id}_timetables_info.json', 'w') as file:
        json.dump(timetables_info, file)
    await update.message.reply_text("Timetable information saved successfully!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text("Timetable creation cancelled.")
    return ConversationHandler.END

# Initialize the bot application
application = Application.builder().token(BOT_TOKEN).build()

# Add command handlers to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("freenow", freenow_command))
application.add_handler(CommandHandler("freeuntil", freeuntil_command))
application.add_handler(CommandHandler("freewhen", freewhen_command))
application.add_handler(CommandHandler("timetable", timetable_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Add error handler to the application
application.add_error_handler(error_handler)

# Add ConversationHandler for maketimetable
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('maketimetable', maketimetable_start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_name)],
        COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_color)],
        URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_url)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

application.add_handler(conv_handler)

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