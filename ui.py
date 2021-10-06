from minizinc import Instance, Model, Solver, Status
from tkinter import *

root = Tk() 

class Table: 
    def __init__(self,root,tab,total_rows, total_columns) : 
        for i in range(total_rows): 
            for j in range(total_columns): 
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
    is_good_score = False
    if(check_int(score_entry.get())): 
        score = int(score_entry.get())
        if(score <= 300 and score >=0):
            is_good_score = True
    if(is_good_score == False):
        return
    
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

    instance["score"] = score
    result = instance.solve()

    new_window = Toplevel(root)
    new_window.title("New Window")

    if result.status == Status.UNSATISFIABLE:
        print("=====UNSATISFIABLE=====")
        Label(new_window, text="=====UNSATISFIABLE=====",).grid(row=1)
        return

    throws = result["throws"]
    nb_strike = result["nbStrike"]
    nb_spare = result["nbSpare"]

    
    
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
            ('Strike : ', nb_strike, 'Spare : ', nb_spare, '', '', '', '', '', 'Score :', score),
        ]    
        total_rows = len(normal_game) 
        total_columns = len(normal_game[0])
        Table(new_window, normal_game,total_rows,total_columns)
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
            ('Strike : ', nb_strike, 'Spare : ', nb_spare, '', '', '', '', '', '', 'Score : ', score),
        ] 
        total_rows = len(extra_game) 
        total_columns = len(extra_game[0])
        Table(new_window, extra_game, total_rows, total_columns)

Label(root, text="Score : ",).grid(row=2)
score_entry = Entry(root, width="10")
score_entry.grid(row=2, column=1)

Label(root, text="NbSapre : ",).grid(row=4)
spare_entry = Entry(root, width="10")
spare_entry.grid(row=4, column=1)

Label(root, text="NbStrike : ",).grid(row=6)
strike_entry = Entry(root, width="10")
strike_entry.grid(row=6, column=1)
Button(root, text='Go !', command=go_score).grid(row=4, column=2)

root.mainloop()