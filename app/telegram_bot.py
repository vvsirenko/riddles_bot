import random

from telegram import BotCommand, Update
from telegram.ext import ContextTypes, Application, ApplicationBuilder, CommandHandler

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
            )
        ]
        self.usage = {}
        self.last_message = {}

    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Show the help menu
        """
        commands_description = [f'/{command.command} - {command.description}' for command in self.commands]
        help_text = (
                localized_text('help_text')[0]
        )
        await update.message.reply_text(help_text, disable_web_page_preview=True)

    async def post_init(self, application: Application) -> None:
        """
        Post initialization hook for the bot.
        """
        await application.bot.set_my_commands(self.commands)

    def run(self):
        """
        Runs the bot
        """
        application = ApplicationBuilder() \
            .token(self.config['token']) \
            .post_init(self.post_init) \
            .build()

        application.add_handler(CommandHandler('help', self.help))
        application.run_polling()

