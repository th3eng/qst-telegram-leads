from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import csv, re

TOKEN = "6572624563:AAH_Ff5055ByAlB_Q52r82gu67FePXR1okA"

# Define our CSV file name
FILE_NAME = "lead_data.csv"

#data format three lines
pattern = r"^(.+)\n(.+)\n(.+)$"
# regx must be: first name and last name and have space between them
pattern1 = r"^(.+)\s(.+)$"
# regx must be: email
pattern2 = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
# regx must be: phone number with or without + sign
pattern3 = r"^\+?[0-9]+$"

# Validate the details
def validate_details(details: str) -> bool:
    return bool(re.match(pattern, details.replace('\n\n','\n')))

# Start command
async def start(update: Update, context: CallbackContext) -> None :
    keyboard = [['Arabic', 'English']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Welcome 😃.\nSelect your language, please 😉', reply_markup=reply_markup)

# Handle language selection
async def handle_language(update: Update, context: CallbackContext) -> None:
    chosen_language = update.message.text
    if chosen_language == "Arabic":
        context.user_data['language'] = 'Arabic'
        # You can replace the below text with the Arabic equivalent
        await update.message.reply_text("من فضلك أرسل بياناتك بالصيغة التالية:\n\nالاسم الكامل\nالبريد الإلكتروني\nرقم الهاتف مع رمز البلد")
    elif chosen_language == "English":
        context.user_data['language'] = 'English'
        await update.message.reply_text("Please send your details in the following format:\n\nFull name\nEmail address\nPhone number with country code")

# Handle the user details
async def handle_details(update: Update, context: CallbackContext) -> None:
    if validate_details(update.message.text):  # Check if there are three lines for name, email, and phone
        details = update.message.text.replace('\n\n','\n').split('\n')
        if not bool(re.match(pattern1, details[0])):
            await update.message.reply_text('Your name is not correct😥\n' + details[0])
            return
        if not bool(re.match(pattern2, details[1])):
            await update.message.reply_text('Your email is not correct😥\n' + details[1])
            return
        if not bool(re.match(pattern3, details[2])):
            await update.message.reply_text('Your phone number is not correct😥\n' + details[2])
            return
        with open(FILE_NAME, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(details)
        if context.user_data.get('language') == 'Arabic':
            # Replace with an Arabic thank you message
            await update.message.reply_text('شكرا لك لقد تم تسجيلك بنجاح !🫡')
        else:
            await update.message.reply_text('Thank you for registering!🫡')
    else:
        if context.user_data.get('language') == 'Arabic':
            # Replace with an Arabic error message
            await update.message.reply_text('الصيغة غير صحيحة🤕\nمن فضلك أرسل بياناتك بالصيغة المحددة🙏')
        else:
            await update.message.reply_text('Incorrect format🤕\nPlease send your details in the specified format🙏')

def main() -> None:
    # Get the dispatcher to register handlers
    dp = ApplicationBuilder().token(TOKEN).build()

    # on different commands
    dp.add_handler(CommandHandler("start", start))

    #handle language selection message
    dp.add_handler(MessageHandler(filters.Regex('^(Arabic|English|arabic|english)$'), handle_language))

    # add handler to handle the other messages not three lines
    dp.add_handler(MessageHandler(filters.ALL, handle_details))

    # Start the Bot
    dp.run_polling()

if __name__ == '__main__':
    main()
