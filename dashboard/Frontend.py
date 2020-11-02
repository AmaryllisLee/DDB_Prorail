import numpy as np
from tkinter import *
from tkinter import ttk
from datetime import datetime
from joblib import load

linreg1 = load('linreg1.joblib')
linreg2 = load('linreg2.joblib')
linreg3 = load('linreg3.joblib')


def get_predict(code, groep, prioriteit):  # voorspeld de hersteltijd aan de hand van de code, groep en prioriteit
    if groep == 'ONR-DERD':
        values = np.array([code, prioriteit, 1, 0, 0, 0]).reshape(1, -1)
        result = str(linreg2.predict(values))
        result = result.replace('[', '')
        result = result.replace(']', '')
        return float(result), values
    elif groep == 'ONR-RIB':
        values = np.array([code, prioriteit, 0, 1, 0, 0]).reshape(1, -1)
        result = str(linreg2.predict(values))
        result = result.replace('[', '')
        result = result.replace(']', '')
        return float(result), values
    elif groep == 'TECHONV':
        values = np.array([code, prioriteit, 0, 0, 1, 0]).reshape(1, -1)
        result = str(linreg2.predict(values))
        result = result.replace('[', '')
        result = result.replace(']', '')
        return float(result), values
    elif groep == 'WEER':
        values = np.array([code, prioriteit, 0, 0, 1, 0]).reshape(1, -1)
        result = str(linreg2.predict(values))
        result = result.replace('[', '')
        result = result.replace(']', '')
        return float(result), values


def get_accuracy(prediction, values):  # berekend de betrouwbaarheid van de voorspelde tijd aan de hand van marge
    # van twee andere linregs
    result1 = str(linreg1.predict(values))
    result3 = str(linreg3.predict(values))
    result1 = result1.replace('[', '')
    result1 = result1.replace(']', '')
    result3 = result3.replace('[', '')
    result3 = result3.replace(']', '')
    result1 = float(result1)
    result3 = float(result3)
    marge = ((result1 - prediction)-(result3 - prediction))/2
    # print(prediction, result1, result3, marge, marge/prediction*100)

    percentage = 100-(marge/prediction*100)
    # maakt van trust lager dan 0 een 0
    if percentage < 0:
        percentage = 0.0

    return percentage


def get_color(percent):  # geeft de kleurnaam aan de hand van het percentage
    if 0 <= percent < 21:
        return 'red'
    elif 20 < percent < 41:
        return 'orange'
    elif 40 < percent < 61:
        return 'yellow'
    elif 60 < percent < 81:
        return 'OliveDrab1'
    elif 80 < percent < 101:
        return 'green2'
    elif 0 > percent or 100 < percent:
        return 'purple'
    else:
        return 'blue'


def get_input():  # Functie die de invoer van de comboboxen verwerkt en in de treeview zet
    # Waardes uit de comboboxen halen
    code = e1.get()
    groep = e2.get()
    prioriteit = e3.get()
    # check of alle velden zijn ingevult voor dat hij het verwerkt
    if code != "" and groep != "" and prioriteit != "":
        # voorspelt de hersteltijd, berekend de betouwbaarheid en haalt de kleur van de regel op
        prediction, values = get_predict(int(code), groep, int(prioriteit))
        trust = get_accuracy(prediction, values)
        color = get_color(trust)
        # voegt alle waardes aan de treeview toe met een tijd van toevoeging
        tree.insert("", END, values=(
            code, groep, prioriteit, round(prediction, 2), round(trust, 2), datetime.now().strftime("%d-%m-%Y %H:%M")),
                    tags=color)

        # reset de comboboxen
        e1.set('')
        e2.set('')
        e3.set('')


def remove():  # Functie die de geselecteerde row uit de treeview verwijderd
    if tree.selection():
        tree.delete(tree.selection())


def treeview_sort_column(tree, col, reverse):  # Functie die rows sort op de column
    # kijkt of de waardes ints zijn of niet, haalt de waardes op en sorteert ze
    # van laag naar hoog of hoog naar laag
    try:
        l = [(int(tree.set(k, col)), k) for k in tree.get_children('')]
    except Exception:
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
    l.sort(reverse=reverse)

    # Zet de waardes terug in de treeview
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # Zorgt ervoor dat de volgende sort het tegenovergestelde doet
    tree.heading(col, command=lambda _col=col: treeview_sort_column(tree, _col, not reverse))


def handle_click(event):  # Functie die aanpassen van de column breedte voorkomt
    if tree.identify_region(event.x, event.y) == "separator":
        return "break"


def deselect(event):  # functie die het deselecteren van rows mogelijk maakt
    selection = tree.selection()
    item = tree.identify('item', event.x, event.y)
    if item in selection:
        tree.selection_remove(item)
        return "break"


