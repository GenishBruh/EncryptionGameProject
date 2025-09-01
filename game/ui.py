import customtkinter as ctk
from customtkinter import CTkButton
from pymsgbox import buttonsFrame
from urllib3.filepost import choose_boundary

from EncryptionGameProject.auth.auth_manager import sign_up, log_in
from EncryptionGameProject.encryption.caesar import caesar_cipher
from EncryptionGameProject.encryption.vigenere import vigenere_cipher
from EncryptionGameProject.encryption.zigzag import zigzag_cipher


ctk.set_appearance_mode("dark")

class BaseMenuLayout(ctk.CTk):
    def __init__(self, title):
        super().__init__()

        # Set up window boundaries and location
        self.window_width = 400
        self.window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.title(title)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

# Since we have 2 menus that are practically the same
class BaseAuthMenu(BaseMenuLayout):
    def __init__(self, title, button_text, button_command, switch_button_text, switch_command):
        super().__init__(title=title)

        # Welcome Frame
        frame1 = ctk.CTkFrame(self, width=300, height=100, corner_radius=10)
        frame1.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        self.text1 = ctk.CTkLabel(frame1, text="Welcome to my Encryption Game!\nDecrypt messages based on method & difficulty! 🙃",
                                   wraplength=280, font=("Segoe UI", 15))
        self.text1.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Result Frame
        frame2 = ctk.CTkFrame(self, width=300, height=50, corner_radius=10)
        frame2.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
        self.text2 = ctk.CTkLabel(frame2, text="", wraplength=280, font=("Segoe UI", 15))
        self.text2.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # TextBoxes to enter username/password
        self.entry1 = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry1.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.entry2 = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry2.place(relx=0.5, rely=0.57, anchor=ctk.CENTER)

        # Toggle password hiding
        self.checkbox_var = ctk.BooleanVar(value=False)
        self.checkbox = ctk.CTkCheckBox(self, text="Show Password", variable=self.checkbox_var,
                                        command=self.toggle_password)
        self.checkbox.place(relx=0.5, rely=0.63, anchor=ctk.CENTER)

        # Main action button, will have text written on it later separately
        self.button = ctk.CTkButton(self, width=140, height=40, text=button_text, corner_radius=25,
                                    hover_color="#323C69", text_color="#CAD8DB",
                                    command=button_command)
        self.button.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

        # Switch menu button
        self.switch_button = ctk.CTkButton(self, width=140, height=30, text=switch_button_text, corner_radius=25,
                                           fg_color="#740f85", hover_color="#560a62", text_color="#CAD8DB",
                                           command=switch_command)
        self.switch_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

    # Function to toggle password hiding
    def toggle_password(self):
        if self.checkbox_var.get():
            self.entry2.configure(show="")
        else:
            self.entry2.configure(show="*")

# Sign Up menu
class SignUpMenu(BaseAuthMenu):
    def __init__(self):
        super().__init__(
            title="Sign Up - Encryption Game",
            button_text="Sign Up",
            button_command=self.sign_up_result,
            switch_button_text="Go to Login",
            switch_command=self.open_login
        )


    def handle_signup(self):
        return sign_up(self.entry1.get(), self.entry2.get())

    def sign_up_result(self):
        result = self.handle_signup()
        color = "#268e24" if result == "Success!" else "#a8310d"
        self.text2.configure(text=result, text_color=color)

    def open_login(self):
        self.destroy()
        login_window = LoginMenu()
        login_window.mainloop()

# Log In menu
class LoginMenu(BaseAuthMenu):
    def __init__(self):
        super().__init__(
            title="Log In - Encryption Game",
            button_text="Log In",
            button_command=self.log_in_result,
            switch_button_text="Go to Sign Up",
            switch_command=self.open_sign_up
        )

    def handle_log_in(self):
        return log_in(self.entry1.get(), self.entry2.get())

    def log_in_result(self):
        result = self.handle_log_in()
        color = "#268e24" if result == "Success!" else "#a8310d"
        self.text2.configure(text=result, text_color=color)

        if result == "Success!":
            self.after(0, self.open_diff_menu)


    def open_sign_up(self):
        self.destroy()
        signup_window = SignUpMenu()
        signup_window.mainloop()

    def open_diff_menu(self):
        self.destroy()
        md_menu = ChooseMode()
        md_menu.mainloop()

