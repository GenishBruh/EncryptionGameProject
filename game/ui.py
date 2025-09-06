import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel
import random

from EncryptionGameProject.auth.auth_manager import sign_up, log_in, get_file_data, update_data
from EncryptionGameProject.encryption.caesar import caesar_cipher
from EncryptionGameProject.encryption.vigenere import vigenere_cipher
from EncryptionGameProject.encryption.zigzag import zigzag_cipher
from EncryptionGameProject.game.utils import (DIFFICULTY_INFO, ENCRYPTION_INFO,
                                              GAME_CONFIG)
from EncryptionGameProject.auth.session import set_current_user, get_current_user


ctk.set_appearance_mode("dark")


class BaseMenuLayout(ctk.CTk):
    def __init__(self, title, window_width=400, window_height=600):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.title(title)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def transfer_menu(self, next_class):
        self.destroy()
        window = next_class()
        window.mainloop()

    def back_btn(self, command):
        self.back_frame = ctk.CTkFrame(self, width=75, height=40)
        self.back_frame.place(x=0, y=0, anchor=ctk.NW)
        # renamed attribute so it does not shadow the method name
        self.back_button = ctk.CTkButton(
            self.back_frame,
            width=60,
            text="BACK",
            command=command
        )
        self.back_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def test_btn(self):
        self.test_frame = ctk.CTkFrame(self, width=75, height=40)
        self.test_frame.place(relx=1, y=0, anchor=ctk.NE)
        # renamed attribute
        self.test_button = ctk.CTkButton(
            self.test_frame,
            width=60,
            text="TEST",
            command=lambda: self.transfer_menu(ChooseMode)
        )
        self.test_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

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
            switch_command=lambda: self.transfer_menu(LoginMenu)
        )

        self.test_btn()

    def handle_signup(self):
        return sign_up(self.entry1.get(), self.entry2.get())

    def sign_up_result(self):
        result = self.handle_signup()
        color = "#268e24" if result == "Success!" else "#a8310d"
        self.text2.configure(text=result, text_color=color)

# Log In menu
class LoginMenu(BaseAuthMenu):
    def __init__(self):
        super().__init__(
            title="Log In - Encryption Game",
            button_text="Log In",
            button_command=self.log_in_result,
            switch_button_text="Go to Sign Up",
            switch_command=lambda: self.transfer_menu(SignUpMenu)
        )

    def handle_log_in(self):
        return log_in(self.entry1.get(), self.entry2.get())


    def log_in_result(self):
        result = self.handle_log_in()
        color = "#268e24" if result == "Success!" else "#a8310d"
        self.text2.configure(text=result, text_color=color)

        if result == "Success!":
            set_current_user(self.entry1.get())
            self.after(400, lambda: self.transfer_menu(ChooseMode))

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

    def show_instructions(self, title, instructions, winx, winy):
        popup = ctk.CTkToplevel()  # Creates a new window on top
        popup.resizable(False, False)
        popup.title(title)
        popup.geometry(f"{winx}x{winy}")

        container = ctk.CTkFrame(popup)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(container, text=instructions, justify="left", wraplength=380, font=("Arial", 20))
        label.pack(padx=20, pady=20, fill="both", expand=True)

        close_btn = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=(0, 20))

    def display_info(self, dict, name, winx=450, winy=400):
        instructions = dict[name]
        self.show_instructions(f"{name.title()} - Info", instructions, winx, winy)

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
                         bt1command=lambda: self.transfer_menu(CaesarChooseDifficulty),
                         bt2command=lambda: self.transfer_menu(VigenereChooseDifficulty),
                         bt3command=lambda: self.transfer_menu(ZigzagChooseDifficulty),
                         ibt1command=lambda: self.display_info(dict=ENCRYPTION_INFO, name="caesar"),
                         ibt2command=lambda: self.display_info(dict=ENCRYPTION_INFO, name="vigenere"),
                         ibt3command=lambda: self.display_info(dict=ENCRYPTION_INFO, name="zigzag"),
                         infotext="Welcome! :)\n\nBelow there are 3 different encryption methods\n\n"
                                  "when you click 'i', you will be shown info about each method.\n"
                                  "Choose a method to proceed!\n\n"
                                  "Good Luck!🤗")

        # Leaderboard button (place near bottom)
        self.leaderboard_button = ctk.CTkButton(self,
                                                text="Leaderboard",
                                                width=140,
                                                command=lambda: self.transfer_menu(LeaderboardMenu))
        self.leaderboard_button.place(relx=0.5, rely=0.93, anchor=ctk.CENTER)

