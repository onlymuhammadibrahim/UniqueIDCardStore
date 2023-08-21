from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import winsound
from dateutil import tz
from datetime import datetime
import time
from collections import defaultdict
import pyodbc

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
    Path(r"C:\Users\DELL\Desktop\new\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

server = "DESKTOP-DFCHIE6"
database = "OFFLINE"
cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-DFCHIE6;'
                          'Database=OFFLINE;'
                          'UID=sa;'
                          'PWD=helloworld125;'
                          'Trusted_Connection=no;')
    
cursor = cnxn.cursor()


window = Tk()

window.geometry("798x496")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=496,
    width=798,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

def check_record(record):
    cursor.execute('SELECT * FROM offline_version_table WHERE Card LIKE '  + "'%" + str(record)+ "%'")
    if (len(list(cursor))) != 0:
        return True
    return False

def insert_new_record(record):
    if check_record(record) == False:
        value = (record, time.time())
        insert_query = '''INSERT INTO offline_version_table (Card, Time)
        	      VALUES (?, ?);'''
        cursor.execute(insert_query, value)
        cnxn.commit()
        return True
    return False

def get_record_time(record):
    cursor.execute('SELECT * FROM offline_version_table WHERE Card LIKE '  + "'%" + str(record)+ "%'")
    for i in cursor:
        return  datetime.fromtimestamp(i[2]).strftime("%m/%d/%Y, %H:%M:%S")



def save():
    newInput = ''
    error = False
    inp = entry_1.get(1.0, "end-1c")
    entry_1.delete("1.0", "end")

    if (len(inp) == 13):
        newInput = inp
        if (insert_new_record(newInput) == False):
            oldDate = get_record_time(newInput)
            error = True
            canvas.itemconfig(lbl, text="Duplicate Record "+ oldDate, fill='red')
    elif (len(inp) == 27):
        newInput = inp[:-1][12:-1]
        if (insert_new_record(newInput) == False):
            oldDate = get_record_time(newInput)
            error = True
            canvas.itemconfig(lbl, text="Duplicate Record "+ oldDate, fill='red')
    else:
        x = inp.split('\n')
        for i in x:
            if (len(i) == 13) & (i.isdigit()):
                newInput = i
                if (insert_new_record(newInput) == False):
                    oldDate = get_record_time(newInput)
                    error = True
                    canvas.itemconfig(
                        lbl, text="Duplicate Record "+ oldDate, fill='red')

    if (error == False):
        if (len(newInput) != 0):
            canvas.itemconfig(lbl, text="Successfully saved: " +
                                newInput, fill='green')
        else:
            canvas.itemconfig(
                lbl, text="You have entered wrong Id", fill='red')
    else:
        winsound.PlaySound("panic.wav", winsound.SND_ALIAS)


def checkWithoutError():
    newInput = ''
    error = False
    inp = entry_1.get(1.0, "end-1c")
    entry_1.delete("1.0", "end")

    if (len(inp) == 13):
        newInput = inp
        if (check_record(newInput) == False):
            error = True
            canvas.itemconfig(lbl, text="No Record", fill='red')
    elif (len(inp) == 27):
        newInput = inp[:-1][12:-1]
        if (check_record(newInput) == False):
            error = True
            canvas.itemconfig(lbl, text="No Record", fill='red')
    else:
        x = inp.split('\n')
        for i in x:
            if (len(i) == 13) & (i.isdigit()):
                newInput = i
                if (check_record(newInput) == False):
                    error = True
                    canvas.itemconfig(lbl, text="No Record", fill='red')

    if (error == False):
        if (len(newInput) != 0):
            canvas.itemconfig(lbl, text="Record Exists: " +
                                newInput, fill='green')
        else:
            canvas.itemconfig(
                lbl, text="You have entered wrong Id", fill='red')


def generate_report():
    entry_2.delete("1.0", "end")
    to_zone = tz.gettz('Asia/Karachi')
    cursor.execute('SELECT * FROM offline_version_table')
    countTotal = 0
    output = ''
    recordsByDate = defaultdict(list)
    for i in cursor:
        newTime = datetime.utcfromtimestamp(i[2]).astimezone(to_zone)
        recordsByDate[str(newTime.date())].append(i)
    keys = sorted(recordsByDate.keys())

    for key in keys:
        dayLength = len(recordsByDate[key])
        output = output + key + ' : ' + str(dayLength) + '\n'
        countTotal += dayLength
    output = output + 'Total' + ' : ' + str(countTotal) + '\n'
    entry_2.insert('1.0', output)


image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    399.0,
    481.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    399.0,
    35.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    399.0,
    35.0,
    image=image_image_3
)

canvas.create_text(
    71.0,
    119.0,
    anchor="nw",
    text="Please enter NIC",
    fill="#222222",
    font=("Inter", 19 * -1)
)

canvas.create_text(
    482.0,
    119.0,
    anchor="nw",
    text="Report",
    fill="#222222",
    font=("Inter", 19 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    191.0,
    180.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#F4F4F4",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=79.0,
    y=159.0,
    width=224.0,
    height=40.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    604.0,
    235.5,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#F4F4F4",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=492.0,
    y=159.0,
    width=224.0,
    height=151.0
)

lbl = canvas.create_text(
    71.0,
    214.0,
    anchor="nw",
    text="Result : ",
    fill="#222222",
    font=("Inter", 19 * -1),
    width=200
)

lbl2 = canvas.create_text(
    648.0,
    472.0,
    anchor="nw",
    text="Internet : Connected",
    fill="#222222",
    font=("Inter", 13 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=checkWithoutError,
    relief="flat"
)
button_1.place(
    x=215.0,
    y=337.0,
    width=98.0,
    height=33.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=generate_report,
    relief="flat"
)
button_2.place(
    x=506.0,
    y=337.0,
    width=195.0,
    height=32.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=save,
    relief="flat"
)
button_3.place(
    x=71.0,
    y=337.0,
    width=98.0,
    height=32.0
)
window.resizable(False, False)
window.mainloop()