# A parent class layout for choosing modes/difficulties
class ModeDiffMenu(BaseMenuLayout):
    def __init__(self,
                 bt1command, bt2command, bt3command,
                 ibt1command, ibt2command, ibt3command,
                 bt1color="#4CAF50", bt2color="#FFB74D", bt3color="#E57373",
                 hcolor1="#357A38", hcolor2="#B87D2F", hcolor3="#B04C4C",
                 title="Modes",
                 bt1text="button 1", bt2text="button 1", bt3text="button 1",
                 infotext="Info placeholder"
                 ):
        super().__init__(title=title)

        container1 = ctk.CTkFrame(self, width=250, height=230)
        container1.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        self.instructions = ctk.CTkLabel(container1,
                                         text=infotext, wraplength=250, font=("Arial", 18))
        self.instructions.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Create a frame for the buttons
        container2 = ctk.CTkFrame(self, width=250, height=230)
        container2.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        # Create mode buttons
        self.button1 = CTkButton(container2, text_color="black", width=100, height=35, corner_radius=25,
                                 fg_color=bt1color, command=bt1command, text=bt1text, hover_color=hcolor1)
        self.button2 = CTkButton(container2, text_color="black", width=100, height=35, corner_radius=25,
                                 fg_color=bt2color, command=bt2command, text=bt2text, hover_color=hcolor2)
        self.button3 = CTkButton(container2, text_color="black", width=100, height=35, corner_radius=25,
                                 fg_color=bt3color, command=bt3command, text=bt3text, hover_color=hcolor3)

        self.button1.place(relx=0.4, rely=0.2, anchor=ctk.CENTER)
        self.button2.place(relx=0.4, rely=0.5, anchor=ctk.CENTER)
        self.button3.place(relx=0.4, rely=0.8, anchor=ctk.CENTER)

        self.i_button1 = CTkButton(container2, text_color="black", width=34, height=34, corner_radius=17,
                                   fg_color=bt1color,command=ibt1command, text="i", hover_color=hcolor1)
        self.i_button2 = CTkButton(container2, text_color="black", width=34, height=34, corner_radius=17,
                                   fg_color=bt2color,command=ibt2command, text="i", hover_color=hcolor2)
        self.i_button3 = CTkButton(container2, text_color="black", width=34, height=34, corner_radius=17,
                                   fg_color=bt3color,command=ibt3command, text="i", hover_color=hcolor3)

        self.i_button1.place(relx=0.7, rely=0.2, anchor=ctk.CENTER)
        self.i_button2.place(relx=0.7, rely=0.5, anchor=ctk.CENTER)
        self.i_button3.place(relx=0.7, rely=0.8, anchor=ctk.CENTER)

# Choose encryption method menu
class ChooseMode(ModeDiffMenu):
    def __init__(self):
        super().__init__(title="Choose Gamemode",
                         bt1text="Caesar",
                         bt2text="Vigenere",
                         bt3text="ZigZag",
                         bt1color="#1f6aa5",
                         bt2color="#1f6aa5",
                         bt3color="#1f6aa5",
                         hcolor1="#323c69",
                         hcolor2="#323c69",
                         hcolor3="#323c69",
                         bt1command=self.caesar_diff_menu,
                         bt2command=self.vigenere_diff_menu,
                         bt3command=self.zigzag_diff_menu,
                         ibt1command=self.caesar_info,
                         ibt2command=self.vigenere_info,
                         ibt3command=self.zigzag_info,
                         infotext="Welcome! :)\n\nBelow there are 3 different encryption methods\n\n"
                                              "when you click 'i', you will be shown info about each method.\n"
                                              "Choose a method to proceed!\n\n"
                                              "Good Luck!🤗")

    def show_instructions(self, title, instructions):

        popup = ctk.CTkToplevel()  # Creates a new window on top
        popup.resizable(False, False)
        popup.title(title)
        popup.geometry("500x400")

        container = ctk.CTkFrame(popup)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(container, text=instructions, justify="left", wraplength=380, font=("Arial", 20))
        label.pack(padx=20, pady=20, fill="both", expand=True)

        close_btn = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=(0, 20))

    def caesar_info(self):
        instructions = (
            "Each letter in the message gets shifted a number of places in the alphabet, depending on the key.\n"
            "For example:\n\n"
            "Key : 2  |  ABC → CDE\n"
            "A → C | B → D | C → E\n"
            "Your task is to reverse the encryption."
        )
        self.show_instructions("Caesar Cipher Instructions", instructions)

    def vigenere_info(self):
        instructions = (
            "Each letter in the message is shifted according to the corresponding letter in the keyword.\n"
            "The keyword repeats to match the length of the message.\n"
            "For example:\n\n"
            "Keyword : ABC | Word to encrypt : Hello\n"
            "(A shifts by 1, B shifts by 2, etc.)\n\n"
            "H → I | e → g | l → o | l → m | o → q\n"
            "Hello → Igomq"
        )
        self.show_instructions("Vigenere Cipher Instructions", instructions)

    def zigzag_info(self):
        instructions = (
            "The message is written in a zigzag pattern across a set number of rows (rails).\n"
            "It is then read row by row to create the encrypted text.\n"
            "For example, with 3 rails:\n\n"
            "M . . . A . .\n"
            ". E . S . G .\n"
            ". . S . . . E\n"
            "MESSAGE → MAESGSE\n"
            "Your task is to reconstruct the zigzag to reveal the original message."
        )
        self.show_instructions("Zigzag Cipher Instructions", instructions)

    def caesar_diff_menu(self):
        self.destroy()
        cdm_window = CaesarChooseDifficulty()
        cdm_window.mainloop()

    def vigenere_diff_menu(self):
        self.destroy()
        vdm_window = VigenereChooseDifficulty()
        vdm_window.mainloop()

    def zigzag_diff_menu(self):
        self.destroy()
        zdm_window = ZigzagChooseDifficulty()
        zdm_window.mainloop()


    def RAHHHH(self):
        print("RAHHH")

