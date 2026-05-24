import csv
import glob
import random
import customtkinter as ctk

voca = []
files = glob.glob("vocabulary/*.tsv")

current_index = 0
show_answer = False
waiting_for_next = False
checkbox_vars = []

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("900x700")
app.title("중국어 학습기")

selection_label = ctk.CTkLabel(
    app,
    text="학습할 파일 선택",
    font=("Arial", 28)
)
selection_label.pack(pady=(20, 10))

checkbox_frame = ctk.CTkFrame(app)
checkbox_frame.pack(pady=10)

for file_name in files:
    var = ctk.BooleanVar(value=True)

    checkbox = ctk.CTkCheckBox(
        checkbox_frame,
        text=file_name.replace("vocabulary/", ""),
        variable=var,
        font=("Arial", 18)
    )
    checkbox.pack(anchor="w", padx=20, pady=5)

    checkbox_vars.append((file_name, var))


def load_selected_files():
    global voca

    voca = []

    for file_name, var in checkbox_vars:
        if var.get():
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter="\t")
                next(reader)

                for row in reader:
                    hanzi = row[0]
                    pinyin = row[1]
                    meaning = row[2]

                    voca.append([hanzi, pinyin, meaning])

    random.shuffle(voca)

hanzi_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 64)
)
hanzi_label.pack(pady=(40, 20))

answer_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 28)
)
answer_label.pack(pady=20)


def load_problem():
    word = voca[current_index]

    hanzi_label.configure(text=word[0])

    if show_answer:
        answer_label.configure(text=f"{word[1]}\n{word[2]}")
    else:
        answer_label.configure(text="")



def next_problem():
    global current_index
    global show_answer
    global waiting_for_next

    if len(voca) == 0:
        load_selected_files()

        if len(voca) == 0:
            answer_label.configure(text="파일을 하나 이상 선택하세요")
            return

        current_index = 0
        show_answer = False
        waiting_for_next = False
        load_problem()
        return

    if not waiting_for_next:
        show_answer = True
        waiting_for_next = True
        load_problem()
        return

    current_index += 1

    if current_index >= len(voca):
        random.shuffle(voca)
        current_index = 0

    show_answer = False
    waiting_for_next = False
    load_problem()


def on_enter(event):
    next_problem()

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=40)

next_button = ctk.CTkButton(
    button_frame,
    text="엔터 / 다음",
    command=next_problem,
    width=160,
    height=50,
    font=("Arial", 20)
)
next_button.pack(side="left", padx=20)

app.bind("<Return>", on_enter)

hanzi_label.configure(text="엔터를 눌러 시작")

app.mainloop()
    