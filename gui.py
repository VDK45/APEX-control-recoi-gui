import tkinter as tk
from random import randint
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

photo = resource_path('weapon_data/apex_full.png')



window = tk.Tk()
bg_color = '#A0ACB0'
height = 250
weight = 350
photo = tk.PhotoImage(file=photo)
window.iconphoto(False, photo)
window.config(bg=bg_color)
window.title("Option:")
# Высота х ширина + (отступ по x+100) + (отступ по y+100)
window.geometry(f"{height}x{weight}+100+100")
window.minsize(250, 350)
window.maxsize(500, 600)
window.resizable(False, False)
sens_value = 2.0
SHOP = True
M_SENS = 0

def mouse_sen_plus():
    global sens_value 
    global M_SENS
    if sens_value < 4:
        sens_value += 0.2
        M_SENS -= 0.5
        label_1.config(text = f"Recoil sensitivity: {round(sens_value, 1)}")
    else:
        sens_value = 4
    


button_1 = tk.Button(window, text="Recoil sensitivity +",
                     command=mouse_sen_plus,
                     bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=15,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT 
                     )
button_1.place(x=45, y=15)


def mouse_sen_minus():
    global sens_value 
    global M_SENS
    if sens_value > 0.2:
        sens_value -= 0.2
        M_SENS += 0.5
        label_1.config(text = f"Recoil sensitivity: {round(sens_value, 1)}")
    else:
        sens_value = 0.2
    
    

button_2 = tk.Button(window, text="Recoil sensitivity -",
                     command=mouse_sen_minus,
                     bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=15,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT 
                     )
button_2.place(x=45, y=70)


label_1 = tk.Label(window, text=f"""Recoil sensitivity: {round(sens_value)}""",
                    bg="#2FB7B3",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="se",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.RIGHT  # Выровнять тексты по правой стороне
                    
                    )
label_1.place(x=25, y=130)  # Отобразить   # Отобразить 


def shop_on():
    global SHOP
    SHOP = True
    label_2.config(text = "Dead box/Shop: ON")
    label_2.config(bg = "#5CD78D")
    

button_3 = tk.Button(window, text="""Dead box/Shop 
ON             """,
                    command=shop_on,
                    bg="#5CD78D",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=5,  
                    pady=5,  
                    width=10,  
                    height=1,  
                    anchor="center",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT 
                     )
button_3.place(x=15, y=220)


def shop_off():
    global SHOP
    SHOP = False
    label_2.config(text = "Dead box/Shop: OFF")
    label_2.config(bg = "#E17E7E")
    

button_4 = tk.Button(window, text="""Dead box/Shop 
OFF          """,
                    command=shop_off,
                    bg="#E17E7E",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=5,  
                    pady=5,  
                    width=10,  
                    height=1,  
                    anchor="center",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT 
                     )
button_4.place(x=130, y=220)


label_2 = tk.Label(window, text=f"""Dead box/Shop: {'ON '}""",
                    bg="#5CD78D",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="se",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.RIGHT  # Выровнять тексты по правой стороне
                    )
label_2.place(x=25, y=280)  # Отобразить  


if __name__ == "__main__":
    window.mainloop()















