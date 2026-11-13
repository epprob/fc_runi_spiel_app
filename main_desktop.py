import tkinter as tk

from source.Teams_Total_Vals import Teams_Total_Vals
from source.Gui import MainApplication




Teams_Objects = []
for i in range(6):
    Teams_obj = Teams_Total_Vals()
    Teams_Objects.append(Teams_obj)

root = tk.Tk()
MainApplication(root, Teams_Objects).pack(side="top", fill="both", expand=True)

root.mainloop()
