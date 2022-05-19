import tkinter
from expression import Expression


CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class GUI:
    def __init__(self, master: tkinter.Tk):
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
        
        for y, yval in enumerate(self.grid):
            for x, xval in enumerate(yval):
                self.button(xval, x, y+2)

        self.update()

    def update(self) -> None:
        children = self.master.children
        for i, child in enumerate(children.values()):
            if isinstance(child, tkinter.Button):
                if child['text'] in '•/':
                    if self.expr.base != 10:
                        child['bg'] = 'gray'
                        child['state'] = 'disabled'
                        continue
                
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

    def handler(self, value: str) -> None:
        if self.expr.value == ['ERROR']:
            self.expr.clear()

        if value == '<':
            self.expr.trim()
        elif value == '=':
            self.expr.eval()
        elif value == 'CE':
            self.expr.clear()
        elif value == 'bin':
            self.expr.set_base(2)
        elif value == 'oct':
            self.expr.set_base(8)
        elif value == 'dec':
            self.expr.set_base(10)
        elif value == 'duodec':
            self.expr.set_base(12)
        elif value == 'hex':
            self.expr.set_base(16)
        else:
            self.expr.insert(value)

        self.update()

    def button(self, value: str, x: int, y: int, padding: int = 0) -> tkinter.Button:
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