# initialiseren root, frame en labels
master = Tk()
frame = Frame(master, background='#bf1238', borderwidth=4, relief='raised')
frame2 = Frame(master, background='black', borderwidth=2, relief='raised')
Label(frame, text="Oorzaakscode", width=12).grid(row=0)
Label(frame, text="Oorzaaksgroep", width=12).grid(row=1)
Label(frame, text="Prioriteit", width=12).grid(row=2)
Label(frame2, text="Legenda", width=12, relief='raised').grid(row=10, column=2)
Label(frame2, text="0% - 20%", width=12, background='red', relief='raised').grid(row=11, column=2)
Label(frame2, text="21% - 40%", width=12, background='orange', relief='raised').grid(row=12, column=2)
Label(frame2, text="41% - 60%", width=12, background='yellow', relief='raised').grid(row=13, column=2)
Label(frame2, text="61% - 80%", width=12, background='OliveDrab1', relief='raised').grid(row=10, column=3)
Label(frame2, text="81% - 100%", width=12, background='green2', relief='raised').grid(row=11, column=3)
Label(frame2, text="<0% or >100%", width=12, background='purple', relief='raised').grid(row=12, column=3)
Label(frame2, text="Not int", width=12, background='blue', relief='raised').grid(row=13, column=3)

# combobox voor de oorzaakscode
e1 = ttk.Combobox(frame,
                  state="readonly",
                  values=[130, 131, 132, 133, 134, 135, 136, 140, 141,
                          142, 143, 144, 145, 146, 147, 148, 149, 150,
                          151, 152, 153, 154, 181, 182, 183, 184, 185,
                          186, 187, 188, 189, 201, 202, 203, 204, 205,
                          206, 207, 208, 209, 210, 211, 212, 213, 214,
                          215, 218, 219, 220, 221, 222, 223, 224, 225,
                          226, 227, 228, 229, 230, 231, 233, 234, 235,
                          239, 240, 241, 242, 250, 294, 298, 299])
# combobox voor de oorzaaksgroep
e2 = ttk.Combobox(frame, state="readonly", values=['ONR-RIB', 'ONR-DERD', 'TECHONV', 'WEER'])
# combobox voor de prioriteit
e3 = ttk.Combobox(frame, state="readonly", values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# button voor het invoeren van de comboboxen in de treeview
b = Button(frame, width=12, text="Insert", command=get_input)

# treeview aanmaken
tree = ttk.Treeview(master)

# button voor selectie uit de treeview halen
btn = Button(master, width=12, text="Delete", command=remove)

# code om lettertype van heading in treeview te vergroten
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 13))

# columns in treeview aanmaken
tree["columns"] = ["Oorzaakscode", "Oorzaaksgroep", "Prioriteit", "Voorspeltijd (min)", "Trust (%)", "Toevoegdatum"]
tree["show"] = "headings"
tree.heading("Oorzaakscode", text="Oorzaakscode",
             command=lambda col="Oorzaakscode": treeview_sort_column(tree, col, False))
tree.column("Oorzaakscode", minwidth=0, width=100)
tree.heading("Oorzaaksgroep", text="Oorzaaksgroep",
             command=lambda col="Oorzaaksgroep": treeview_sort_column(tree, col, False))
tree.column("Oorzaaksgroep", minwidth=0, width=100)
tree.heading("Prioriteit", text="Prioriteit", command=lambda col="Prioriteit": treeview_sort_column(tree, col, False))
tree.column("Prioriteit", minwidth=0, width=100)
tree.heading("Voorspeltijd (min)", text="Voorspeltijd (min)",
             command=lambda col="Voorspeltijd (min)": treeview_sort_column(tree, col, False))
tree.column("Voorspeltijd (min)", minwidth=0, width=150)
tree.heading("Trust (%)", text="Trust (%)", command=lambda col="Trust (%)": treeview_sort_column(tree, col, False))
tree.column("Trust (%)", minwidth=0, width=100)
tree.heading("Toevoegdatum", text="Toevoegdatum",
             command=lambda col="Toevoegdatum": treeview_sort_column(tree, col, False))
tree.column("Toevoegdatum", minwidth=0, width=150)

# Tags voor kleuren van rows in treeview
tree.tag_configure('red', background='red')
tree.tag_configure('orange', background='orange')
tree.tag_configure('yellow', background='yellow')
tree.tag_configure('OliveDrab1', background='OliveDrab1')
tree.tag_configure('green2', background='green2')
tree.tag_configure('purple', background='purple')
tree.tag_configure('blue', background='blue')

# code om de functie voor aanpassen van columnbreedte aan de linkermuistoets te koppelen
tree.bind('<Button-1>', handle_click)

# code om de functie voor deselecteren rows aan rechtermuistoets te koppelen
tree.bind("<2>", deselect)

# locaties in grids
frame.grid(row=0, column=0, rowspan=8, columnspan=2, sticky=NSEW)
frame2.grid(row=8, column=0, rowspan=4, columnspan=2)
e1.grid(row=0, column=1, padx=5, pady=5)
e2.grid(row=1, column=1, padx=5, pady=5)
e3.grid(row=2, column=1, padx=5, pady=5)
b.grid(row=3, padx=5, pady=25)
tree.grid(row=0, column=2, rowspan=8, columnspan=2)
btn.grid(row=10, column=3)

# window settings
master.configure(background='gray65')
master.geometry('1075x310')
master.resizable(False, False)

mainloop()