# Leaderboard menu
class LeaderboardMenu(BaseMenuLayout):
    def __init__(self, limit=10):
        super().__init__(title="Leaderboard", window_width=420, window_height=520)
        self.back_btn(lambda: self.transfer_menu(ChooseMode))

        data = get_file_data() or {}
        # Build list of (username, score) where score is int
        entries = []
        for u, info in data.items():
            score = info.get("score")
            if isinstance(score, int):
                entries.append((u, score))
        entries.sort(key=lambda x: x[1], reverse=True)
        top = entries[:limit]

        header = ctk.CTkLabel(self, text=f"Top {len(top)} Players", font=("Arial", 28))
        header.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        box = ctk.CTkFrame(self, width=360, height=360)
        box.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

        if not top:
            msg = "No scores yet."
        else:
            lines = []
            rank = 1
            for user, score in top:
                lines.append(f"{rank:>2}. {user}  -  {score}")
                rank += 1
            msg = "\n".join(lines)

        lbl = ctk.CTkLabel(box, text=msg, font=("Consolas", 18), justify="left")
        lbl.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

# Choose difficulty for Caesar
class CaesarChooseDifficulty(ModeDiffMenu):
    def __init__(self):
        super().__init__(
                         bt1command=lambda: self.transfer_menu(lambda: GamePlayMenu("caesar", "easy")),  # pass a function to be invoked on click
                         bt2command=lambda: self.transfer_menu(lambda: GamePlayMenu("caesar", "medium")),
                         bt3command=lambda: self.transfer_menu(lambda: GamePlayMenu("caesar", "hard")),
                         ibt1command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Caesar Easy"),
                         ibt2command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Caesar Medium"),
                         ibt3command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Caesar Hard"),
                         title="Choose Caesar difficulty mode",
                         bt1text="Easy", bt2text="Medium", bt3text="Hard",
                         infotext="Welcome to the Caesar difficulty selection menu!\n\n"
                                  "Click one of the difficulties below to begin.\n\n"
                                  "The info button next to each one tells you the settings for the chosen difficulty")

        self.back_btn(lambda: self.transfer_menu(ChooseMode))


    def RAHHHH(self):
        pass

# Choose difficulty for Vigenere
class VigenereChooseDifficulty(ModeDiffMenu):
    def __init__(self):
        super().__init__(
                         bt1command=lambda: self.transfer_menu(lambda: GamePlayMenu("vigenere", "easy")),  # pass a function to be invoked on click
                         bt2command=lambda: self.transfer_menu(lambda: GamePlayMenu("vigenere", "medium")),
                         bt3command=lambda: self.transfer_menu(lambda: GamePlayMenu("vigenere", "hard")),
                         ibt1command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Vigenere Easy"),
                         ibt2command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Vigenere Medium"),
                         ibt3command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Vigenere Hard"),
                         title="Choose Vigenere difficulty mode",
                         bt1text="Easy", bt2text="Medium", bt3text="Hard",
                         infotext="Welcome to the Vigenere difficulty selection menu!\n\n"
                                  "Click one of the difficulties below to begin.\n\n"
                                  "The info button next to each one tells you the settings for the chosen difficulty")

        self.back_btn(lambda: self.transfer_menu(ChooseMode))

    def RAHHHH(self):
        pass

# Choose difficulty for Zigzag
class ZigzagChooseDifficulty(ModeDiffMenu):
    def __init__(self):
        super().__init__(
                         bt1command=lambda: self.transfer_menu(lambda: GamePlayMenu("zigzag", "easy")),
                         bt2command=lambda: self.transfer_menu(lambda: GamePlayMenu("zigzag", "medium")),
                         bt3command=lambda: self.transfer_menu(lambda: GamePlayMenu("zigzag", "hard")),
                         ibt1command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Zigzag Easy"),
                         ibt2command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Zigzag Medium"),
                         ibt3command=lambda: self.display_info(dict=DIFFICULTY_INFO, name="Zigzag Hard"),
                         title="Choose Zigzag difficulty mode",
                         bt1text="Easy", bt2text="Medium", bt3text="Hard",
                         infotext="Welcome to the Zigzag difficulty selection menu!\n\n"
                                  "Click one of the difficulties below to begin.\n\n"
                                  "The info button next to each one tells you the settings for the chosen difficulty")

        self.back_btn(lambda: self.transfer_menu(ChooseMode))


