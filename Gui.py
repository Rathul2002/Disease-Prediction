from tkinter import *
from tkinter import messagebox, IntVar
import pandas as pd
import disease_prediction as dp


def message():
    symptoms = []
    day = 0
    if Symptom1.get() == "None" and Symptom2.get() == "None" and Symptom3.get() == "None" and Symptom4.get() == "None" and Symptom5.get() == "None":
        messagebox.showinfo("OPPS!!", "ENTER  SYMPTOMS PLEASE")
    elif DaysVar.get() == 0:
        messagebox.showinfo("OPPS!!", "ENTER  Valid day PLEASE")
    else:
        if Symptom1.get() != "None":
            symptoms.append(Symptom1.get())
        if Symptom2.get() != "None":
            symptoms.append(Symptom2.get())
        if Symptom3.get() != "None":
            symptoms.append(Symptom3.get())
        if Symptom4.get() != "None":
            symptoms.append(Symptom4.get())
        if Symptom5.get() != "None":
            symptoms.append(Symptom5.get())
        day = DaysVar.get()
        result = symptoms, day
        d, desc, prec, sev = dp.Disease_prediction(result)

        if d != '':
            pred.delete("1.0", END)
            pred.insert(END, d)
        else:
            pred.delete("1.0", END)
            pred.insert(END, "No Disease Detected")
        text = 'Description:\n' + desc + '\nPrecaution:\n' + prec + '\nSeverity:\n' + sev
        t4.delete("1.0", END)
        t4.insert(END, text)


tr = pd.read_csv("./MasterData/Symptoms.csv")
list = tr['Key'].to_list()
list.insert(0, 'None')
root = Tk()
root.title(" Disease Prediction From Symptoms")
root.configure()
w2 = Label(root, justify=LEFT, text=" Disease Prediction From Symptoms ")
w2.config(font=("Comic Sans MS", 20, "bold"))
w2.grid(row=1, column=0, columnspan=2, padx=100)

Symptom1 = StringVar()
Symptom1.set(None)
Symptom2 = StringVar()
Symptom2.set(None)
Symptom3 = StringVar()
Symptom3.set(None)
Symptom4 = StringVar()
Symptom4.set(None)
Symptom5 = StringVar()
Symptom5.set(None)
DaysVar: IntVar = IntVar()

S1Lb = Label(root, text="Symptom 1")
S1Lb.config(font=("Comic Sans MS", 15))
S1Lb.grid(row=3, column=0, pady=5, sticky=W)

S2Lb = Label(root, text="Symptom 2")
S2Lb.config(font=("Comic Sans MS", 15))
S2Lb.grid(row=4, column=0, pady=5, sticky=W)

S3Lb = Label(root, text="Symptom 3")
S3Lb.config(font=("Comic Sans MS", 15))
S3Lb.grid(row=5, column=0, pady=5, sticky=W)

S4Lb = Label(root, text="Symptom 4")
S4Lb.config(font=("Comic Sans MS", 15))
S4Lb.grid(row=6, column=0, pady=5, sticky=W)

S5Lb = Label(root, text="Symptom 5")
S5Lb.config(font=("Comic Sans MS", 15))
S5Lb.grid(row=7, column=0, pady=5, sticky=W)

dLb = Label(root, text="No of days the symptoms have")
dLb.config(font=("Comic Sans MS", 15))
dLb.grid(row=8, column=0, pady=5, sticky=W)

OPTIONS = sorted(list)

S1En = OptionMenu(root, Symptom1, *OPTIONS)
S1En.grid(row=3, column=2)

S2En = OptionMenu(root, Symptom2, *OPTIONS)
S2En.grid(row=4, column=2)

S3En = OptionMenu(root, Symptom3, *OPTIONS)
S3En.grid(row=5, column=2)

S4En = OptionMenu(root, Symptom4, *OPTIONS)
S4En.grid(row=6, column=2)

S5En = OptionMenu(root, Symptom5, *OPTIONS)
S5En.grid(row=7, column=2)

days_entry = Entry(root, textvariable=DaysVar, width=11)
days_entry.grid(row=8, column=2)

lr = Button(root, text="Predict", height=2, width=20, command=message)
lr.config(font=("Comic Sans MS", 15))
lr.grid(row=9, column=0, columnspan=3, pady=10)

predLb = Label(root, text="Predicted Disease:")
predLb.config(font=("Comic Sans MS", 15))
predLb.grid(row=10, column=0, pady=5, sticky=W)

pred = Text(root, height=1.5, width=20)
pred.config(font=("Comic Sans MS", 15))
pred.grid(row=10, column=1, columnspan=2, padx=(20 // 2), pady=10)

NameLb = Label(root, text="")
NameLb.config(font=("Comic Sans MS", 15))
NameLb.grid(row=11, column=0, pady=10, sticky=W)

t4 = Text(root, height=8, width=40)
t4.config(font=("Comic Sans MS", 15))
t4.grid(row=12, column=0, columnspan=3, padx=(20 // 2), pady=0)

NameLb = Label(root, text="")
NameLb.config(font=("Comic Sans MS", 15))
NameLb.grid(row=13, column=0, pady=0, sticky=W)
root.mainloop()
