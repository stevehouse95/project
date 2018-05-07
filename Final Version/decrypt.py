#
#
# Use: decrypt("eqnvz", "XMCKL")
# => "hello"
#
#
def decrypt(st, key):
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
            nText.append(st[i].lower())
            kText.append(key[i].lower())
    out = ""
    for i in range(len(nText)):
        if type(nText[i]) == int:
            op = (nText[i] - kText[i])
            if op < 0:
                x = len(alphabet) + op
            else:
                x = op % len(alphabet)
            out += alphabet[x]
        else:
            out += nText[i]
    return out;
