from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ADMIN_CHAT_ID = "1905981428"  # Replace with your admin chat ID

# Start command
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("\u2714\ufe0f خرید سرویس", callback_data='buy_service')],
        [InlineKeyboardButton("\u2714\ufe0f شارژ کیف پول", callback_data='charge_wallet')],
        [InlineKeyboardButton("\u2714\ufe0f لینک نرم افزارها", callback_data='software_links')],
        [InlineKeyboardButton("\u2714\ufe0f پیام به پشتیبانی", callback_data='support')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "خوش آمدید! از خدمات ما استفاده کنید:\n\n",
        reply_markup=reply_markup
    )

# Callback handler for menu actions
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'buy_service':
        buy_service_menu(query)
    elif query.data == 'charge_wallet':
        query.edit_message_text(
            text="برای شارژ کیف پول خود، مبلغ موردنظر را ارسال کنید (مثال: 50000):"
        )
    elif query.data == 'software_links':
        query.edit_message_text(
            text="لینک نرم افزارها:\n\n1. نرم افزار A: [لینک](https://example.com)\n2. نرم افزار B: [لینک](https://example.com)",
            parse_mode='Markdown'
        )
    elif query.data == 'support':
        query.edit_message_text(
            text=f"برای ارتباط با پشتیبانی، به این آیدی پیام دهید: @YourAdminUsername"
        )

# Buy service menu
def buy_service_menu(query):
    keyboard = [
        [InlineKeyboardButton("\u2714\ufe0f سرور همراه اول", callback_data='mci_server')],
        [InlineKeyboardButton("\u2714\ufe0f سرور ایرانسل", callback_data='irancell_server')],
        [InlineKeyboardButton("\u2714\ufe0f سرور همه اپراتورها", callback_data='all_servers')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("انتخاب نوع سرور:", reply_markup=reply_markup)

# Handle text messages
def handle_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    if user_message.isdigit():
        # User sends amount to charge wallet
        amount = int(user_message)
        update.message.reply_text(
            f"برای شارژ کیف پول {amount} تومان، مبلغ را به شماره کارت زیر واریز کنید:\n\n" +
            "`1234-5678-9012-3456`\n\n" +
            "سپس اسکرین شات فیش واریزی را ارسال کنید.",
            parse_mode='Markdown'
        )
    else:
        update.message.reply_text("پیام شما ثبت شد و به پشتیبانی ارسال می‌شود.")
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"پیام جدید از کاربر {chat_id}:\n{user_message}")

# Handle photos (screenshot of receipt)
def handle_photo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    photo = update.message.photo[-1]  # Get highest resolution photo
    caption = update.message.caption or "بدون توضیح"

    # Forward photo to admin
    context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo.file_id, caption=f"عکس واریزی از کاربر {chat_id}:\n{caption}")

    update.message.reply_text("عکس شما به پشتیبانی ارسال شد. منتظر بررسی باشید.")

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update caused error: %s', context.error)

# Main function
def main() -> None:
    updater = Updater("7291885432:AAGeSVC9j5QoYvrDR08FrwwKDuOr37k3MjU")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
