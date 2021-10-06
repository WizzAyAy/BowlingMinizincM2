from minizinc import Instance, Model, Solver
from tkinter import *

class Table: 
    def __init__(self,root,tab,total_rows, total_columns) : 
        for i in range(total_rows): 
            for j in range(total_columns): 
                self.e = Entry(root, width=15, fg='black', font=('Arial',12,'bold')) 
                self.e.grid(row=i, column=j) 
                self.e.insert(END, tab[i][j])

root = Tk() 

Label(root, text="Score : ",).grid(row=2)
e1 = Entry(root, width="10")
e1.grid(row=2, column=1)

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
    if(check_int(e1.get())): 
        score = int(e1.get())
        if(score <= 300 and score >=0):
            is_good_score = True

    if(is_good_score == False):
        return
    instance["score"] = score
    result = instance.solve()
    throws = result["throws"]
    nb_strike = result["nbStrike"]
    nb_spare = result["nbSpare"]

    new_window = Toplevel(root)
    new_window.title("New Window")
    
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


Button(root, text='Go !', command=go_score).grid(row=2, column=2)
root.mainloop()