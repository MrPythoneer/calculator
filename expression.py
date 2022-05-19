from string import printable


def isdigit(value):
    try:
        int(value, 36)
        return True
    except:
        return False


def convertNumber(num, base):
    out = ''
    while num > base-1:
        out = printable[num % base] + out
        num //= base
    return (printable[num] + out).upper()


class Expression:
    def __init__(self):
        self.value = ['0']
        self.base = 10

    def _changeBase(self, new_base):
        output = []
        for val in self.value:
            if '.' in val:
                output = ['0']
                break

            if '(' in val and ')' not in val:
                val = '(' + convertNumber(int(val.replace('(', ''),
                                              self.base), new_base)
            elif ')' in val and '(' not in val:
                val = convertNumber(
                    int(val.replace('(', ''), self.base), new_base) + ')'
            elif '(' in val and ')' in val:
                val = '(' + convertNumber(int(val.replace('(',
                                                          '').replace(')', ''), self.base), new_base) + ')'
            elif isdigit(val):
                val = convertNumber(int(val, self.base), new_base)
            output.append(val)

        return output

    def changeBase(self, base):
        self.value = self._changeBase(base)
        self.base = base

    def add(self, value):
        if value in '.0123456789ABCDE()':
            if self.value[-1] == '0' and value != '.':
                self.value[-1] = value
            elif self.value[-1] in '.*+-/^':
                if value == '.':
                    self.value.append('0.')
                else:
                    self.value += value
            else:
                self.value[-1] += value

        elif value in '*+-/^':
            if self.value[-1][-1] in '0123456789ABCDE()':
                self.value.append(value)
            else:
                self.value[-1] = value

    def clear(self):
        self.value = ['0']

    def trim(self):
        if len(self.value) == 1 and len(self.value[-1]) == 1:
            self.value[-1] = '0'

        if len(self.value) != 1 and len(self.value[-1]) == 1:
            self.value.pop(-1)

        if len(self.value[-1]) != 1:
            self.value[-1] = self.value[-1][:-1]

    def eval(self):
        old_base = self.base
        try:
            if self.base != 10:
                self.changeBase(10)
                expr = eval(''.join(self.value).replace('^', '**'))
                self.changeBase(old_base)
                self.value = [convertNumber(expr, old_base)]
            else:
                expr = eval(''.join(self.value).replace('^', '**'))
                self.value = [str(expr)]
        except:
            self.value = ['ERROR']
