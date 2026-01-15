import tkinter

#setup calculatrice
button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="],
]

#position des bouttons
right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]
bottom_symbols = ["√"]


#nombre rangs et colonnes
row_count = len(button_values) #5
column_count = len(button_values[0])#4


color_1 = "#D4D4D2"
color_2 = "#1C1C1C"
color_3 = "#505050"
color_4 = "#FF9500"
color_5 = "white"

#setup page calculatrice
window = tkinter.Tk() #creer la page
window.title("Calculator")
window.resizable(False, False)

#affichage dans la page
frame = tkinter.Frame(window)#integrer la frame dans window
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_2,
                      foreground=color_5, anchor="e", width=column_count + 1)

label.grid(row=0, column=0, columnspan=column_count, sticky="we")

#Prio des signes
def calculate_expression(expression):
    # Séparer les num et symbols en protégeant les nombres négatifs
    temp_expr = ""
    for i, char in enumerate(expression):
        if char in "+×÷":
            temp_expr += f" {char} "
        elif char == "-":
            # Si le moins est au début ou après un autre opérateur, c'est un nombre négatif
            if i == 0 or expression[i-1] in "+-×÷":
                temp_expr += char
            else:
                temp_expr += " - "
        else:
            temp_expr += char
            
    elements = temp_expr.split()

    # mettre la prio sur la div et la multiplication
    i = 0
    while i < len(elements):
        if elements[i] in ["×", "÷"]:
            num1 = float(elements[i-1])
            num2 = float(elements[i+1])
            if elements[i] == "×" :
                res = num1 * num2
            else:
                if num2 == 0: return "ERROR"
                res = num1 / num2
            elements[i-1:i+2] = [res] 
            i -= 1 
        i += 1 # Passage au suivant

    #addition et soustraction
    try:
        total = float(elements[0])
        i = 1
        while i < len(elements):
            op = elements[i]
            num2 = float(elements[i+1])
            if op == "+": total += num2
            if op == "-": total -= num2
            i += 2
        return round(total, 10) # Arrondi pour corriger les erreurs de virgule flottante
    except:
        return "ERROR"


for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30),
                                width=column_count-1, height=1,
                                command=lambda value=value: button_clicked(value))
        
        if value in top_symbols:
            button.config(foreground=color_2, background=color_1)
        elif value in right_symbols:
            button.config(foreground=color_5, background=color_4)
        else:
            button.config(foreground=color_5, background=color_3)

        button.grid(row=row+1, column=column)
frame.pack()



def clear_all():
    global A, B, operator
    A = "0"
    operator = None
    B = None

def remove_zero(num):
    if num == "ERROR": return "ERROR"
    num = round(float(num),10)
    if float(num) % 1 == 0 :
        num = int(num)
    return str(num)


def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value in bottom_symbols:
        if value == "√":
            result = float(label["text"]) ** 0.5
            result = round(result, 4)
            label["text"] = remove_zero(result)


    if value in right_symbols:
        if value == "=":
            try:
                final_result = calculate_expression(label["text"])
                label["text"] = remove_zero(final_result)
                clear_all()
            except:
                label["text"] = "ERROR"
                clear_all()

        elif value in "+-×÷":
            if label["text"] == "ERROR":
                label["text"] = "0"

            if label["text"][-1] in "+-×÷":
                label["text"] = label["text"][:-1] + value
            else:
                label["text"] += value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"

        elif value == "+/-":
            result = float(label["text"])* -1
            label["text"] = remove_zero(result)
            
        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero(result)
    else:
        if value == ".":
            # On split pour vérifier le point sur le dernier nombre tapé
            last_part = label["text"].replace("+"," ").replace("-"," ").replace("×"," ").replace("÷"," ").split()[-1]
            if "." not in last_part:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0" or label["text"] == "ERROR":
                label["text"] = value #remplace le 0
            else:
                label["text"] += value #ajoute chiffre

#centrer la calculatrice
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()