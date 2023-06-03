import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import itemSearch as itemS
import itemInfo as itemI


bot_token = 'put token in file bot_token'
with open('bot_token', 'r') as reader:
    bot_token = reader.read()

# https://xivapi.com/docs/Search#search (Accepts: Achievement, Title, Action, CraftAction, Trait, PvPAction, PvPTrait, Status, BNpcName, ENpcResident, Companion, Mount, Leve, Emote, InstanceContent, Item, Recipe, Fate, Quest, ContentFinderCondition, Balloon, BuddyEquip, Orchestrion, PlaceName, Weather, World, Map, lore_finder)
accepted_types = ['Item', 'Mount', 'Balloon', 'BuddyEquip', 'Orchestrion']
world_search = 0
datacenter = '猫小胖'
world = '摩杜纳'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/start")


async def textMain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(text)
    # print(type(text))   # <class 'str'>
    out = '/start'

    if text.isdigit():  # input is already an item ID
        out = itemI.itemInfoDictFormat(itemI.itemInfo(text))
    else:   # input is item name
        out = itemS.itemSearchDictFormat(itemS.itemSearch(text))

    print(out)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=out, parse_mode='MarkdownV2', disable_web_page_preview=True)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="0")

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    textMain_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), textMain)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(textMain_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
