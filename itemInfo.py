import requests
import json

import mongo

world_search = 0
datacenter = '猫小胖'
world = '摩杜纳'


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
