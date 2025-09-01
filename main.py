import customtkinter as ctk
from EncryptionGameProject.auth.auth_manager import sign_up, log_in

ctk.set_appearance_mode("dark")

class EncryptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_width = 400
        self.window_height = 600
        self.title("Encryption Game")

        # Logic to make window size and make it appear in the middle of the user's screen
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (self.window_width // 2)
        y = (screen_h // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)

        # container holds the stacked frames
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # IMPORTANT FIX:
        # tell the container that its grid row 0 and column 0 should expand
        # when the container expands. This lets the frames we grid into (row=0,col=0)
        # fill the container instead of collapsing to minimal size.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SignUpFrame, LoginFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # sticky expands frame to fill cell

        self.show_frame("SignUpFrame")

    def show_frame(self, page_name: str):
        frame = self.frames[page_name]
        frame.tkraise()


class BaseAuthFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, title_text, action_text, action_command, switch_text, switch_command):
        super().__init__(parent)
        self.controller = controller


        # header
        header = ctk.CTkLabel(self, text=title_text, font=("Segoe UI", 15), wraplength=320)
        header.place(relx=0.5, rely=0.07, anchor=ctk.CENTER)

        # result label
        self.result_label = ctk.CTkLabel(self, text="", wraplength=320, font=("Segoe UI", 13))
        self.result_label.place(relx=0.5, rely=0.22, anchor=ctk.CENTER)

        # entries
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Username", width=260)
        self.entry_user.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=260)
        self.entry_pass.place(relx=0.5, rely=0.48, anchor=ctk.CENTER)

        # show/hide pass
        self.show_var = ctk.BooleanVar(value=False)
        self.checkbox = ctk.CTkCheckBox(self, text="Show password", variable=self.show_var, command=self._toggle_password)
        self.checkbox.place(relx=0.5, rely=0.56, anchor=ctk.CENTER)

        # action & switch buttons
        self.action_btn = ctk.CTkButton(self, text=action_text, width=160, height=40, command=action_command)
        self.action_btn.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        self.switch_btn = ctk.CTkButton(self, text=switch_text, width=140, height=30, fg_color="#740f85",
                                        hover_color="#560a62", command=switch_command)
        self.switch_btn.place(relx=0.5, rely=0.82, anchor=ctk.CENTER)

    def _toggle_password(self):
        if self.show_var.get():
            self.entry_pass.configure(show="")
        else:
            self.entry_pass.configure(show="*")

    def set_result(self, text, success: bool):
        color = "#268e24" if success else "#a8310d"
        self.result_label.configure(text=text, text_color=color)


class SignUpFrame(BaseAuthFrame):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title_text="Welcome! Create an account for the Encryption Game 🙃",
            action_text="Sign Up",
            action_command=self.sign_up_result,
            switch_text="Go to Login",
            switch_command=lambda: controller.show_frame("LoginFrame")
        )

    def sign_up_result(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        result = sign_up(username, password)
        success = (result == "Success!")
        self.set_result(result, success)


class LoginFrame(BaseAuthFrame):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title_text="Log in to the Encryption Game",
            action_text="Log In",
            action_command=self.log_in_result,
            switch_text="Go to Sign Up",
            switch_command=lambda: controller.show_frame("SignUpFrame")
        )

    def log_in_result(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        result = log_in(username, password)
        success = (result == "Success!")
        self.set_result(result, success)



if __name__ == "__main__":
    app = EncryptionApp()
    app.mainloop()
