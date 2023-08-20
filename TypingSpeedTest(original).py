import tkinter as tk
from tkinter import ttk
import time
import random
from nltk.corpus import words
from nltk.probability import FreqDist

root = tk.Tk()
root.title('Typing Speed Test')
root.config(bg='lavender')

words_per_minute = tk.StringVar()
accuracy = tk.StringVar()
time_left = tk.StringVar(value="60")

word_dist = FreqDist(words.words())
common_words = [w[0] for w in word_dist.most_common(500)]

typed_words = []
random_words = []
start_time = None

def update_wpm():
    if typed_words:
        wpm = len(typed_words) / ((time.time() - start_time)/60)
        words_per_minute.set(str(round(wpm)))

def update_accuracy():
    if typed_words:
        errors = sum(typed_word != random_word for typed_word, random_word in zip(typed_words, random_words))
        accuracy_value = ((len(typed_words) - errors) / len(typed_words)) * 100
        accuracy.set(str(round(accuracy_value, 2)))

def start_test():
    global random_words, typed_words, start_time
    
    random_words = random.sample(common_words, 50)
    typed_words.clear()
    
    text_widget.delete('1.0', tk.END)
    text_widget.insert('1.0', ' '.join(random_words))
    
    start_time = time.time()

def key_press(event):
    global typed_words
    
    typed_word = entry.get()
    typed_words.append(typed_word)
    
    if typed_word != random_words[len(typed_words)-1]:
        entry.config(fg='red')
    else:
        entry.config(fg='black')
        
    entry.delete(0, tk.END)
    
    update_wpm()
    update_accuracy()

def countdown(time_left):
    if time_left > 0:
        root.after(1000, countdown, time_left-1)
        time_left.set(str(time_left))
    else:
        show_results()

def show_results():
    result_string = f"Words per minute: {words_per_minute.get()}, Accuracy: {accuracy.get()}%"
    result_label.config(text=result_string)
    result_label.config(font=('TkDefaultFont', 14))

instructions = ttk.Label(root, text='Type the words below as fast and accurately as you can. Press enter to start.', font=('TkDefaultFont', 14))
instructions.pack(pady=(20, 0))

text_widget = tk.Text(root, height=10, font=('TkDefaultFont', 14))
text_widget.pack()

entry = ttk.Entry(root, width=40, font=('TkDefaultFont 14'))
entry.pack()
entry.focus_set()

wpm_label = ttk.Label(root, text='Words per minute:', font=('TkDefaultFont', 14))
wpm_label.pack()

wpm_value = ttk.Label(root, textvariable=words_per_minute, font=('TkDefaultFont', 24))
wpm_value.pack()

accuracy_label = ttk.Label(root, text='Accuracy:', font=('TkDefaultFont', 14))
accuracy_label.pack()

accuracy_value = ttk.Label(root, textvariable=accuracy, font=('TkDefaultFont', 24))
accuracy_value.pack(pady=(0, 20))

start_button = ttk.Button(root, text='Start Test', command=lambda: [start_test(), countdown(60)])
start_button.pack()

result_label = ttk.Label(root, text='', font=('TkDefaultFont', 24))
result_label.pack(pady=(20, 0))

root.bind('<Return>', key_press)

root.mainloop()