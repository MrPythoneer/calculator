import tkinter


def formatnum(x):
    if int(x) == x:
        return int(x)
    else:
        return x


class GUI:
    def __init__(self, master):
        self.entry_font = 'Fixedsys 24'
        self.b_font = 'Fixedsys 12'

        self.master = master
        master.title('Calculator')
        master.geometry('359x388')

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

        self.usegrid()

    def usegrid(self):
        for y, yval in enumerate(self.grid):
            for x, xval in enumerate(yval):
                self.button(xval, x, y+1, *self.b_size)

    def settext(self, text):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(text))

    def gettext(self):
        return self.entry.get()

    def addtext(self, text):
        self.entry.insert('end', str(text))

    def addInput(self, value):
        self.entry['state'] = 'normal'

        if self.gettext() == 'ERROR':
            self.entry.delete(0, 'end')
        if value == '=':
            try:
                result = eval(self.gettext().replace('^', '**'))
                if len(str(result)) >= 22:
                    result = '{:e}'.format(result)
                self.settext(formatnum(result))
            except Exception:
                self.settext('ERROR')
        elif value == '<':
            self.entry.delete(len(self.gettext())-1)
        elif value == 'CE':
            self.entry.delete(0, 'end')
        if value in ['=', '<', 'CE']:
            self.entry['state'] = 'readonly'
            return
        if value in '/*+':
            if len(self.gettext()[-1]) == 0 or self.gettext()[-1] in '+-*/':
                return

        self.entry.insert('end', value)
        self.entry['state'] = 'readonly'

    def button(self, value, x, y, width, height, padding=0):
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

'''
||||||||
+ - * /
7 8 9 ce
4 5 6 c
1 2 3 .
| 0 ^ =
'''
