import requests
import json

# https://xivapi.com/docs/Search#search (Accepts: Achievement, Title, Action, CraftAction, Trait, PvPAction, PvPTrait, Status, BNpcName, ENpcResident, Companion, Mount, Leve, Emote, InstanceContent, Item, Recipe, Fate, Quest, ContentFinderCondition, Balloon, BuddyEquip, Orchestrion, PlaceName, Weather, World, Map, lore_finder)
accepted_types = ['Item', 'Mount', 'Balloon', 'BuddyEquip', 'Orchestrion']


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
