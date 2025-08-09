import tkinter as tk
from tkinter import scrolledtext
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Ensure NLTK data is available
nltk.download('punkt', quiet=True)

# Load FAQs
with open("faqs.json", "r") as f:
    faqs = json.load(f)

# Preprocess text
def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    return " ".join(tokens)

questions = [preprocess(faq["question"]) for faq in faqs]
answers = [faq["answer"] for faq in faqs]

# Vectorize questions
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# Chatbot response function
def get_response(user_input):
    user_input_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_input_processed])
    similarities = cosine_similarity(user_vector, question_vectors)
    best_match_index = similarities.argmax()
    return answers[best_match_index]

# GUI setup
root = tk.Tk()
root.title("FAQ Chatbot")
root.geometry("500x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state="disabled")
chat_area.pack(padx=10, pady=10)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=5)

user_entry = tk.Entry(entry_frame, width=40)
user_entry.pack(side=tk.LEFT, padx=5)

def send_message():
    user_text = user_entry.get().strip()
    if user_text:
        chat_area.config(state="normal")
        chat_area.insert(tk.END, f"You: {user_text}\n")
        bot_response = get_response(user_text)
        chat_area.insert(tk.END, f"Bot: {bot_response}\n\n")
        chat_area.config(state="disabled")
        chat_area.yview(tk.END)
        user_entry.delete(0, tk.END)

send_button = tk.Button(entry_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

root.mainloop()
