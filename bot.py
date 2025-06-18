import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from aiohttp import web

# Переменные из окружения
TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "-1002203558146"))

# Клавиатура
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📩 Потрібна допомога", callback_data="help")],
    [InlineKeyboardButton("🙏 Подякувати", callback_data="thanks")]
])

# Обработка кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print("Button pressed:", query.data)

    if query.data == "help":
        await context.bot.send_message(chat_id=GROUP_CHAT_ID,
                                       text="📢 Потрібна допомога! instagram: @Vladosss991 @vikTyzz @Milajust @Bereshchenko13")
    elif query.data == "thanks":
        await context.bot.send_message(chat_id=GROUP_CHAT_ID,
                                       text="🙏 Вельми дякую! instagram: @Vladosss991 @vikTyzz @Milajust @Bereshchenko13")

    await query.edit_message_text(text="✅ Повідомлення відправлено")

# Ответ на текст в личке
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text("Оберіть дію з кнопок нижче 👇", reply_markup=keyboard)

# Запуск Telegram-приложения
def create_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app

# Aiohttp-сервер для Render
async def start_web_server():
    async def handle(request):
        return web.Response(text="Bot is running")
    
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8000)))
    await site.start()
    print("🌐 Web server started")

# Основной запуск
async def main():
    app = create_bot()
    await app.initialize()
    await start_web_server()
    await app.start()
    await app.updater.start_polling()
    print("🚀 Bot started")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

