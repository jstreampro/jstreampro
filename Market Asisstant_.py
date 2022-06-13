from tkinter import *
from tkinter import END
from tkinter.filedialog import asksaveasfile
from requests import *
import json
import pprint
win = Tk()


def stop():
    win.destroy()  # exits the window


class App(object):
    def __init__(self, master):
        self.master = master



        # main window
        master.geometry("950x800")
        master.resizable(False, False)
        master.title("Market Assistent")
        master.wm_iconbitmap("favicon.ico") # its icon

        self.lbl1 = Label(win, text='Please enter a Symbol name : ', fg="black", font="Verdana 12 ")  # the title
        self.lbl1.place(x=100, y=23)
        self.txt1 = Text(win, width=100, height=45)
        self.txt1.place(x=100, y=60)
        self.w = Entry(win, text="symbol?", font="Verdana 12 bold", width=30)  # insert symbol widget
        self.w.place(x=380, y=23)
        self.bExecute = Button(win, text="Submit", command=self.crypto_price, font="Verdana 10 bold", width=10)
        self.bExecute.place(x=805, y=20)

        men = Menu(win)
        newMen = Menu(men)
        newMen.add_command(label="Read Me", command=self.help)
        newMen.add_separator()
        newMen.add_command(label="Save output", command=lambda: self.save())
        newMen.add_command(label="Exit", command=stop)
        men.add_cascade(label='Options', men=newMen)
        win.config(menu=men)


    def save(self):
        Files = [('All Files', '*.*'),
                 ('Text Document', '*.txt')]
        file = asksaveasfile(filetypes=Files, defaultextension=Files)
        file = str(file)

        self.filepath = file[file.find("\'")+ 1 : file.rfind("m") - 2]
        with open(self.filepath, "w") as file:
            file.write(str(self.data))

    def help(self):
        self.help = Toplevel()
        self.help.title("Read Me")
        self.help.geometry("550x150")
        Label(self.help,
              text="\nThis is the ReadMe page."
                    "To make use of Market Assistant,\n"
                    "Only the whole name of your selected Crypto-Coin should be entered.\n"
                    "You will receive all accessible information on this coin from the CMC API instantaneously.\n"
                    "To save the output, click save on the menu bar.\n").pack()
    # API listings
    def crypto_name_updater(self):


        global crypto_name, crypto_names
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5',
            'convert': 'USD',
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '<Enter your CMC API key here>',
        }
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        data = response.json()

        for info in data['data']:
            nameCoin = info['name']
            coinID = info['id']
            coinSymbol = info['symbol']
            print(nameCoin, coinID, coinSymbol)
        self.txt1.insert(END, crypto_name)

    def crypto_price(self):
        slug = self.w.get()
        self.txt1.delete(1.0, END)
        self.txt1.insert(END, slug)
        # print(slug)


        # API
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'slug': slug,
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '70819274-06bf-439a-aa39-ddf65761a315'
        }


        # saves cookies, this way it wont download the same info again & again.
        session = Session()
        session.headers.update(headers)  # setting the headers to the API
        response = session.get(url, params=parameters)  # completes the session cycle
        self.data = json.loads(response.text)  # controls the output ['data']['1']['quote']['USD']['price']


        pprint.pprint(self.data['status'])
        json_formatted_str = json.dumps(self.data, indent=2)
        self.txt1.insert(END, json_formatted_str)




root = App(win)
win.mainloop()