# Choose difficulty for Caesar
class CaesarChooseDifficulty(ModeDiffMenu):
    def __init__(self):
        super().__init__(
                         bt1command=self.RAHHHH, bt2command=self.RAHHHH, bt3command=self.RAHHHH,
                         ibt1command=self.caesar_easy_info, ibt2command=self.caesar_medium_info, ibt3command=self.caesar_hard_info,
                         title="Choose Caesar difficulty mode",
                         bt1text="Easy", bt2text="Medium", bt3text="Hard",
                         infotext="Welcome to the Caesar difficulty selection menu!\n\n"
                                  "Click one of the difficulties below to begin.\n\n"
                                  "The info button next to each one tells you the settings for the chosen difficulty")

    def caesar_easy_info(self):
        pass

    def caesar_medium_info(self):
        pass

    def caesar_hard_info(self):
        pass

    def RAHHHH(self):
        pass

# Choose difficulty for Vigenere
class VigenereChooseDifficulty(ModeDiffMenu):
    def __init__(self):
        super().__init__(
                         bt1command=self.RAHHHH, bt2command=self.RAHHHH, bt3command=self.RAHHHH,
                         ibt1command=self.vigenere_easy_info, ibt2command=self.vigenere_medium_info, ibt3command=self.vigenere_hard_info,
                         title="Choose Vigenere difficulty mode",
                         bt1text="button 1", bt2text="button 1", bt3text="button 1",
                         infotext="Welcome to the Vigenere difficulty selection menu!\n\n"
                                  "Click one of the difficulties below to begin.\n\n"
                                  "The info button next to each one tells you the settings for the chosen difficulty")

    def vigenere_easy_info(self):
        pass

    def vigenere_medium_info(self):
        pass

    def vigenere_hard_info(self):
        pass

    def RAHHHH(self):
        pass

# Choose difficulty for Zigzag
class ZigzagChooseDifficulty(ModeDiffMenu):
    def __init__(self):
        super().__init__(
                         bt1command=self.RAHHHH, bt2command=self.RAHHHH, bt3command=self.RAHHHH,
                         ibt1command=self.zigzag_easy_info, ibt2command=self.zigzag_medium_info, ibt3command=self.zigzag_hard_info,
                         title="Choose Zigzag difficulty mode",
                         bt1text="button 1", bt2text="button 1", bt3text="button 1",
                         infotext="Welcome to the Zigzag difficulty selection menu!\n\n"
                                  "Click one of the difficulties below to begin.\n\n"
                                  "The info button next to each one tells you the settings for the chosen difficulty")

    def zigzag_easy_info(self):
        pass

    def zigzag_medium_info(self):
        pass

    def zigzag_hard_info(self):
        pass

    def RAHHHH(self):
        pass



if __name__ == "__main__":
    app = SignUpMenu()
    app.resizable(False, False)
    app.mainloop()
