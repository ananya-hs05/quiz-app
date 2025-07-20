
from tkinter import *
from quiz_brain import QuizBrain
import random

THEME_COLOR = "#D7D1D1" \
""

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain, username="User", on_quiz_end=None):
        self.quiz = quiz_brain
        self.username = username
        self.on_quiz_end = on_quiz_end
        self.timer_job = None

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Colorful header
        self.header_label = Label(
            text="🎯 Welcome to the Quizzler Game 🎯",
            font=("Helvetica", 20, "bold"),
            fg="#ff9861",
            bg=THEME_COLOR
        )
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.is_dark = True
        self.theme_button = Button(text="Switch Theme", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0)

        self.score_label = Label(text=f"{self.username}'s Score: 0", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=1, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Some Question Text",
            fill=THEME_COLOR,
            font=("Arial", 20, "italic")
        )
        self.timer_text = self.canvas.create_text(150, 20, text="", fill=THEME_COLOR, font=("Arial", 12, "bold"))
        self.canvas.grid(row=2, column=0, columnspan=2, pady=50)

        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.image = true_image
        self.true_button.grid(row=3, column=0)

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.image = false_image
        self.false_button.grid(row=3, column=1)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"{self.username}'s Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)

            # 🎨 Random color text
            colors = ["#fdffb6", "#0e100e", "#9bf6ff", "#a0c4ff", "#ffc6ff"]
            random_color = random.choice(colors)
            self.canvas.itemconfig(self.question_text, fill=random_color)
            self.canvas.itemconfig(self.timer_text, fill=random_color)

            self.remaining_time = 10
            self.update_timer()
        else:
            self.canvas.itemconfig(self.question_text, text="🎉 You've reached the end of the quiz! 🎉")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

            if self.timer_job:
                self.window.after_cancel(self.timer_job)
                self.timer_job = None

            if self.on_quiz_end:
                self.window.after(1500, lambda: [self.window.destroy(), self.on_quiz_end(self.quiz.score, self.quiz.incorrect_questions)])

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
            self.timer_job = None

        # 🎨 Pastel feedback colors
        if is_right:
            self.canvas.config(bg="#111010")  # pastel green
        else:
            self.canvas.config(bg="#ed1616")  # pastel red

        self.window.after(1000, self.get_next_question)

    def update_timer(self):
        self.canvas.itemconfig(self.timer_text, text=f"Time Left: {self.remaining_time}s")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_job = self.window.after(1000, self.update_timer)
        else:
            self.timer_job = None
            self.give_feedback(False)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        new_color = "#375362" if self.is_dark else "#aedaf5"
        text_color = "white" if self.is_dark else "black"
        self.window.config(bg=new_color)
        self.header_label.config(bg=new_color, fg="#ff6f61")
        self.score_label.config(bg=new_color, fg=text_color)
        self.canvas.config(bg="white")
        self.canvas.itemconfig(self.question_text, fill=new_color)
        self.canvas.itemconfig(self.timer_text, fill=new_color)
        self.theme_button.config(bg=new_color, fg=text_color)
