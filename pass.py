import random
import string
import secrets
import tkinter as tk
from tkinter import messagebox, simpledialog

class PasswordGenerator:
    """
    A class to generate strong, random passwords with user-specified criteria.
    """
    def __init__(self):
        self.min_length = 10  # Minimum password length
        self.max_length = 128 #maximum password length
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_special_chars = True
        self.avoid_ambiguous_chars = True # Avoid characters like l, 1, o, 0, i

    def generate_password(self):
        """
        Generates a strong, random password based on the current criteria.

        Returns:
            str: The generated password.

        Raises:
            ValueError: If the password length is invalid or if no character
                        types are selected.
        """
        if not (self.include_uppercase or self.include_lowercase or
                self.include_numbers or self.include_special_chars):
            raise ValueError("At least one character type must be selected.")

        if not (self.min_length <= self.max_length):
            raise ValueError("Minimum length must be less than or equal to maximum length.")
        
        length = random.randint(self.min_length, self.max_length) #randomize the length

        char_pool = ''
        if self.include_uppercase:
            char_pool += string.ascii_uppercase
        if self.include_lowercase:
            char_pool += string.ascii_lowercase
        if self.include_numbers:
            char_pool += string.digits
        if self.include_special_chars:
            char_pool += string.punctuation
        if self.avoid_ambiguous_chars:
            ambiguous = 'l1o0iI'
            char_pool = ''.join(c for c in char_pool if c not in ambiguous)

        if not char_pool:
             raise ValueError("Character pool is empty.  Check your settings.")
        
        # Use secrets.choice() for cryptographically secure random selection
        password = ''.join(secrets.choice(char_pool) for _ in range(length))
        return password

class PasswordManagerGUI:
    """
    A GUI for the password manager application.
    """
    def __init__(self, master):
        self.master = master
        master.title("Password Manager")
        master.geometry("400x300")  # Increased size for better layout

        self.password_generator = PasswordGenerator()

        # Labels
        self.length_label = tk.Label(master, text="Password Length:")
        self.length_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        self.uppercase_label = tk.Label(master, text="Include Uppercase:")
        self.uppercase_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        self.lowercase_label = tk.Label(master, text="Include Lowercase:")
        self.lowercase_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.numbers_label = tk.Label(master, text="Include Numbers:")
        self.numbers_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self.special_chars_label = tk.Label(master, text="Include Special Chars:")
        self.special_chars_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.ambiguous_chars_label = tk.Label(master, text="Avoid Ambiguous Chars:")
        self.ambiguous_chars_label.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)

        # Entry for password length
        self.min_length_entry = tk.Entry(master, width=10)
        self.min_length_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        self.min_length_entry.insert(0, str(self.password_generator.min_length))  # Default value

        self.max_length_entry = tk.Entry(master, width=10)
        self.max_length_entry.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        self.max_length_entry.insert(0, str(self.password_generator.max_length))

        # Checkboxes
        self.uppercase_var = tk.BooleanVar()
        self.uppercase_check = tk.Checkbutton(master, variable=self.uppercase_var,
                                             onvalue=True, offvalue=False)
        self.uppercase_check.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        self.uppercase_var.set(self.password_generator.include_uppercase)  # Default value

        self.lowercase_var = tk.BooleanVar()
        self.lowercase_check = tk.Checkbutton(master, variable=self.lowercase_var,
                                             onvalue=True, offvalue=False)
        self.lowercase_check.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        self.lowercase_var.set(self.password_generator.include_lowercase)  # Default value

        self.numbers_var = tk.BooleanVar()
        self.numbers_check = tk.Checkbutton(master, variable=self.numbers_var,
                                           onvalue=True, offvalue=False)
        self.numbers_check.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        self.numbers_var.set(self.password_generator.include_numbers)  # Default value

        self.special_chars_var = tk.BooleanVar()
        self.special_chars_check = tk.Checkbutton(master, variable=self.special_chars_var,
                                                 onvalue=True, offvalue=False)
        self.special_chars_check.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
        self.special_chars_var.set(self.password_generator.include_special_chars)  # Default value

        self.ambiguous_chars_var = tk.BooleanVar()
        self.ambiguous_chars_check = tk.Checkbutton(master, variable=self.ambiguous_chars_var,
                                                 onvalue=True, offvalue=False)
        self.ambiguous_chars_check.grid(row=5, column=1, sticky=tk.W, padx=10, pady=5)
        self.ambiguous_chars_var.set(self.password_generator.avoid_ambiguous_chars)

        # Buttons
        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_and_show_password)
        self.generate_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=master.destroy)
        self.exit_button.grid(row=6, column=2, pady=10)

        # Password display
        self.password_label = tk.Label(master, text="Generated Password:", font=('Arial', 12))
        self.password_label.grid(row=7, column=0, columnspan=3, pady=5)
        self.generated_password_var = tk.StringVar()
        self.generated_password_label = tk.Label(master, textvariable=self.generated_password_var,
                                                font=('Arial', 14, 'bold'), wraplength=380)  # Use wraplength
        self.generated_password_label.grid(row=8, column=0, columnspan=3, pady=5)

    def generate_and_show_password(self):
        """
        Generates a password and displays it in a message box.
        """
        try:
            # Get user inputs from GUI
            min_length = int(self.min_length_entry.get())
            max_length = int(self.max_length_entry.get())
            include_uppercase = self.uppercase_var.get()
            include_lowercase = self.lowercase_var.get()
            include_numbers = self.numbers_var.get()
            include_special_chars = self.special_chars_var.get()
            avoid_ambiguous = self.ambiguous_chars_var.get()

            # Update the password generator's settings
            self.password_generator.min_length = min_length
            self.password_generator.max_length = max_length
            self.password_generator.include_uppercase = include_uppercase
            self.password_generator.include_lowercase = include_lowercase
            self.password_generator.include_numbers = include_numbers
            self.password_generator.include_special_chars = include_special_chars
            self.password_generator.avoid_ambiguous_chars = avoid_ambiguous
            # Generate the password
            password = self.password_generator.generate_password()
            self.generated_password_var.set(password)  # Update the label
            messagebox.showinfo("Generated Password", password) #show a message box

        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    gui = PasswordManagerGUI(root)
    root.mainloop()
