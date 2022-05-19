import tkinter


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
        return formatnum(result)
    except:
        return 'ERROR'


class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Calculator')
        master.geometry('359x388')

        self.entry_font = 'Fixedsys 24'
        self.b_font = 'Fixedsys 12'

        self.entry = tkinter.Entry(
            master, justify='right', font=self.entry_font, state='readonly')

        self.b_size = (10, 4)
        self.grid = [
            ['+', '-', '*', '/'],
            ['7', '8', '9', 'CE'],
            ['4', '5', '6', '<'],
            ['1', '2', '3', '.'],
            ['^', '0', '=', '=']
        ]
        self.style = {
            '.': {'text': '•'},
            '=': {'bg': '#FF7F27'}
        }

        self.entry.grid(row=0, column=0, columnspan=len(
            self.grid[0]), sticky='we')
        self.putButtons()

    def putButtons(self):
        for y, yval in enumerate(self.grid):
            for x, xval in enumerate(yval):
                self.button(xval, x, y+1)

    def addInput(self, value):
        def settext(text):
            self.entry.delete(0, 'end')
            self.entry.insert(0, str(text))

        def gettext(): return self.entry.get()
        def addtext(text): return self.entry.insert('end', str(text))
        def cleartext(): return self.entry.delete(0, 'end')
        def getlast(): return self.entry.get()[-1]
        def dectext(): return self.entry.delete(len(gettext())-1)

        self.entry['state'] = 'normal'

        if gettext() == 'ERROR':
            cleartext()

        if value == '=':
            settext(evaluate(gettext()))
        elif value == '<':
            dectext()
        elif value == 'CE':
            cleartext()
        if value in ['=', '<', 'CE']:
            self.entry['state'] = 'readonly'
            return
        if value in '/*+':
            if len(gettext()) == 0 or getlast() in '+-*/':
                return
        if gettext() == '0' and value in '0123456789':
            dectext()

        addtext(value)
        self.entry['state'] = 'readonly'

    def button(self, value, x, y, padding=0):
        width, height = self.b_size
        btn = tkinter.Button(self.master, text=value, command=lambda: self.addInput(
            value), width=width, height=height, font=self.b_font)

        if value in self.style:
            for i in self.style[value]:
                btn[i] = self.style[value][i]

        btn.grid(row=y, column=x, padx=padding, pady=padding)
        return btn


root = tkinter.Tk()
gui = GUI(root)
root.mainloop()
