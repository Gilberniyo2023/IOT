# -*- coding: utf-8 -*-
"""
Advanced AI-Powered Password Generator with Strength Prediction
---------------------------------------------------------------
Now includes:
- Machine Learning strength prediction
- Dynamic password mutation
- Entropy feature
- Auto model saving/loading
- GUI with Tkinter
"""

import os
import string
import random
import secrets
import numpy as np
import joblib
import tkinter as tk
from tkinter import messagebox
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class PasswordGenerator:
    def __init__(self):
        self.min_length = 10
        self.max_length = 128
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_special_chars = True
        self.avoid_ambiguous_chars = True

        self.model = None
        self.scaler = None
        self.model_path = "password_strength_model.joblib"
        self.scaler_path = "password_scaler.joblib"

        self.load_model()

    def generate_password(self):
        if not (self.include_uppercase or self.include_lowercase or
                self.include_numbers or self.include_special_chars):
            raise ValueError("At least one character type must be selected.")

        length = random.randint(self.min_length, self.max_length)

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
            ambiguous = 'l1Io0O'
            char_pool = ''.join(c for c in char_pool if c not in ambiguous)

        if not char_pool:
            raise ValueError("Character pool is empty.")

        password = ''.join(secrets.choice(char_pool) for _ in range(length))

        # Enhance with ML Prediction
        if self.model:
            features = self.extract_features(password)
            features_scaled = self.scaler.transform([features])
            prediction = self.model.predict_proba(features_scaled)[0][1]  # confidence of being strong

            if prediction < 0.6:  # If predicted weak, mutate
                # Add more complexity
                for _ in range(3):
                    index = random.randint(0, len(password) - 1)
                    replacement = secrets.choice(string.punctuation + string.digits)
                    password = password[:index] + replacement + password[index+1:]

        return password

    def extract_features(self, password):
        upper = sum(1 for c in password if c.isupper())
        lower = sum(1 for c in password if c.islower())
        digits = sum(1 for c in password if c.isdigit())
        special = sum(1 for c in password if c in string.punctuation)
        length = len(password)

        # Entropy
        entropy = 0
        if length > 0:
            freqs = {c: password.count(c)/length for c in set(password)}
            entropy = -sum(p * np.log2(p) for p in freqs.values())

        return [upper, lower, digits, special, length, entropy]

    def create_training_data(self, n=30000):
        X, y = [], []
        for _ in range(n):
            length = random.randint(8, 20)
            flags = [random.choice([True, False]) for _ in range(4)]
            char_pool = ''
            if flags[0]: char_pool += string.ascii_uppercase
            if flags[1]: char_pool += string.ascii_lowercase
            if flags[2]: char_pool += string.digits
            if flags[3]: char_pool += string.punctuation
            if not char_pool: char_pool = string.ascii_letters

            password = ''.join(secrets.choice(char_pool) for _ in range(length))
            features = self.extract_features(password)
            label = 1 if length >= 12 and sum(flags) >= 3 else 0  # Strong if complex
            X.append(features)
            y.append(label)
        return X, y

    def train_model(self):
        if os.path.exists(self.model_path):
            print("[INFO] Loading existing model.")
            self.load_model()
            return

        print("[INFO] Training model...")
        X, y = self.create_training_data()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500,
                                   activation='relu', solver='adam', random_state=42,
                                   early_stopping=True)
        self.model.fit(X_train_scaled, y_train)
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"[INFO] Model trained. Accuracy: {accuracy:.2f}")

        self.save_model()

    def save_model(self):
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("[INFO] Model and scaler saved.")

    def load_model(self):
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print("[INFO] Model and scaler loaded.")
        except Exception:
            print("[WARNING] Model not found or corrupted. Retraining...")
            self.train_model()

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Password Manager")
        self.root.geometry("420x300")

        self.generator = PasswordGenerator()

        tk.Label(root, text="Min Length").grid(row=0, column=0)
        self.min_entry = tk.Entry(root)
        self.min_entry.insert(0, "12")
        self.min_entry.grid(row=0, column=1)

        tk.Label(root, text="Max Length").grid(row=0, column=2)
        self.max_entry = tk.Entry(root)
        self.max_entry.insert(0, "20")
        self.max_entry.grid(row=0, column=3)

        # Check buttons
        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.num = tk.BooleanVar(value=True)
        self.spec = tk.BooleanVar(value=True)
        self.amb = tk.BooleanVar(value=True)

        self.add_check("Uppercase", self.upper, 1)
        self.add_check("Lowercase", self.lower, 2)
        self.add_check("Numbers", self.num, 3)
        self.add_check("Special Chars", self.spec, 4)
        self.add_check("Avoid Ambiguous", self.amb, 5)

        self.pass_var = tk.StringVar()
        tk.Label(root, textvariable=self.pass_var, font=('Arial', 12), fg='blue').grid(row=6, column=0, columnspan=4)

        tk.Button(root, text="Generate", command=self.generate).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Exit", command=root.quit).grid(row=7, column=2, columnspan=2)

    def add_check(self, text, var, row):
        tk.Checkbutton(self.root, text=text, variable=var).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=10)

    def generate(self):
        try:
            self.generator.min_length = int(self.min_entry.get())
            self.generator.max_length = int(self.max_entry.get())
            self.generator.include_uppercase = self.upper.get()
            self.generator.include_lowercase = self.lower.get()
            self.generator.include_numbers = self.num.get()
            self.generator.include_special_chars = self.spec.get()
            self.generator.avoid_ambiguous_chars = self.amb.get()

            password = self.generator.generate_password()
            self.pass_var.set(f"Generated: {password}")
            messagebox.showinfo("Password", password)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
