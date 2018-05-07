def encrypt(st, key): 
    if len(st) != len(key): 
        return "Text and Key have to be the same length."
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    nText = []
    kText = []
    for i in range(len(st)):
        if (st[i] in alphabet) == True:
            nText.append(alphabet.index(st[i].lower()))
            kText.append(alphabet.index(key[i].lower()))
        else:
            nText.append(st[i])
            kText.append(st[i])
    #nText.append(alphabet.index(st[i].lower()))
    #kText.append(alphabet.index(key[i].lower()))
    out = "" 
    for i in range(len(nText)):
        if type(nText[i]) == int:
            out += alphabet[(nText[i] + kText[i]) % len(alphabet)]
        else:
            out += nText[i]
    return out;
