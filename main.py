# main.py
from tkinter import *
from question_model import Question
from data import get_question_data
from quiz_brain import QuizBrain
from ui import QuizInterface
from datetime import datetime
import csv

# ---------- Global Variables ----------
user_data = []
current_user_index = 0
all_scores = []

def collect_names():
    global total_users
    try:
        total_users = int(user_count_entry.get())
        root.destroy()
        ask_user_details()
    except ValueError:
        user_count_entry.delete(0, END)
        user_count_entry.insert(0, "Enter a number")

def ask_user_details():
    global user_window, name_entry, category_var, difficulty_var
    user_window = Tk()
    user_window.title(f"User {len(user_data)+1} Details")
    user_window.config(padx=20, pady=20)

    Label(user_window, text="Enter your name:").pack()
    name_entry = Entry(user_window, width=30)
    name_entry.pack()

    Label(user_window, text="Select Category:").pack()
    category_var = StringVar(user_window)
    category_var.set("9")  # Default: General Knowledge
    OptionMenu(user_window, category_var, "9", "18", "21", "22", "23").pack()

    Label(user_window, text="Select Difficulty:").pack()
    difficulty_var = StringVar(user_window)
    difficulty_var.set("easy")
    OptionMenu(user_window, difficulty_var, "easy", "medium", "hard").pack()

    Button(user_window, text="Next", command=save_user_info).pack(pady=10)

def save_user_info():
    name = name_entry.get()
    category = category_var.get()
    difficulty = difficulty_var.get()
    user_data.append({
        "name": name,
        "category": category,
        "difficulty": difficulty
    })
    user_window.destroy()
    if len(user_data) < total_users:
        ask_user_details()
    else:
        start_next_quiz()

def start_next_quiz():
    global current_user_index
    user = user_data[current_user_index]
    question_data = get_question_data(amount=10, category=user["category"], difficulty=user["difficulty"])

    question_bank = []
    for question in question_data:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    QuizInterface(quiz, username=user["name"], on_quiz_end=quiz_finished)

def quiz_finished(score, incorrect_questions):
    global current_user_index
    user = user_data[current_user_index]
    all_scores.append((user["name"], score, incorrect_questions))

    with open("quiz_results.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user["name"], score, user["category"], user["difficulty"], datetime.now()])

    current_user_index += 1

    if current_user_index < len(user_data):
        start_next_quiz()
    else:
        show_final_results()

def show_final_results():
    result_window = Tk()
    result_window.title("Quiz Results")
    result_window.config(padx=20, pady=20)

    Label(result_window, text="Quiz Over! Scores:").pack()

    for name, score, mistakes in all_scores:
        Label(result_window, text=f"{name}: {score}/10").pack()
        if mistakes:
            Label(result_window, text="❌ Mistakes:", font=("Arial", 10, "bold")).pack()
            for item in mistakes:
                Label(result_window, text=f"Q: {item['question']}\nYour Ans: {item['your']} | Correct: {item['correct']}", wraplength=400, fg="red").pack()

    Button(result_window, text="Close", command=result_window.quit).pack(pady=10)
    result_window.mainloop()

# ---------- Start Screen ----------
root = Tk()
root.title("Multi-User Quiz")
root.config(padx=20, pady=20)

Label(root, text="How many users want to play?").pack()
user_count_entry = Entry(root, width=30)
user_count_entry.pack()

Button(root, text="Next", command=collect_names).pack(pady=10)
root.mainloop()