class GamePlayMenu(BaseMenuLayout):
    def __init__(self, method, difficulty):
        super().__init__(title="Game!", window_width=600, window_height=400)

        self.method = method.lower()
        self.difficulty = difficulty.lower()
        self.username = get_current_user()
        self.data = get_file_data()
        self.solved = False

        key_id = f"{self.difficulty}_{self.method}"
        self.config = GAME_CONFIG[key_id]

        # Scoring / hint tracking
        self.base_score = self.config["score_given"]
        self.hint_uses = 0
        self.deduction_unit = max(1, self.base_score // 4)  # linear 25% chunks, at least 1
        self.current_award = self.base_score

        # Prepare puzzle
        self.generate_puzzle()

        self.back_btn(lambda: self.transfer_menu(ChooseMode))

        self.time_left = self.config["timer_counts"]

        self.game_frame = ctk.CTkFrame(self, width=450, height=300)
        self.game_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Cipher display
        self.cipher_label = ctk.CTkLabel(
            self.game_frame,
            text=f"Cipher:\n{self.cipher_text}",
            font=("Arial", 30),
            wraplength=480,
            justify="center"
        )
        self.cipher_label.place(relx=0.5, rely=0.16, anchor=ctk.CENTER)

        # Timer
        self.timer_label = ctk.CTkLabel(self.game_frame, text=f"Time: {self.time_left}", font=("Arial", 28))
        self.timer_label.place(relx=0.5, rely=0.33, anchor=ctk.CENTER)

        # Potential score label
        self.potential_label = ctk.CTkLabel(
            self.game_frame,
            text=f"Potential Score: {self.current_award}",
            font=("Arial", 18)
        )
        self.potential_label.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        # Feedback
        self.feedback_label = ctk.CTkLabel(self.game_frame, text="", font=("Arial", 18))
        self.feedback_label.place(relx=0.5, rely=0.57, anchor=ctk.CENTER)

        # Hint label
        self.hint_label = ctk.CTkLabel(self.game_frame, text="", font=("Arial", 16), wraplength=480)
        self.hint_label.place(relx=0.5, rely=0.93, anchor=ctk.CENTER)

        # Input
        self.answer_box = ctk.CTkEntry(self.game_frame, placeholder_text="Type decrypted word...", width=200)
        self.answer_box.place(relx=0.35, rely=0.82, anchor=ctk.CENTER)
        self.answer_box.bind("<Return>", self.check_answer)

        # Answer button
        self.answer_button = ctk.CTkButton(
            self.game_frame,
            text="Answer",
            width=90,
            command=lambda: self.check_answer()
        )
        self.answer_button.place(relx=0.5, rely=0.69, anchor=ctk.CENTER)

        # Hint button
        self.hint_button = ctk.CTkButton(
            self.game_frame,
            text="Hint (-25%)",
            width=110,
            command=self.use_hint
        )
        self.hint_button.place(relx=0.75, rely=0.82, anchor=ctk.CENTER)

        self.countdown()

    def debug_print(self, tag):
        try:
            user_score = self.data[self.username]["score"] if self.username in self.data else "N/A"
        except Exception:
            user_score = "ERR"
        snippet = {k: self.data[k] for k in list(self.data)[:5]}  # small snapshot
        print(f"[DEBUG:{tag}] username={self.username}")
        print(f"[DEBUG:{tag}] user_score_current={user_score}")
        print(f"[DEBUG:{tag}] base_score={self.base_score} current_award={self.current_award} hint_uses={self.hint_uses} deduction_unit={self.deduction_unit}")
        print(f"[DEBUG:{tag}] plain(right_answer)={self.right_answer} meta={self.meta}")
        print(f"[DEBUG:{tag}] cipher={self.cipher_text}")
        print(f"[DEBUG:{tag}] data_snapshot_keys={list(snippet.keys())}")
        print(f"[DEBUG:{tag}] full_user_entry={self.data.get(self.username)}")

    def generate_puzzle(self):
        word_func = self.config["word"]
        plain = word_func()
        meta = {}

        if self.method == "caesar":
            key = random.randint(*self.config["key_range"])
            cipher = caesar_cipher(plain, key)
            meta["key"] = key
        elif self.method == "vigenere":
            start, end = self.config["key_range"]
            letters = [chr(c) for c in range(ord(start), ord(end) + 1)]
            key_length = self.config["key_length"]
            keyword = "".join(random.choice(letters) for _ in range(key_length))
            cipher = vigenere_cipher(plain, keyword)
            meta["key"] = keyword
        elif self.method == "zigzag":
            rails = self.config["rails"]
            cipher = zigzag_cipher(plain, rails)
            meta["rails"] = rails
        else:
            cipher = plain

        self.right_answer = plain
        self.cipher_text = cipher
        self.meta = meta
        self.debug_print("PUZZLE_GEN")

    def build_hint(self):
        # Progressive hints
        p = self.right_answer
        length = len(p)
        h_index = self.hint_uses  # about to show after increment
        hints = []

        # Generic pattern helpers
        def pattern(reveal):
            return "".join(c if i < reveal else "_" for i, c in enumerate(p))

        # Base hints
        hints.append(f"Length: {length}, starts with '{p[0]}'")
        if length >= 3:
            hints.append(f"First 2 letters: {p[:2]}, last letter: {p[-1]}")
        else:
            hints.append(f"First letter again: {p[0]}")
        if self.method in ("caesar", "vigenere"):
            key_val = self.meta.get("key")
            hints.append(f"Key: {key_val}")
        elif self.method == "zigzag":
            rails = self.meta.get("rails")
            hints.append(f"Rails: {rails}")
        hints.append(f"Pattern reveal (50%): {pattern(max(1, length // 2))}")
        hints.append(f"Full answer: {p}")

        # Clamp index
        use = min(h_index - 1, len(hints) - 1)
        return hints[use]

    def use_hint(self):
        if self.solved or self.time_left <= 0:
            return
        if self.current_award == 0:
            self.hint_label.configure(text="No score left to deduct.")
            return

        self.hint_uses += 1
        # Linear deduction
        self.current_award = max(self.base_score - self.hint_uses * self.deduction_unit, 0)

        hint_text = self.build_hint()
        self.hint_label.configure(text=f"Hint {self.hint_uses}: {hint_text}")
        self.potential_label.configure(text=f"Potential Score: {self.current_award}")
        if self.current_award == 0:
            self.hint_button.configure(state="disabled")

        self.debug_print("HINT")

    def countdown(self):
        if self.time_left > 0 and not self.solved:
            self.timer_label.configure(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.after(1000, self.countdown)
        elif not self.solved:
            self.timer_label.configure(text="Time's up! You lost!")
            self.answer_box.configure(state="disabled")
            self.answer_button.configure(state="disabled")
            self.hint_button.configure(state="disabled")
            self.feedback_label.configure(text=f"Plain: {self.right_answer}")
            self.debug_print("TIME_UP")
            self.after(2000, lambda: self.transfer_menu(ChooseMode))

    def check_answer(self, event=None):
        if self.solved:
            return
        guess = self.answer_box.get().strip().lower()
        if guess == self.right_answer:
            self.answer_button.configure(state="disabled")
            self.solved = True
            score = self.current_award
            if self.username in self.data and isinstance(self.data[self.username].get("score"), int):
                self.data[self.username]["score"] += score
                update_data(self.data)

            meta_info = ""
            if "key" in self.meta:
                meta_info = f" (key: {self.meta['key']})"
            elif "rails" in self.meta:
                meta_info = f" (rails: {self.meta['rails']})"

            self.feedback_label.configure(
                text=f"Correct! +{score} score!{meta_info}",
                text_color="#268e24"
            )
            self.answer_box.configure(state="disabled")
            self.hint_button.configure(state="disabled")
            self.potential_label.configure(text=f"Awarded: {score}")
            self.debug_print("SOLVED")
            self.after(1800, lambda: self.transfer_menu(ChooseMode))
        else:
            self.feedback_label.configure(text="Wrong, try again!", text_color="#a8310d")
            self.debug_print("WRONG_GUESS")


if __name__ == "__main__":
    app = SignUpMenu()
    app.mainloop()