import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import newPortfolio
import stockoperation

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="To begin, type /initiate. Next you can you /chart or /report to get insight of your investment")
async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("C:/Users/Admin/Desktop/piechart.png", 'rb'))
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("C:/Users/Admin/Desktop/report.txt", 'r') as file:
        content = file.read()
    await context.bot.send_message(chat_id=update.effective_chat.id, text = content)
async def initiate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    newPortfolio.mainControl()
    context.bot.send_message(chat_id=update.effective_chat.id, text = "DONE")

async def news(update: Update, context = ContextTypes.DEFAULT_TYPE):
    stockoperation.news()
    with open('C:/Users/Admin/Desktop/news.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    await context.bot.send_message(chat_id=update.effective_chat.id, text = content)
if __name__ == '__main__':
    application = ApplicationBuilder().token('7286877896:AAFiiaHlwAS9HE-wdvYhPTN5NIJb8zD0hyM').build()
    
    start_handler = CommandHandler('start', start)
    
    photo_handler = CommandHandler('chart', chart)
    report_handler = CommandHandler('report', report)
    initiate_handler = CommandHandler('initiate', initiate)
    news_handler = CommandHandler('news', news)

    application.add_handler(start_handler)
    application.add_handler(photo_handler)
    application.add_handler(report_handler)
    application.add_handler(initiate_handler)
    application.add_handler(news_handler)

    application.run_polling()
    