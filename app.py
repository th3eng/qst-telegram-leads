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

print("="*20)
print("Thndelegram bot V0.1")
print("="*20)
print("This bot is used to collect leads from users and store them in a CSV file")
print("="*20)
print("Coded by: Ahmed Farag")
print("="*20)
print("Status: Running\nEnjoy!")
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
        # record the details in the CSV file
        with open(FILE_NAME, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(details)
        # Updating step to end
        context.user_data['name']=None
        context.user_data['email']=None
        context.user_data['phone']=None

        if context.user_data.get('language') == 'Arabic':
            await update.message.reply_text('شكرا لك لقد تم تسجيلك بنجاح !🫡\nيمكنك التواصل مع الدعم من هنا @Octopus_support_2')
        else:
            await update.message.reply_text('Thank you for registering!🫡\nContact the support now: @Octopus_support_2')
    
    elif bool(re.match(pattern1, update.message.text)):
        context.user_data['name']=update.message.text
        if context.user_data.get('email') is not None and context.user_data.get('name') is not None and context.user_data.get('phone') is not None:
            # store the data
            with open(FILE_NAME, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([context.user_data.get('name'), context.user_data.get('email'), context.user_data.get('phone')])
            # Updating step to end
            context.user_data['name']=None
            context.user_data['email']=None
            context.user_data['phone']=None
            if context.user_data.get('language') == 'Arabic':
                await update.message.reply_text('شكرا لك لقد تم تسجيلك بنجاح !🫡\nيمكنك التواصل مع الدعم من هنا @Octopus_support_2')
            else:
                await update.message.reply_text('Thank you for registering!🫡\nContact the support now: @Octopus_support_2')

        if context.user_data.get('language') == 'Arabic':
            # Replace with an Arabic message to get email
            await update.message.reply_text('من فضلك أرسل بريدك الإلكتروني📧')
        else:
            await update.message.reply_text('Please send your email📧')
    
    elif bool(re.match(pattern2, update.message.text)):
        context.user_data['email']=update.message.text
        if context.user_data.get('email') is not None and context.user_data.get('name') is not None and context.user_data.get('phone') is not None:
            # store the data
            with open(FILE_NAME, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([context.user_data.get('name'), context.user_data.get('email'), context.user_data.get('phone')])
            # Updating step to end
            context.user_data['name']=None
            context.user_data['email']=None
            context.user_data['phone']=None
            if context.user_data.get('language') == 'Arabic':
                await update.message.reply_text('شكرا لك لقد تم تسجيلك بنجاح !🫡\nيمكنك التواصل مع الدعم من هنا @Octopus_support_2')
            else:
                await update.message.reply_text('Thank you for registering!🫡\nContact the support now: @Octopus_support_2')
            return

        # the email is stored, and now send message to get phone
        if context.user_data.get('language') == 'Arabic':
            # Replace with an Arabic message to get phone
            await update.message.reply_text('من فضلك أرسل رقم هاتفك📱')
        else:
            await update.message.reply_text('Please send your phone number📱')
    elif bool(re.match(pattern3, update.message.text)):
        context.user_data['phone']=update.message.text
        if context.user_data.get('email') is not None and context.user_data.get('name') is not None and context.user_data.get('phone') is not None:
            # store the data
            with open(FILE_NAME, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([context.user_data.get('name'), context.user_data.get('email'), context.user_data.get('phone')])
            if context.user_data.get('language') == 'Arabic':
                await update.message.reply_text('شكرا لك لقد تم تسجيلك بنجاح !🫡\nيمكنك التواصل مع الدعم من هنا @Octopus_support_2')
            else:
                await update.message.reply_text('Thank you for registering!🫡\nContact the support now: @Octopus_support_2')
            
            # Updating step to end
            context.user_data['name']=None
            context.user_data['email']=None
            context.user_data['phone']=None
    
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
