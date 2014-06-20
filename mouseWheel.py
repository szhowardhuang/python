# explore the mouse wheel with the Tkinter GUI toolkit
# Windows and Linux generate different events
# tested with Python25

import Tkinter as tk

def mouse_wheel(event):
    global count
    # respond to Linux or Windows wheel event
    if event.num == 5 or event.delta == -28:
        count -= 1
    if event.num == 4 or event.delta == 28:
        count += 1
    label['text'] = count
    print event.type
    print event.delta

count = 0
root = tk.Tk()
root.title('turn mouse wheel')
root['bg'] = 'darkgreen'

# with Windows OS
root.bind("<MouseWheel>", mouse_wheel)
# with Linux OS
root.bind("<Button-4>", mouse_wheel)
root.bind("<Button-5>", mouse_wheel)
root.bind("<Button-1>", mouse_wheel)
root.bind("<Button-2>", mouse_wheel)
root.bind("<Button-3>", mouse_wheel)

label = tk.Label(root, font=('courier', 18, 'bold'), width=10)
label.pack(padx=40, pady=40)

root.mainloop()
