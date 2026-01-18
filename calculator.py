import tkinter

#setup calculatrice
button_values = [
    ["AC", "+/-", "%", "+"],
    ["(", ")", "√", "-"],
    ["sin", "cos", "tan", "×"], 
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "**"],
    ["1", "2", "3", "="],
    ["0", ".", " ", "π"],
]

#position des bouttons
right_symbols = ["**", "÷", "×", "-", "+", "=", "π"]
top_symbols = ["AC", "+/-", "%"]
bottom_symbols = ["√", "sin", "cos", "tan"]


#nombre rangs et colonnes
row_count = len(button_values) 
column_count = len(button_values[0])


color_1 = "#D4D4D2"
color_2 = "#1C1C1C"
color_3 = "#505050"
color_4 = "#FF9500"
color_5 = "white"

is_result=False

#setup page calculatrice
window = tkinter.Tk() #creer la page
window.title("Calculator")
window.resizable(False, False)
window.configure(background=color_2)

# --- STRUCTURE POUR HISTORIQUE ---
main_wrapper = tkinter.Frame(window, background=color_2)
main_wrapper.pack(padx=10, pady=10)

frame = tkinter.Frame(main_wrapper, background=color_2)#integrer la frame dans main_wrapper
frame.grid(row=0, column=0)

label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_2,
                      foreground=color_5, anchor="e", width=column_count + 1)

label.grid(row=0, column=0, columnspan=column_count, sticky="we")

# --- SECTION HISTORIQUE ---
history_frame = tkinter.Frame(main_wrapper, background=color_3, padx=10, pady=10)
history_frame.grid(row=0, column=1, sticky="ns", padx=(10, 0))

tkinter.Label(history_frame, text="HISTORIQUE", font=("Arial", 12, "bold"), 
              background=color_3, foreground=color_5).pack()

history_list = tkinter.Listbox(history_frame, width=20, height=15, font=("Arial", 10),
                               background=color_2, foreground=color_5, borderwidth=0)
history_list.pack(pady=5)

def clear_history():
    history_list.delete(0, tkinter.END)

clear_hist_btn = tkinter.Button(history_frame, text="Effacer", command=clear_history,
                                background=color_1, foreground=color_2, font=("Arial", 10))
clear_hist_btn.pack(fill="x")

# --- VALEUR DE PI ET FONCTIONS MAISON ---
PI_VAL = 3.14

def custom_sin(x):
    # Conversion degrés en radians
    x = (x % 360) * (PI_VAL / 180)
    # Série de Taylor
    res = x - (x**3)/6 + (x**5)/120 - (x**7)/5040 + (x**9)/362880
    return round(res, 8)

def custom_cos(x):
    x = (x % 360) * (PI_VAL / 180)
    # Série de Taylor
    res = 1 - (x**2)/2 + (x**4)/24 - (x**6)/720 + (x**8)/40320
    return round(res, 8)

def custom_tan(x):
    c = custom_cos(x)
    if abs(c) < 0.0000001: return "ERROR"
    return round(custom_sin(x) / c, 8)


#Prio des signes
def calculate_expression(expression):
    #Gestion des parantheses
    
    while "(" in expression:
        start = expression.rfind("(")
        end = expression.find(")", start)

        if end == -1: return "ERROR"
        
        sub_expr = expression[start + 1:end]
        sub_result = calculate_expression(sub_expr)
        expression = expression[:start] + str(sub_result) + expression[end + 1:]


    # Séparer les num et symbols en protégeant les nombres négatifs
    temp_expr = expression.replace("**", " ** ").replace("×", " × ").replace("÷", " ÷ ").replace("+", " + ")
            
    elements = []
    for part in temp_expr.split():
            if "-" in part and len(part) > 1: 
                elements.append(part)
            elif "-" in part: 
                elements.append("-")
            else:
                elements.append(part)

    # mettre la prio sur la div et la multiplication
    i = 0
    while i < len(elements):

        if elements[i] == "**": # Utilise == car c'est un seul symbole
                    num1 = float(elements[i-1])
                    num2 = float(elements[i+1])
                    res = num1 ** num2
                    elements[i-1:i+2] = [res]

                    i -= 1      
        elif elements[i] in ["×", "÷"]:
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
        if value == " ": continue
        button = tkinter.Button(frame, text=value, font=("Arial", 25),
                                width=column_count, height=1,
                                command=lambda value=value: button_clicked(value))
        
        if value in top_symbols:
            button.config(foreground=color_2, background=color_1)
        elif value in right_symbols:
            button.config(foreground=color_5, background=color_4)
        else:
            button.config(foreground=color_5, background=color_3)

        button.grid(row=row+1, column=column)



def clear_all():
    global A, B, operator
    A = "0"
    operator = None
    B = None


# Nettoyage et formatage du texte
def remove_zero(num):
    if num == "ERROR": return "ERROR"

    try:
        f_num = float(num)
        if abs(f_num) > 9999999999 :
            return "{:.5e}".format(f_num)
        
        # Vérifie que c'est un entier
        if f_num % 1 == 0:
            return str(int(f_num))
        else:
            return str(round(f_num, 8))
    except:
        return "ERROR"


def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator
    global is_result

    if value in bottom_symbols:
        val_origin = label["text"]
        
        # Cas spécial pour PI
        if value == "π":
            if label["text"] == "0" or label["text"] == "ERROR":
                label["text"] = str(PI_VAL)
            else:
                # Si on a déjà un chiffre, on multiplie par défaut ou on ajoute
                label["text"] += str(PI_VAL)
            return

        try:
            val = float(val_origin)
            res_str = ""
            if value == "√":
                if val < 0: res_str = "ERROR"
                else: res_str = remove_zero(round(val**0.5, 4))
            elif value == "sin":
                res_str = remove_zero(custom_sin(val))
            elif value == "cos":
                res_str = remove_zero(custom_cos(val))
            elif value == "tan":
                res_str = remove_zero(custom_tan(val))
            
            if res_str != "ERROR":
                history_list.insert(0, f"{value}({val_origin}) = {res_str}")
            label["text"] = res_str
        except: label["text"] = "ERROR"


    if value in right_symbols:
        if value == "=":
            expr_origin = label["text"] # Sauvegarde avant calcul
            try:
                final_result = calculate_expression(expr_origin)
                res_str = remove_zero(final_result)
                
                # Ajout à l'historique
                if res_str != "ERROR" and expr_origin != res_str:
                    history_list.insert(0, f"{expr_origin} = {res_str}")
                
                label["text"] = res_str
                is_result=True
                clear_all()
            except:
                label["text"] = res_str
                is_result = True  # On active le témoin : c'est un résultat
                clear_all()
        elif value in "+-×÷**":
            is_result = False
            if label["text"] == "ERROR":
                label["text"] = "0"

            if label["text"][-1] in "+-×÷**":
                label["text"] = label["text"][:-1] + value
            else:
                label["text"] += value

    elif value in top_symbols:
        if value == "AC":
            is_result = False
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
            last_part = label["text"].replace("+"," ").replace("-"," ").replace("×"," ").replace("÷"," ").replace("(", " ").replace(")", " ").split()
            if not last_part: last_part = ["0"]
            if "." not in last_part[-1]:
                label["text"] += value
        elif value in "0123456789()π":
            # Si c'est un résultat, on efface tout et on écrit le nouveau chiffre
            if is_result:
                label["text"] = value
                is_result = False # On désactive le témoin pour la suite
            elif label["text"] == "0" or label["text"] == "ERROR":
                label["text"] = value
            else:
                label["text"] += value

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