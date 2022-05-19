import tkinter


def convert(base, num, new_base):
    def toDigits(n, b):
        digits = ''
        lst = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
        while n > 0:
            a = n % b
            a = a in lst and lst[a] or str(a)
            digits = a + digits
            n = n // b
        return digits

    n = int(str(num), base)
    return toDigits(n, new_base)


def formatnum(x):
    if int(x) == x:
        return int(x)
    else:
        return x


def evaluate(expr, l=22):
    if expr == '':
        return '0'
    try:
        result = eval(expr.replace('^', '**'))
        if len(str(result)) >= l:
            result = '{:e}'.format(result)
        return str(formatnum(result))
    except:
        return 'ERROR'


def isnum(num):
    return num.replace('.', '').isdigit()


class GUI:
    def __init__(self, master):
        self.expr = ['']
        self.base = 10

        self.b_size = (10, 4)
        self.grid = [
            ['+', '-', '*', '/', 'bin'],
            ['7', '8', '9', 'CE', 'dec'],
            ['4', '5', '6', '<', 'oct'],
            ['1', '2', '3', '.', 'duo'],
            ['^', '0', 'concat', '=', 'hex']
        ]
        self.style = {
            '.': {'text': '•'},
            '=': {'bg': '#FF7F27'}
        }

        self.master = master
        master.title('Calculator')
        master.geometry('{}x423'.format(
            22*self.b_size[1]*len(self.grid[0])+10))

        self.entry_font = 'Fixedsys 24'
        self.b_font = 'Fixedsys 12'

        self.view = tkinter.Entry(
            master, justify='right', font=self.entry_font, state='readonly')
        self.entry = tkinter.Entry(
            master, justify='right', font=self.entry_font, state='readonly')

        self.view.grid(row=0, column=0, columnspan=len(
            self.grid[0]), sticky='we')
        self.entry.grid(row=1, column=0, columnspan=len(
            self.grid[0]), sticky='we')
        self.putButtons()

    def putButtons(self):
        for y, yval in enumerate(self.grid):
            for x, xval in enumerate(yval):
                self.button(xval, x, y+2)

    def update(self):
        self.view['state'] = 'normal'
        self.entry['state'] = 'normal'

        self.view.delete(0, 'end')
        self.view.insert(0, ''.join(self.expr[:-1]))

        self.entry.delete(0, 'end')
        self.entry.insert(0, len(self.expr) == 0 and '' or self.expr[-1])

        self.entry['state'] = 'readonly'
        self.view['state'] = 'readonly'

    def handler(self, value):
        if 'ERROR' in self.expr:
            self.expr = ['']
        if value in '0123456789.':
            if self.expr[-1] == '':
                self.expr[-1] = value
            elif self.expr[-1][-1] in '0123456789.':
                self.expr[-1] += value
        else:
            self.expr.append('')

        if value == '=':
            self.expr = [evaluate(''.join(self.expr))]
        elif value in '/*+-^':
            if isnum(self.expr[-2]):
                self.expr[-1] = value
                self.expr.append('')
        elif value == '<':
            self.expr.pop(-1)

            while self.expr[-1] == '':
                self.expr.pop(-1)
            self.expr[-1] = self.expr[-1][:-1]
        elif value == 'CE':
            self.expr = ['']
        elif value == 'bin':
            self.changeBase(2)
        self.expr[-1] = self.expr[-1][0:10]

        self.update()

    def button(self, value, x, y, padding=0):
        width, height = self.b_size
        btn = tkinter.Button(self.master, text=value, command=lambda: self.handler(
            value), width=width, height=height, font=self.b_font)

        if value in self.style:
            for i in self.style[value]:
                btn[i] = self.style[value][i]

        btn.grid(row=y, column=x, padx=padding, pady=padding)
        return btn

    def changeBase(self, base):
        for i, v in enumerate(self.expr):
            if isnum(v):
                self.expr[i] = convert(self.base, v, base)
        self.base = base
        self.update()


root = tkinter.Tk()
gui = GUI(root)
root.mainloop()
