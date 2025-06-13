import tkinter as tk

def edit_orientation(controller, quad_index, callback):
    """Petite fenêtre modale : choisit rotation (0/90/180/270) + miroir"""
    root = controller.winfo_toplevel()
    win = tk.Toplevel(root)
    win.title(f"Orientation Quadrant {quad_index + 1}")
    win.grab_set()

    rot_var = tk.IntVar(value=0)
    mir_var = tk.BooleanVar(value=False)

    tk.Label(win, text="Rotation").pack(pady=5)
    for k, txt in enumerate(("0°", "90°", "180°", "270°")):
        tk.Radiobutton(win, text=txt, variable=rot_var, value=k).pack(anchor="w")

    tk.Checkbutton(win, text="Miroir horizontal", variable=mir_var).pack(pady=5)

    def validate():
        win.grab_release()
        win.destroy()
        callback(rot_var.get(), mir_var.get())

    tk.Button(win, text="Valider", command=validate).pack(pady=10)
