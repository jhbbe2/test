from tkinter import *
import math

window = Tk()
window.title("My Calculator")

def click(t):
    try: #일반적인 코드
        if t == "=":
            result = str(eval(display.get()))
            display.insert(END,"=")
            display2.insert(END,result)
        elif t=="C":
            display.delete(0,END)
            display2.delete(0,END)
        elif t=="del":
            pos = len(display.get())-1
            display.delete(pos,END)
        else:
            display.insert(END,t)
            
    except: #오류 발생 시 처리 
        display.delete(0,END)
        display2.delete(0,END)
        display.insert(END,"Error")

    

display = Entry(window, width=33, bg="yellow")
display.grid(row=0, column=0, columnspan=6)
display2 = Entry(window, width=33, bg="yellow")
display2.grid(row=1, column=0, columnspan=6)

button_list = [
    '7','8','9','/','//','C',
    '4','5','6','*','**','(',
    '1','2','3','-','%',')',
    '0','.','=','+','abs','del']

row_index = 2
col_index = 0
for button_text in button_list:
    def temp(t=button_text):
        click(t)
    Button(window,text=button_text,width=5,command=temp).grid(row=row_index, column=col_index)
    col_index += 1
    if col_index > 5:
        row_index += 1
        col_index = 0
