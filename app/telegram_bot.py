import json
import random

from telegram import BotCommand, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler

from app.integrations.integration_client import IntegrationClient
from app.logging.logging_utils import log, LogLevel, LogCustomMessage
from app.utils import localized_text


class ChatTelegramBot:
    """
    Class Telegram Bot
    """

    def __init__(
            self,
            config: dict
    ):
        self.config = config
        self.commands = [
            BotCommand(
                command='help',
                description='test_help'
            ),
            BotCommand(
                command='start',
                description='start_text'
            )
        ]
        self.usage = {}
        self.last_message = {}

    async def start(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Хочу загадку", callback_data="riddle"),
                InlineKeyboardButton("Правила", callback_data="rule"),
            ],
            [InlineKeyboardButton("Присоединиться в группу", callback_data="3")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        greeting_text = f"Привет! {update.message.from_user.name}! \n\nЯ бот с загадками. "
        description_text = localized_text('start_text')[0]

        start_text = greeting_text + description_text + '\n\n' + localized_text('start_text')[1]
        await update.message.reply_text(start_text, reply_markup=reply_markup)

    async def get_riddle_text(self):
        client = IntegrationClient()
        return await client.get_riddle_text()

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        answer = "Тестовое сообщение"
        keyboard = [
            [
                InlineKeyboardButton("Хочу еще", callback_data="yet_riddle"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.data == 'riddle':
            answer = await self.get_riddle_text()
        elif query.data == 'yet_riddle':
            answer = "Еще одна загадка"
        elif query.data == 'rule':
            answer = "Правила:"

        await update.callback_query.message.reply_text(
            text=f"Загадка: {answer}",
            reply_markup=reply_markup
        )

    async def post_init(self, application: Application) -> None:
        await application.bot.set_my_commands(self.commands)

    def run(self):
        application = ApplicationBuilder() \
            .token(self.config['token']) \
            .post_init(self.post_init) \
            .build()
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CallbackQueryHandler(self.button))
        application.run_polling()

