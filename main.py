import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import requests
import json

import mongo


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


def itemSearch(item_name):
    x = requests.get(
        'https://cafemaker.wakingsands.com/search?string=' + item_name)
    y = json.loads(x.text)
    results = y['Results']

    name_id_dict = {}
    for i in results:
        if i['UrlType'] in accepted_types:
            name_id_dict[i['Name']] = i['ID']

    return name_id_dict


def itemSearchDictFormat(dic):
    out = ''
    for key in dic:
        out += key + ': [' + str(dic[key]) + ']' + '(' + \
            'https://universalis.app/market/' + str(dic[key]) + ')\n'

    return out


def itemInfo(item_id, listings_count=20, entries=5, noGst=0):
    if world_search:
        x = requests.get(
            'https://universalis.app/api/v2/' + world + '/' + item_id + '?listings=' + str(listings_count) + '&entries=' + str(entries) + '&noGst=' + str(noGst))
    else:
        x = requests.get(
            'https://universalis.app/api/v2/' + datacenter + '/' + item_id + '?listings=' + str(listings_count) + '&entries=' + str(entries) + '&noGst=' + str(noGst))

    # print(x.text)
    y = json.loads(x.text)

    # push to mongoDB
    mongo.pyMongoPush(y)

    return y


def itemInfoDictFormat(y):
    out = ''

    listings = y['listings']
    # recentHistory = y['recentHistory']

    # listingAveragePrice = str(y['currentAveragePrice']).replace('.', '\.')
    # listingAveragePriceHQ = str(y['currentAveragePriceHQ']).replace('.', '\.')
    # salesAveragePrice = str(y['averagePrice']).replace('.', '\.')
    # salesAveragePriceHQ = str(y['averagePriceHQ']).replace('.', '\.')
    # historyMinPrice = str(y['minPrice'])
    # historyMinPriceHQ = str(y['minPriceHQ'])
    # historyMaxPrice = str(y['maxPrice'])
    # historyMaxPriceHQ = str(y['maxPriceHQ'])

    # out += '_listings:_\n'
    # out += '_avg: ' + listingAveragePrice + '_\n'
    # out += '_avg \(HQ\): ' + listingAveragePriceHQ + '_\n'
    # out += '\n'

    # out += 'sales:\n'
    # out += 'avg: ' + salesAveragePrice + '\n'
    # out += 'avg \(HQ\): ' + salesAveragePriceHQ + '\n'
    # out += '\n'

    # out += 'historical:\n'
    # out += 'min: ' + historyMinPrice + '\n'
    # out += 'min \(HQ\): ' + historyMinPriceHQ + '\n'
    # out += 'max: ' + historyMaxPrice + '\n'
    # out += 'max \(HQ\): ' + historyMaxPriceHQ + '\n'
    # out += '\n'

    # out += 'listings:\n'
    for i in range(len(listings)):

        if listings[i]['worldName'] == world:
            out += '*'

        out += listings[i]['worldName'][0] + ' '

        if listings[i]['hq']:
            out += '__'

        out += str(listings[i]['pricePerUnit']) + \
            ' x' + str(listings[i]['quantity'])

        if listings[i]['hq']:
            out += '__'

        if listings[i]['worldName'] == world:
            out += '*'

        out += '\n'

    return out


async def textMain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(text)
    # print(type(text))   # <class 'str'>
    out = '/start'

    if text.isdigit():  # input is already an item ID
        out = itemInfoDictFormat(itemInfo(text))
    else:   # input is item name
        out = itemSearchDictFormat(itemSearch(text))

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
