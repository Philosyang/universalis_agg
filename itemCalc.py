import numpy as np

# y: universalis api return dict
# colname: 'listings' or 'recentHistory' or else, must contain 'pricePerUnit'
# hq: -1 means calc ignoring NQ/HQ status, 0 means calc only NQ, 1 means calc only HQ


def columnMedian(y, colName='listings', hq=-1):
    listings = y[colName]
    # pricePerUnitList = []   # 180, 180, 181, 190, 190
    # quantityList = []   # 1, 99, 99, 36, 19
    combinedList = []   # 180, 180 (repeat 99 times), 181 (repeat 99 times)...

    if hq == -1:
        for i in range(len(listings)):
            combinedList.extend([listings[i]['pricePerUnit']] * listings[i]['quantity'])
    elif hq == 0:
        for i in range(len(listings)):
            if not listings[i]['hq']:
                combinedList.extend([listings[i]['pricePerUnit']] * listings[i]['quantity'])
    else:   # hq == 1
        for i in range(len(listings)):
            if listings[i]['hq']:
                combinedList.extend([listings[i]['pricePerUnit']] * listings[i]['quantity'])

    if len(combinedList) < 9:
        return [np.round(np.median(combinedList), 2), np.round(np.median(combinedList), 2), np.round(np.median(combinedList), 2)]
    elif len(combinedList) < 99:
        return [np.round(np.median(combinedList[:9]), 2), np.round(np.median(combinedList), 2), np.round(np.median(combinedList), 2)]
    
    return [np.round(np.median(combinedList[:9]), 2), np.round(np.median(combinedList[:99]), 2), np.round(np.median(combinedList), 2)]
