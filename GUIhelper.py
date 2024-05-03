import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

def setWindowProperties(window):
    def show_tooltip(event):
        aboutUsLabel.config(font= ('Helvetica 13 underline'))
        tooltip.place(relx=0.99, rely=0.95, anchor='se')
        tooltip.lift()

    def hide_tooltip(event):
        aboutUsLabel.config(font= ('Helvetica 12'))
        tooltip.place_forget()


    window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('icon.png')))
    window.title('DFA minimization')
    window.geometry("1000x650")
    window.resizable(False, False)
    window.configure(bg="black")

    aboutUsLabel = tk.Label(window, text="About us?", font=("Helvetica", 12), bg="black", fg="white")
    aboutUsLabel.place(relx=0.99, rely=0.99, anchor='se')
    aboutUsLabel.bind("<Enter>", show_tooltip)
    aboutUsLabel.bind("<Leave>", hide_tooltip)

    # Create the tooltip
    tooltip_text = "Welcome to our DFA Minimizer!\n\nOur application employs the Myhill-Nerode algorithm along\nwith the removal of inaccessible states to efficiently \nminimize DFAs. Our tool optimizes DFAs, reducing their\n complexity while preserving language acceptance.  \n\n Contributors:\n1) Asfand Khanzada (22k-4626)\n2) Munnazzar Shehzad (22k-4231)\n3) Ibrahim Ahmed (22k-4341)"
    tooltip = tk.Label(window, text=tooltip_text, background="grey", relief="solid", borderwidth=1, padx=10, pady=10)
    tooltip.bind("<Enter>", show_tooltip)
    tooltip.bind("<Leave>", hide_tooltip)

    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                            settings={'TCombobox':
                                    {'configure':
                                        {'selectforeground': 'white',   # black font color for selection
                                        'selectbackground': 'black',   # gray background for selection
                                        'fieldbackground': 'black',    # dark gray for the combobox field
                                        'background': 'gray',        # black background
                                        'foreground': 'red',        # white font color
                                        }
                                    }
                                    }
                            )
    combostyle.theme_use('combostyle') 

def addImage(image, image_label, yPosition=450):
    image_label.place(relx=0.5,y=yPosition, anchor="center")
    image_label.configure(image=image)    
    image_label.photo= image

def getValues(stateEntry,transition0Entry, transition1Entry):
    state=stateEntry.get()
    stateEntry.delete(0, tk.END)
    transition0=transition0Entry.get()
    transition0Entry.delete(0, tk.END)
    transition1=transition1Entry.get()
    transition1Entry.delete(0, tk.END)
    return state, transition0, transition1

def on_enter(event):
    event.widget['bg']="gray"
    event.widget['fg']="black"

def on_leave(event):
    event.widget['bg']="black"
    event.widget['fg']="white"