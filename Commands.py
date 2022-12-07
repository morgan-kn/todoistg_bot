from telegram import ForceReply, Update
from telegram.ext import ContextTypes

import FileDB
import MemoryDB
from logger import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I can /add <text>, /list, /help",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("No one's gonna help you! DIY!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = ' '.join(update.message.text.split(' ')[1:])
    if task == '':
        await update.message.reply_text("Task can't be empty")
    else:
        user_id = update.effective_user.id
        if FileDB.FileDb.add(user_id, task):
            logger.info(update.message.from_user.id)
            await update.message.reply_text("Task \"{0}\" has been saved".format(task))
        else:
            logger.error("Couldn't save a task")


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks = FileDB.FileDb.get_list(update.effective_user.id)
    if len(tasks) == 0:
        await update.message.reply_text("You have no tasks")
    await update.message.reply_text('\n'.join(tasks))
