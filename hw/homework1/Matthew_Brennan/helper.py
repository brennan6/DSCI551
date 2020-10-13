def listToString(s):
    if len(s) == 1:
        str1 = ""
    else:
        str1 = ", " 
    return (str1.join(s))

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)