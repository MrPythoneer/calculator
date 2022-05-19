import tkinter
from expression import Expression


CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class GUI:
    def __init__(self, master):
        self.expr = Expression()
        self.b_size = (10, 4)

        self.grid = [
            ['bin', 'oct',	'dec',	'duodec', 	'hex'],
            ['7',	'8',	'9',	'<',		'CE'],
            ['4',	'5',	'6',	'+',		'-'],
            ['1', 	'2',	'3',	'*',		'/'],
            ['A',	'0',	'E',	'(',		')'],
            ['B',	'C',	'D',	'.',		'='],
        ]

        self.style = {
            '.': {'text': '•'},	'=': {'bg': '#FF7F27'},
            'bin': {'bg': '#BEEC9D', 'height': '1'},
            'oct': {'bg': '#BEEC9D', 'height': '1'},
            'dec': {'bg': '#BEEC9D', 'height': '1'},
            'hex': {'bg': '#BEEC9D', 'height': '1'},
            'duodec': {'bg': '#BEEC9D', 'height': '1'},
            'A': {'bg': '#FFD4D4'}, 'B': {'bg': '#FFD4D4'},
            'C': {'bg': '#FFD4D4'}, 'D': {'bg': '#FFD4D4'},
            'E': {'bg': '#FFD4D4'}
        }

        self.master = master
        master.title('Calculator')

        width = 9 * self.b_size[0] * len(self.grid[0])
        height = 18.7 * self.b_size[1] * len(self.grid)
        master.geometry(f'{width:.0f}x{height:.0f}')

        self.entry_font = 'Fixedsys 24'
        self.b_font = 'Fixedsys 15'

        self.view = tkinter.Entry(master, justify='right', font=self.entry_font, state='readonly')
        self.entry = tkinter.Entry(master, justify='right', font=self.entry_font, state='readonly')

        self.view.grid(row=0, column=0, columnspan=len(self.grid[0]), sticky='we')
        self.entry.grid(row=1, column=0, columnspan=len(self.grid[0]), sticky='we')
        self.placeButtons()

        self.update()

    def placeButtons(self):
        for y, yval in enumerate(self.grid):
            for x, xval in enumerate(yval):
                self.button(xval, x, y+2)

    def update(self):
        children = self.master.children
        for i, child in enumerate(children.values()):
            if type(child) == tkinter.Button:
                if child['text'] in '•/':
                    if self.expr.base != 10:
                        child['bg'] = 'gray'
                        child['state'] = 'disabled'
                        continue
                    else:
                        child['bg'] = 'white'
                        child['state'] = 'normal'

                if child['text'] in '0123456789ABCDE' and int(CHARACTERS.index(child['text'])) > self.expr.base-1:
                    child['bg'] = 'gray'
                    child['state'] = 'disabled'
                else:
                    child['state'] = 'normal'
                    if child['text'] in self.style:
                        child['bg'] = self.style[child['text']]['bg']
                    else:
                        child['bg'] = 'white'

        self.view['state'] = 'normal'
        self.entry['state'] = 'normal'

        self.view.delete(0, 'end')
        self.view.insert(0, self.expr.value[0:-1])

        self.entry.delete(0, 'end')
        self.entry.insert(0, self.expr.value[-1])

        self.entry['state'] = 'readonly'
        self.view['state'] = 'readonly'

    def handler(self, value):
        if self.expr.value == ['ERROR']:
            self.expr.clear()

        if value == '<':
            self.expr.trim()
        elif value == '=':
            self.expr.eval()
        elif value == 'CE':
            self.expr.clear()
        elif value == 'bin':
            self.expr.changeBase(2)
        elif value == 'oct':
            self.expr.changeBase(8)
        elif value == 'dec':
            self.expr.changeBase(10)
        elif value == 'duodec':
            self.expr.changeBase(12)
        elif value == 'hex':
            self.expr.changeBase(16)
        else:
            self.expr.add(value)

        self.update()

    def button(self, value, x, y, padding=0):
        width, height = self.b_size
        btn = tkinter.Button(
            self.master, 		text=value,
            width=width,		height=height,
            font=self.b_font,	command=lambda: self.handler(value)
        )

        if value in self.style:
            for i in self.style[value]:
                btn[i] = self.style[value][i]

        btn.grid(row=y, column=x, padx=padding, pady=padding)
        return btn


root = tkinter.Tk()
gui = GUI(root)
root.mainloop()
