from string import printable
from typing import List


CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def isnumber(n: str) -> bool:
    try:
        int(n, 36)
        return True
    except ValueError:
        return False


def to_new_base(num: int, new_base: int) -> str:
    out = ''
    while num > new_base-1:
        out = printable[num % new_base] + out
        num //= new_base
    return (printable[num] + out).upper()


class Expression:
    def __init__(self):
        self.value = ['0']
        self.base = 10

    def _change_base(self, new_base: int) -> List[str]:
        output = []
        for val in self.value:
            if '.' in val:
                output = ['0']
                break

            if '(' in val and ')' not in val:
                num = int(val.replace('(', ''), self.base)
                val = '(' + to_new_base(num, new_base)
            elif ')' in val and '(' not in val:
                num = int(val.replace('(', ''), self.base)
                val = to_new_base(num, new_base) + ')'
            elif '(' in val and ')' in val:
                num = int(val.replace('(','').replace(')', ''), self.base)
                val = '(' + to_new_base(num, new_base) + ')'
            elif isnumber(val):
                val = to_new_base(int(val, self.base), new_base)

            output.append(val)

        return output

    def set_base(self, base: int) -> None:
        self.value = self._change_base(base)
        self.base = base

    def insert(self, value: str) -> None:
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

    def clear(self) -> None:
        self.value = ['0']

    def trim(self) -> None:
        if len(self.value) == 1 and len(self.value[-1]) == 1:
            self.value[-1] = '0'

        if len(self.value) != 1 and len(self.value[-1]) == 1:
            self.value.pop(-1)

        if len(self.value[-1]) != 1:
            self.value[-1] = self.value[-1][:-1]

    def eval(self) -> None:
        old_base = self.base
        try:
            if self.base != 10:
                self.set_base(10)
                expr = eval(''.join(self.value).replace('^', '**'))
                self.set_base(old_base)
                self.value = [to_new_base(expr, old_base)]
            else:
                expr = eval(''.join(self.value).replace('^', '**'))
                self.value = [str(expr)]
        except:
            self.value = ['ERROR']
