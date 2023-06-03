import numpy as np

# y: universalis api return dict
# colname: 'listings' or 'recentHistory' or else, must contain 'pricePerUnit'
# hq: -1 means calc ignoring NQ/HQ status, 0 means calc only NQ, 1 means calc only HQ


def columnMedian(y, colName='listings', hq=-1):
    listings = y[colName]
    pricePerUnitList = []

    if hq == -1:
        for i in range(len(listings)):
            pricePerUnitList.append(listings[i]['pricePerUnit'])
    elif hq == 0:
        for i in range(len(listings)):
            if not listings[i]['hq']:
                pricePerUnitList.append(listings[i]['pricePerUnit'])
    else:   # hq == 1
        for i in range(len(listings)):
            if listings[i]['hq']:
                pricePerUnitList.append(listings[i]['pricePerUnit'])

    return np.round(np.median(pricePerUnitList), 2)
