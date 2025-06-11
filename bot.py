from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# Токен и chat_id группы
TOKEN = '8032278690:AAGSOSKz161dujSV03mbra6W71qOZ_4t-S0'
GROUP_CHAT_ID = -1002203558146

# Клавиатура с двумя кнопками
keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📤 Попросити допомогу")],
        [KeyboardButton("🙏 Подякувати")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Главная логика
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_type = message.chat.type
    text = message.text

    # Разрешаем только кнопки, игнорируем весь остальной текст в группе
    if chat_type != "private" and text not in ["📤 Потрібна допомога", "🙏 Подякувати"]:
        return

    # Обработка кнопок
    if text == "📤 Потрібна допомога":
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text="🔔 Потрібна допомога! instagram: @Vladosss991 @vikTyzz @Milajust @Bereshchenko13"
        )
        if chat_type == "private":
            await message.reply_text("✅ Повідомлення про допомогу надіслано!", reply_markup=keyboard)

    elif text == "🙏 Подякувати":
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text="🙏 Вельми дякую! instagram: @Vladosss991 @vikTyzz @Milajust @Bereshchenko13"
        )
        if chat_type == "private":
            await message.reply_text("✅ Подяка надіслана!", reply_markup=keyboard)

    elif chat_type == "private":
        # В личке — показать меню
        await message.reply_text("Оберіть дію з кнопок нижче 👇", reply_markup=keyboard)

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен. Мовчить у групі, але реагує на кнопки.")
    app.run_polling()
import asyncio
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running")

async def run_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=10000)
    await site.start()

if __name__ == '__main__':
    asyncio.get_event_loop().create_task(run_server())  # ← фоновый веб-сервер
    main()

