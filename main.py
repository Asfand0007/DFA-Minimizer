import tkinter as tk
from tkinter import ttk
from DFA import getDFA, getMinimizedDFA
from PIL import ImageTk, Image
from GUIhelper import setWindowProperties, addImage, getValues, on_enter, on_leave

states=set()
transitions={}
finalStates=set()

def startPage():
    startButton.destroy()
    stateLabel.place(x=235, y=120)
    stateEntry.place(x=295, y=123)
    transition0Label.place(x=398, y=120)
    transition0Entry.place(x=505, y=123)
    transition1Label.place(x=605, y=120)
    transition1Entry.place(x=715, y=123)

    imageLabel.place_forget()
    stateButton.place(relx=0.5, y=180, anchor='center')
    nextButton.place(relx=0.5, y=220, anchor='center')
    ErrorLabel.place(relx=0.5,y=250,anchor='center')

def markFinalState():
    state=dropDownCombo.get()
    if state=="":
        errorText.set("Please select a state")
        return

    errorText.set("")
    finalStates.add(state)
    DFAimage= getDFA(states,transitions, initialState.get(), finalStates)
    image = ImageTk.PhotoImage(Image.open(DFAimage))
    addImage(image, imageLabel)

def minimizeDFA():
    if len(finalStates)==0:
        errorText.set("Please add atleast one final state")
        return

    errorText.set("")    
    heading2Label.place(relx=0.5, y=120, anchor="center")
    DFAimage= getMinimizedDFA(states,transitions, initialState.get(), finalStates)
    dropDownCombo.destroy()
    dropDownLabel.destroy()
    stateButton.destroy()
    nextButton.destroy()
    image = ImageTk.PhotoImage(Image.open(DFAimage))
    addImage(image, imageLabel, yPosition=325)

def addState():
    state,transition0,transition1= getValues(stateEntry,transition0Entry, transition1Entry)
    if state=="" or transition0=="" or transition1=="":
        errorText.set("Error: incomplete info about the state")
        return
    
    errorText.set("")
    if stateButtonText.get()== "Add Initial State":
        initialState.set(state)
        stateButtonText.set("Add State")

    
    if transition0 not in states:
        states.add(transition0)
        transitions[transition0]={"0": transition0, "1": transition0}
    
    if transition1 not in states:
        states.add(transition1)
        transitions[transition1]={"0": transition1, "1": transition1}

    states.add(state)
    transitions[state]={"0": transition0, "1": transition1}
    
    DFAimage= getDFA(states,transitions, initialState.get(), finalStates)
    image = ImageTk.PhotoImage(Image.open(DFAimage))
    addImage(image, imageLabel)

def finalStatesPage():
    if len(states)==0:
        errorText.set("Please add atleast one state")
        return
    
    errorText.set("")
    stateLabel.destroy()
    stateEntry.destroy()
    transition0Label.destroy()
    transition0Entry.destroy()
    transition1Label.destroy()
    transition1Entry.destroy()
    
    dropDownCombo.config(values=list(states))
    dropDownLabel.place(x=360, y=120)
    dropDownCombo.place(x=525, y=123)
    stateButton.config(command=markFinalState)
    nextButton.config(command=minimizeDFA)
    stateButtonText.set("Mark Final State")
    nextButtonText.set("Minimize DFA")

def on_enter_pressed(event):
    stateButton.invoke()

window = tk.Tk()
setWindowProperties(window)

heading = tk.Label(window, text="DFA MINIMIZATION", font=("Century Gothic",32), bg="black", fg="white")
startButton = tk.Button(window, text="Start", font=("Century Gothic", 12), command=startPage, bg="black", fg="white", borderwidth=2, width=15)
imageLabel=tk.Label(window, image="", bd=0)
heading.place(relx=0.5, y=70, anchor='center')
startButton.place(relx=0.5, rely=0.6, anchor='center')
image = ImageTk.PhotoImage(Image.open('display.png'))
addImage(image,imageLabel, yPosition=250)

errorText=tk.StringVar()
stateButtonText = tk.StringVar()
initialState= tk.StringVar()
nextButtonText= tk.StringVar()
stateButtonText.set("Add Initial State")
nextButtonText.set("Next") 

stateLabel=tk.Label(window, text="State:", font=("Century Gothic", 14), bg="black", fg="white")
stateEntry = tk.Entry(window, bg="black", font=("Verdana", 12), fg="white", insertbackground="white", width=5)
transition0Label=tk.Label(window, text="Transtion 0:", font=("Century Gothic", 14), bg="black", fg="white")
transition0Entry = tk.Entry(window, bg="black", font=("Verdana", 12), fg="white", insertbackground="white", width=5)
transition1Label=tk.Label(window, text="Transition 1:", font=("Century Gothic", 14), bg="black", fg="white")
transition1Entry = tk.Entry(window, bg="black", font=("Verdana", 12), fg="white", insertbackground="white", width=5)
dropDownLabel=tk.Label(window, text="Select Final State:", font=("Century Gothic", 14), bg="black", fg="white")
dropDownCombo = ttk.Combobox(state="readonly", font=("Verdana", 12), width=5)
ErrorLabel=tk.Label(window, textvariable=errorText, font=("Century Gothic", 11), bg="black", fg="red")
heading2Label=tk.Label(window, text="Minimized DFA:", font=("Century Gothic", 16), bg="black", fg="white")


stateButton = tk.Button(window, textvariable=stateButtonText, font=("Century Gothic", 12), command=addState, bg="black", fg="white", borderwidth=2, width=15)
nextButton = tk.Button(window, textvariable=nextButtonText, font=("Century Gothic", 12), command=finalStatesPage, bg="black", fg="white", borderwidth=2, width=15)

window.bind('<Return>', on_enter_pressed)
stateButton.bind("<Enter>", on_enter)
stateButton.bind("<Leave>", on_leave)
nextButton.bind("<Enter>", on_enter)
nextButton.bind("<Leave>", on_leave)
startButton.bind("<Enter>", on_enter)
startButton.bind("<Leave>", on_leave)

    
window.mainloop()