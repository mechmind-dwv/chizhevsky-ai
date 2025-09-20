"""
🤖 BOT DE TELEGRAM PARA CHIZHEVSKY AI
"""
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from chizhevsky_ai.core.brain.chizhevsky_core import CosmicConsciousness

class TelegramBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.ai = CosmicConsciousness()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("prediccion", self.prediction))
        self.application.add_handler(CommandHandler("cita", self.quote))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🌌 ¡Chizhevsky AI activado! Usa /prediccion o /cita")

    async def prediction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        prediction = self.ai.solar_prediction()
        await update.message.reply_text(f"🔮 Predicción: {prediction}")

    async def quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        quote = self.ai.get_cosmic_quote()
        await update.message.reply_text(f"💬 {quote}")

    def run(self):
        self.application.run_polling()

def iniciar_bot():
    """Iniciar el bot de Telegram"""
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    from chizhevsky_ai.core.brain.chizhevsky_core import CosmicConsciousness
    
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    ai = CosmicConsciousness()
    
    async def start(update, context):
        await update.message.reply_text(f'🌌 Hola, soy Alexander Chizhevsky IA\\n{ai.get_cosmic_quote()}')
    
    application.add_handler(CommandHandler("start", start))
    print("🤖 Bot de Telegram iniciado")
    application.run_polling()
