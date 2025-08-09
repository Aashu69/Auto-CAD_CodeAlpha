import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyperclip
import pyttsx3
import os

# Initialize translator & TTS engine
translator = Translator()
tts_engine = pyttsx3.init()

def translate_text():
    text = source_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text to translate.")
        return
    
    src_lang = source_lang.get()
    tgt_lang = target_lang.get()
    
    try:
        translated = translator.translate(text, src=src_lang, dest=tgt_lang)
        translated_text.delete("1.0", tk.END)
        translated_text.insert(tk.END, translated.text)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {e}")

def copy_text():
    text = translated_text.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Translated text copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No text to copy.")

def speak_text():
    text = translated_text.get("1.0", tk.END).strip()
    if text:
        tts_engine.say(text)
        tts_engine.runAndWait()
    else:
        messagebox.showwarning("Warning", "No text to speak.")

# GUI Setup
root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("600x400")

# Optional icon
icon_path = os.path.join("assets", "icon.png")
if os.path.exists(icon_path):
    root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Language dropdowns
langs = list(LANGUAGES.keys())

source_lang = ttk.Combobox(root, values=langs, width=15)
source_lang.set("en")  # default English
source_lang.grid(row=0, column=0, padx=10, pady=10)

target_lang = ttk.Combobox(root, values=langs, width=15)
target_lang.set("hi")  # default Hindi
target_lang.grid(row=0, column=2, padx=10, pady=10)

# Text Areas
source_text = tk.Text(root, height=8, width=50)
source_text.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

translated_text = tk.Text(root, height=8, width=50)
translated_text.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# Buttons
translate_btn = tk.Button(root, text="Translate", command=translate_text)
translate_btn.grid(row=2, column=1, pady=5)

copy_btn = tk.Button(root, text="Copy", command=copy_text)
copy_btn.grid(row=4, column=0, pady=5)

speak_btn = tk.Button(root, text="Speak", command=speak_text)
speak_btn.grid(row=4, column=2, pady=5)

root.mainloop()
