
def rock_formula(bands):
    b1 = bands[0]
    b2 = bands[1]
    b3 = bands[2]
    if (b1 < b2) and (b1 < b3) and (b3 >= b2) and (b3 - b2 <= 5) and (b2 >= 165):
        mask_value = 1
    else:
        mask_value = 0
    return mask_value


def ndvi(bands):
    return (bands[119] - bands[72]) / (bands[119] + bands[72])


def pssr(bands):
    return bands[119] / bands[72]


def gndvi(bands):
    return (bands[119] - bands[42]) / (bands[119] + bands[42])


def mcari(bands):
    return 1.2 * (2.5 * (bands[108] - bands[72]) - 1.3 * (bands[108] - bands[40]))


def wbi(bands):
    return bands[155] / bands[136]



