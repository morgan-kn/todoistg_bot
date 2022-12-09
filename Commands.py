from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import MySqlDB
from logger import logger
import json


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I can /add task_name, /list, /help",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = """I can /add <task> with some priority that you define. 
    I can show you all your tasks if you call list. """
    await update.message.reply_text(message)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = ' '.join(update.message.text.split(' ')[1:])
    if task == '':
        await update.message.reply_text("Task can't be empty")
    else:
        user_id = update.effective_user.id
        task_id = MySqlDB.MySqlDB.add(user_id, task)
        if task_id > 0:
            logger.info(update.message.from_user.id)

            keyboard = [[
                InlineKeyboardButton("Low",
                                     callback_data=json.dumps({'type': 'priority', 'task_id': task_id, 'priority': 0})),
                InlineKeyboardButton("Medium",
                                     callback_data=json.dumps({'type': 'priority', 'task_id': task_id, 'priority': 1})),
                InlineKeyboardButton("High",
                                     callback_data=json.dumps({'type': 'priority', 'task_id': task_id, 'priority': 2})),
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text("Please set priority:", reply_markup=reply_markup)
            # await update.message.reply_text("Task \"{0}\" has been saved".format(task))
        else:
            logger.error("Couldn't save a task")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    request = json.loads(update.callback_query.data)
    if request['type'] == "priority":
        await query.edit_message_text(text=f"Selected priority: {request['priority']}")
        MySqlDB.MySqlDB.set_priority(update.effective_user.id, request["task_id"], request["priority"])
    else:
        await query.edit_message_text(text=f"Unknown button")


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks = MySqlDB.MySqlDB.get_list(update.effective_user.id)
    if len(tasks) == 0:
        await update.message.reply_text("You have no tasks")
    await update.message.reply_text('\n'.join(map(lambda t : t["name"], tasks)))


async def filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    filter = ' '.join(update.message.text.split(' ')[1:])
    if filter == '':
        await update.message.reply_text("Filter can't be empty")
    else:
        tasks = MySqlDB.MySqlDB.get_list(update.effective_user.id, filter)
        await update.message.reply_text('\n'.join(map(lambda t : t["name"], tasks)))


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sorry, I have no idea what '{0}' means.".format(update.message.text))
