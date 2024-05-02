import random
def monoalphabetic(dictionary_file, ct, partial = {}, flag_format = "flag", tolerance_max = 20, nocolor = False, debug = 1):
    """Cracks a monoalphabetic substitution cipher

    :param dictionary_file: path to dictionary in plaintext's language
    :param ct: ciphertext as string
    :param partial: known part of the key, given as dictionary of uppercase characters, in {ct:pt} form. Defaults to {}
    :param flag_format: flag format, which gets added to the dictionary, defaults to "flag"
    :param tolerance_max: defines how many words outside the dictionary the plaintext can have, needs to be found by trial and error, defaults to 20
    :param nocolor: disable coloring of the decrypted part of the text, defaults to False
    :param debug: integer in range(0, 4), defaults to 1 : level 0 prints nothing,  
        level 1 prints the size of the biggest key found,\\
        level 2 prints the decrypted text whenever a bigger partial key is found, \\
        level 3 adds prints signaling whenever the backtracking exits or enters the function, useful to detect when thrashing happens \\
        level 4 prints which words, completely decrypted by the key are not in the dictionary
    :return: if it is found, the plaintext, otherwise None
    """    
    with open(dictionary_file) as f:
        dc = set(map(str.upper, map(str.strip, f.readlines())))
    dc.add(flag_format.upper())
    s = ''
    for x in ct:
        if x.isalpha():
            s += x.upper()
        else:
            s += ' '
    words = s.split()
    alphabet = set(filter(str.isalpha,map(str.upper, ct)))
    
    def sub_letter(sub, c):
        if c == c.lower():
            return sub[c.upper()].lower()
        return sub[c]

    def substitute(sub, x):
        return ''.join(['\033[32m'+sub_letter(sub, y)+'\033[0m' if y.upper() in sub else y for y in x])

    def substitute_no_color(sub, x):
        return ''.join([sub_letter(sub, y) if y.upper() in sub else y for y in x])

    if nocolor:
        substitute = substitute_no_color
    best = 0

    def btrack(sub, depth = 0):
        nonlocal best

        if all([x in sub for x in alphabet]):
            if debug >= 1:
                print("FINAL RESULT")
                print(substitute(sub, ct))
            return substitute_no_color(sub, ct)
        if debug >= 3:
            print(f"recursion depth = {depth}")
        if len(sub) > best:
            best = len(sub)
            if debug >= 1:
                print(f"best match = {best}")
            if debug >= 2:
                print(substitute(sub, ct))
        tolerance = tolerance_max
        targets = []
        for x in words:
            c = 0
            for y in x:
                if y not in sub:
                    c += 1
            if c > 0:
                targets += [(x, c)]
            if c == 0:
                if substitute_no_color(sub, x).upper() not in dc:
                    tolerance -= 1
                    if debug >= 4:
                        print(f"bad word : {substitute_no_color(sub, x)}")
            if tolerance <= 0:
                if debug >= 3:
                    print("exit, tolerance exceeded")
                return
        targets.sort(key = lambda x:(len(x[0]), -x[1]), reverse=True)
        targets = targets[:tolerance_max+1]

        for trg, _ in targets:
            for s in dc:
                if len(s) == len(trg):
                    no = False
                    for ti, si in zip(trg, s):
                        if ti in sub and sub[ti] != si:
                            no = True
                    if no:
                        continue
                    sub2 = sub.copy()
                    for ti, si in zip(trg, s):
                        sub2[ti] = si
                    if debug >= 3:
                        print(f"TARGET SUBSTITUTED : {substitute(sub, trg)} -> {substitute(sub2, trg)}")
                    ret = btrack(sub2, depth+1)
                    if ret is not None:
                        return ret
            if debug >= 3:
                print(f"no suitable substitution for word {substitute(sub, trg)}")
        if debug >= 3:
            print("exit, no possible substitution")
    return btrack(partial)
