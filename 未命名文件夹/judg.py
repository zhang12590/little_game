def judgment(gamelist):
    pass
    L = []
    for i in gamelist:
        L.append(i.result)
    maxvalue = max(L)
    maxvaluecount = L.count(maxvalue)
    for j in gamelist:
        if j.result == maxvalue:
            j.moneychange = len(L) / maxvaluecount
        else:
            j.moneychange = -1.0
