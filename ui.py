from minizinc import Instance, Model, Solver, Status
from tkinter import *

root = Tk()
root.title("Projet Minizinc")

class Table: 
    def __init__(self,root,tab,total_rows, total_columns,set_score_throws) :
        root.title("Tableau des lancés") 
        for i in range(total_rows): 
            for j in range(total_columns): 
                if i == 1 and (j < 10 and (set_score_throws[(j-1)*2] != -1 or set_score_throws[(j-1)*2 + 1] != -1)):
                    self.e = Entry(root, width=15, fg='red', font=('Arial',12,'bold')) 
                else :  
                    self.e = Entry(root, width=15, fg='black', font=('Arial',12,'bold')) 
                self.e.grid(row=i, column=j) 
                self.e.insert(END, tab[i][j])

def check_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def go_score():
    bowling = Model("./bowling.mzn")
    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, bowling)
    if not(check_int(score_entry.get())): 
        print("Mauvais score syntaxe")
        return

    score = int(score_entry.get())
    set_score_throws = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    for i in range(20):
        if(check_int(button_set_score_throws[i].get())):
            set_score_throws[i] = int(button_set_score_throws[i].get())

    if(check_int(spare_entry.get())):
        instance["fixedSpareNumber"] = int(spare_entry.get())
        instance["setSpareBool"] = True
    else:
        instance["fixedSpareNumber"] = 0
        instance["setSpareBool"] = False

    if(check_int(strike_entry.get())):
        instance["fixedStrikeNumber"] = int(strike_entry.get())
        instance["setStrikeBool"] = True
    else:
        instance["fixedStrikeNumber"] = 0
        instance["setStrikeBool"] = False

    if(check_int(fail_entry.get())):
        instance["fixedFailNumber"] = int(fail_entry.get())
        instance["setFailBool"] = True
    else:
        instance["fixedFailNumber"] = 0
        instance["setFailBool"] = False

    
    instance["score"] = score
    instance["setScoreThrows"] = set_score_throws
    result = instance.solve()

    new_window = Toplevel(root)
    new_window.title("New Window")

    if result.status == Status.UNSATISFIABLE:
        Label(new_window, text="=====UNSATISFIABLE=====",).grid(row=1)
        return

    throws = result["throws"]
    nb_strike = result["nbStrike"]
    nb_spare = result["nbSpare"]
    nb_fail = result["nbFail"]
    
    if throws[18] != 10 and throws[18] + throws[19] != 10:
        normal_game = [
            ('Tour : ','n°1','n°2','n°3','n°4', 'n°5', 'n°6', 'n°7', 'n°8', 'n°9', 'n°10'),
            ('Points : ', 
            str(throws[0]) + ' | ' + str(throws[1]),
            str(throws[2]) + ' | ' + str(throws[3]),
            str(throws[4]) + ' | ' + str(throws[5]),
            str(throws[6]) + ' | ' + str(throws[7]),
            str(throws[8]) + ' | ' + str(throws[9]),
            str(throws[10]) + ' | ' + str(throws[11]),
            str(throws[12]) + ' | ' + str(throws[13]),
            str(throws[14]) + ' | ' + str(throws[15]),
            str(throws[16]) + ' | ' + str(throws[17]),
            str(throws[18]) + ' | ' + str(throws[19])
            ),
            ('Strike : ', nb_strike, 'Spare : ', nb_spare, 'Failed : ', nb_fail, '', '', '', 'Score :', score),
        ]    
        total_rows = len(normal_game) 
        total_columns = len(normal_game[0])
        Table(new_window, normal_game,total_rows,total_columns, set_score_throws)
    else:
        extra_game = [
            ('Tour : ','n°1','n°2','n°3','n°4', 'n°5', 'n°6', 'n°7', 'n°8', 'n°9', 'n°10', 'ExtraShot'),
            ('Points : ', 
            str(throws[0]) + ' | ' + str(throws[1]),
            str(throws[2]) + ' | ' + str(throws[3]),
            str(throws[4]) + ' | ' + str(throws[5]),
            str(throws[6]) + ' | ' + str(throws[7]),
            str(throws[8]) + ' | ' + str(throws[9]),
            str(throws[10]) + ' | ' + str(throws[11]),
            str(throws[12]) + ' | ' + str(throws[13]),
            str(throws[14]) + ' | ' + str(throws[15]),
            str(throws[16]) + ' | ' + str(throws[17]),
            str(throws[18]) + ' | ' + str(throws[19]),
            str(throws[20]),
            ),
            ('Strike : ', nb_strike, 'Spare : ', nb_spare, 'Failed : ', nb_fail, '', '', '', '', 'Score : ', score),
        ] 
        total_rows = len(extra_game) 
        total_columns = len(extra_game[0])
        Table(new_window, extra_game, total_rows, total_columns, set_score_throws)

Label(root, text="Score : ",).grid(row=2)
score_entry = Entry(root, width="10")
score_entry.grid(row=2, column=1)

Label(root, text="NbStrike : ",).grid(row=4)
strike_entry = Entry(root, width="10")
strike_entry.grid(row=4, column=1)

Label(root, text="NbSapre : ",).grid(row=6)
spare_entry = Entry(root, width="10")
spare_entry.grid(row=6, column=1)

Label(root, text="NbFail : ",).grid(row=8)
fail_entry = Entry(root, width="10")
fail_entry.grid(row=8, column=1)

button_set_score_throws = []
for i in range(19):
    Label(root, text="Round : " + str(i + 1) + " Coups : 1").grid(row=i+10)
    button_set_score_throws.append(Entry(root, width="10"))
    button_set_score_throws[i].grid(row=i+10, column=1)

    i = i + 1 

    Label(root, text="Round : " + str(i + 1) + " Coups : 2").grid(row=i+10)
    button_set_score_throws.append(Entry(root, width="10"))
    button_set_score_throws[i].grid(row=i+10, column=1)

Button(root, 
    text='Go !',
    command=go_score
).grid(row=30, columnspan=2, padx=60)

root.mainloop()