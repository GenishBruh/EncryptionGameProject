


ctk.set_appearance_mode("dark")

# Simple app: one top button toggles two frames below it.
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Frame Layering — Simple Demo")
        self.geometry("400x200")

        # --- Top control: single button that switches frames ---
        self.toggle_btn = ctk.CTkButton(self, text="Show Frame 2", command=self.toggle_frames)
        self.toggle_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Make the window expand the content area
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Container where frames will be stacked (same grid cell) ---
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))

        # Ensure the container fills available space
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- Frame 1 (you can think of it as "layer 1") ---
        self.frame1 = ctk.CTkFrame(self.container)
        # Simple content so you can tell frames apart
        ctk.CTkLabel(self.frame1, text="I'm Frame 1").pack(expand=True)

        # --- Frame 2 (stacked exactly on top of frame1 in same grid cell) ---
        self.frame2 = ctk.CTkFrame(self.container)
        ctk.CTkLabel(self.frame2, text="I'm Frame 2").pack(expand=True)

        # Put both frames into the container at the same grid location
        # They are stacked; whichever we .tkraise() becomes visible on top.
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=0, column=0, sticky="nsew")

        # Start with frame1 on top
        self.current = 1
        self.frame1.tkraise()

    def toggle_frames(self):
        # Simple toggle logic: raise the other frame and update button text
        if self.current == 1:
            self.frame2.tkraise()               # bring frame2 to the front
            self.toggle_btn.configure(text="Show Frame 1")
            self.current = 2
        else:
            self.frame1.tkraise()               # bring frame1 to the front
            self.toggle_btn.configure(text="Show Frame 2")
            self.current = 1

if __name__ == "__main__":
    app = App()
    app.mainloop()
