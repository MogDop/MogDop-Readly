import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import subprocess
import platform
import winsound
import requests
from bs4 import BeautifulSoup
import threading
import webbrowser
from PIL import Image, ImageDraw, ImageTk

# Инициализация окна
root = tk.Tk()
script_dir = os.path.dirname(os.path.abspath(__file__))
root.iconbitmap(os.path.join(script_dir, "ava.ico"))
root.title("Ридли")
root.state('zoomed')

# Глобальные переменные
original_text = ""
stage = 1
case_sensitive = True
punctuation_sensitive = True
delay_time = 6
font_size = 18
auto_clear = True
bg_color = "#F5F5F4"
text_bg_color = "#FFFFFF"
button_color = "#D9E7F4"
text_color = "#333333"
theme = "Светлая"
language = "Русский"
current_profile = "save1"
error_count = 0  # Счётчик ошибок в сессии

lines = []
current_line = 0
line_stage = 1
quatrains = []
current_quatrain = 0

# Глобальные переменные для математического тренажёра
math_level = 1
math_points = 0.0
math_tasks_completed = 0
math_difficulty = "Нормальный"
math_current_task = None
math_current_answer = None
math_operations = ["+", "-", "*", "/"]
math_difficulty_ranges = {
    "Лёгкий": [1, 20],
    "Нормальный": [1, 100],
    "Сложный": [1, 1000]
}
math_tasks_per_level = 10

theme_var = tk.StringVar(value="Светлая")
language_var = tk.StringVar(value="Русский")
case_var = tk.BooleanVar(value=True)
punct_var = tk.BooleanVar(value=True)
auto_clear_var = tk.BooleanVar(value=True)
profile_var = tk.StringVar(value="save1")
math_difficulty_var = tk.StringVar(value="Нормальный")
math_add_var = tk.BooleanVar(value=True)
math_subtract_var = tk.BooleanVar(value=True)
math_multiply_var = tk.BooleanVar(value=True)
math_divide_var = tk.BooleanVar(value=True)

themes = {
    "Светлая": {"bg_color": "#F5F5F4", "text_bg_color": "#FFFFFF", "button_color": "#D9E7F4", "text_color": "#333333"},
    "Тёмная": {"bg_color": "#2F2F2F", "text_bg_color": "#3C3C3C", "button_color": "#4A6A8A", "text_color": "#E0E0E0"},
    "Ретро": {"bg_color": "#1A2A1A", "text_bg_color": "#000000", "button_color": "#3A5A3A", "text_color": "#00FF00"}
}

translations = {
    "Русский": {
        # Исходные ключи
        "title": "Ридли",
        "tab_main": "Полностью",
        "tab_lines": "По строкам",
        "tab_paragraphs": "По абзацам",
        "tab_settings": "Параметры",
        "check": "Проверить",
        "reset": "Начать заново",
        "correct": "Правильно!",
        "error": "Ошибка!",
        "success": "Успех!",
        "check_memory": "Проверить память",
        "case_sensitive": "Учитывать размер букв",
        "punct_sensitive": "Учитывать знаки препинания",
        "auto_clear": "Автоматически очищать поле",
        "font_size": "Размер шрифта текста:",
        "theme": "Тема оформления:",
        "language": "Язык:",
        "open_folder": "Открыть папку",
        "explore_poems": "Исследовать стихи...",
        "status_main": "Спиши текст в поле выше",
        "status_main_memory": "Введи текст по памяти",
        "status_main_error": "Нет, неправильно. Попробуй ещё",
        "status_main_done": "Правильно! Можешь начать заново",
        "status_lines": "Строка {0} из {1}: Спиши строку",
        "status_lines_memory": "Строка {0} из {1}: Введи по памяти",
        "status_lines_error": "Строка {0} из {1}: Ошибка! Спиши заново",
        "status_lines_done": "Все строки пройдены!",
        "status_para": "Абзац {0} из {1}",
        "status_para_error": "Ошибка! Попробуй ещё раз",
        "status_para_done": "Все абзацы пройдены!",
        "profile": "Профиль:",
        "create_profile": "Создать профиль",
        "profile_name": "Имя профиля:",
        "profile_password": "Пароль (опционально):",
        "enter_password": "Введите пароль:",
        "errors": "Ошибок: {0}",
        "add_to_stih": "Добавить в stih.txt",
        "go_to_stihi": "Перейти на stihi.ru",
        "back": "Назад",
        "retry": "Повторить",
        "failed_to_load": "Не удалось загрузить стихи. Проверьте соединение.",
        "loading_poems": "Подождите, идет загрузка стихов",
        "author": "Автор",
        "date": "Дата",
        "poem_added": "Стих добавлен в stih.txt",
        "MD": "Автор: Глеб Лазарев, @MogDop или @mogdop9",
        "back_to_menu": "Назад в меню",
        "help": "Помощь",
        # Математический тренажёр
        "poems": "Стихи",
        "mathematics": "Математика",
        "math_mode": "Математический тренажёр",
        "math_level": "Уровень: {0}",
        "math_points": "Очки: {0:.1f}",
        "math_progress": "Прогресс: {0}/{1} заданий",
        "math_task": "Задание:",
        "math_check": "Проверить",
        "math_new_task": "Новое задание",
        "math_easy": "Лёгкий",
        "math_normal": "Нормальный",
        "math_hard": "Сложный",
        "math_difficulty": "Сложность:",
        "math_correct": "Правильно! +{0:.1f} очков",
        "math_incorrect": "Неправильно! Правильный ответ: {0}",
        "math_level_up": "Поздравляем! Вы достигли уровня {0}!",
        "math_operations": "Операции:",
        "math_settings": "Настройки математики",
        "math_add": "Сложение (+)",
        "math_subtract": "Вычитание (-)",
        "math_multiply": "Умножение (×)",
        "math_divide": "Деление (÷)",
        "math_range_easy": "Диапазон для лёгкого:",
        "math_range_normal": "Диапазон для нормального:",
        "math_range_hard": "Диапазон для сложного:",
        "math_tasks_per_level": "Заданий для повышения уровня:",
        "general_settings": "Общие настройки",
        "poems_settings": "Настройки стихов",
        "math_settings_title": "Настройки математики",
        "help_title": "Справка по программе Ридли",
        "help_text": """Ридли - это программа для тренировки памяти и навыков письма.

ОСНОВНЫЕ РЕЖИМЫ:

1. ГЛАВНАЯ - Основной режим работы:
   • Сначала вы видите текст, который нужно переписать
   • После правильного ввода текст скрывается
   • Затем нужно ввести текст по памяти
   • Программа проверяет правильность ввода

2. ПО СТРОКАМ - Режим обучения построчно:
   • Текст разбивается на отдельные строки
   • Вы переписываете каждую строку
   • После правильного ввода строка скрывается
   • Затем нужно ввести строку по памяти
   • После прохождения всех строк режим завершается

3. ПО АБЗАЦАМ - Режим обучения по абзацам:
   • Текст разбивается на абзацы (блоки)
   • Вы переписываете каждый абзац
   • После правильного ввода переходите к следующему
   • После прохождения всех абзацев режим завершается

ПАРАМЕТРЫ:

• Учитывать размер букв - проверка учитывает регистр (заглавные/строчные)
• Учитывать знаки препинания - проверка учитывает пунктуацию
• Автоматически очищать поле - поле ввода очищается после ошибки
• Размер шрифта - настройка размера текста
• Тема оформления - выбор цветовой схемы (Светлая, Тёмная, Ретро)
• Язык - переключение между русским и английским

ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:

• Открыть папку - открывает папку с программой
• Исследовать стихи - загружает стихи с сайта stihi.ru
• Счётчик ошибок - показывает количество ошибок в текущей сессии

ТЕКСТ ДЛЯ ТРЕНИРОВКИ:

Программа автоматически загружает текст из файла stih.txt в папке программы.
Вы можете редактировать этот файл или использовать функцию "Исследовать стихи"
для загрузки новых стихов с сайта stihi.ru.

УДАЧИ В ТРЕНИРОВКЕ!"""
    },
    "English": {
        # Исходные ключи
        "title": "Readly",
        "tab_main": "Main",
        "tab_lines": "By Lines",
        "tab_paragraphs": "By Paragraphs",
        "tab_settings": "Settings",
        "check": "Check",
        "reset": "Start Over",
        "correct": "Correct!",
        "error": "Error!",
        "success": "Success!",
        "check_memory": "Check Memory",
        "case_sensitive": "Case Sensitive",
        "punct_sensitive": "Punctuation Sensitive",
        "auto_clear": "Auto Clear Field",
        "font_size": "Text Font Size:",
        "theme": "Theme:",
        "language": "Language:",
        "open_folder": "Open Folder",
        "explore_poems": "Explore Poems...",
        "status_main": "Write the text in the field above",
        "status_main_memory": "Enter the text from memory",
        "status_main_error": "No, incorrect. Try again",
        "status_main_done": "Correct! You can start over",
        "status_lines": "Line {0} of {1}: Copy the line",
        "status_lines_memory": "Line {0} of {1}: Enter from memory",
        "status_lines_error": "Line {0} of {1}: Error! Copy again",
        "status_lines_done": "All lines completed!",
        "status_para": "Paragraph {0} of {1}",
        "status_para_error": "Error! Try again",
        "status_para_done": "All paragraphs completed!",
        "profile": "Profile:",
        "create_profile": "Create Profile",
        "profile_name": "Profile Name:",
        "profile_password": "Password (optional):",
        "enter_password": "Enter Password:",
        "errors": "Errors: {0}",
        # Новые ключи для open_poem_selector
        "add_to_stih": "Add to stih.txt",
        "go_to_stihi": "Go to stihi.ru",
        "back": "Back",
        "retry": "Retry",
        "failed_to_load": "Failed to load poems. Check your connection.",
        "loading_poems": "Wait, poems are loading",
        "author": "Author",
        "date": "Date",
        "poem_added": "Poem added to stih.txt",
        "MD": "Author: Gleb Lazarev, @MogDop or @mogdop9",
        "back_to_menu": "Back to Menu",
        "help": "Help",
        # Math trainer
        "poems": "Poems",
        "mathematics": "Mathematics",
        "math_mode": "Math Trainer",
        "math_level": "Level: {0}",
        "math_points": "Points: {0:.1f}",
        "math_progress": "Progress: {0}/{1} tasks",
        "math_task": "Task:",
        "math_check": "Check",
        "math_new_task": "New Task",
        "math_easy": "Easy",
        "math_normal": "Normal",
        "math_hard": "Hard",
        "math_difficulty": "Difficulty:",
        "math_correct": "Correct! +{0:.1f} points",
        "math_incorrect": "Incorrect! Correct answer: {0}",
        "math_level_up": "Congratulations! You reached level {0}!",
        "math_operations": "Operations:",
        "math_settings": "Math Settings",
        "math_add": "Addition (+)",
        "math_subtract": "Subtraction (-)",
        "math_multiply": "Multiplication (×)",
        "math_divide": "Division (÷)",
        "math_range_easy": "Range for easy:",
        "math_range_normal": "Range for normal:",
        "math_range_hard": "Range for hard:",
        "math_tasks_per_level": "Tasks per level:",
        "general_settings": "General Settings",
        "poems_settings": "Poems Settings",
        "math_settings_title": "Math Settings",
        "help_title": "Readly Program Help",
        "help_text": """Readly is a program for training memory and writing skills.

MAIN MODES:

1. MAIN - Main working mode:
   • First you see the text that needs to be copied
   • After correct input, the text is hidden
   • Then you need to enter the text from memory
   • The program checks the correctness of input

2. BY LINES - Line-by-line learning mode:
   • Text is split into individual lines
   • You copy each line
   • After correct input, the line is hidden
   • Then you need to enter the line from memory
   • After completing all lines, the mode ends

3. BY PARAGRAPHS - Paragraph-by-paragraph learning mode:
   • Text is split into paragraphs (blocks)
   • You copy each paragraph
   • After correct input, move to the next one
   • After completing all paragraphs, the mode ends

SETTINGS:

• Case Sensitive - check considers case (uppercase/lowercase)
• Punctuation Sensitive - check considers punctuation
• Auto Clear Field - input field clears after error
• Text Font Size - text size setting
• Theme - color scheme selection (Light, Dark, Retro)
• Language - switch between Russian and English

ADDITIONAL FEATURES:

• Open Folder - opens the program folder
• Explore Poems - loads poems from stihi.ru website
• Error Counter - shows the number of errors in current session

TRAINING TEXT:

The program automatically loads text from stih.txt file in the program folder.
You can edit this file or use the "Explore Poems" function
to load new poems from stihi.ru website.

GOOD LUCK WITH TRAINING!"""
    }
}

# Параметры кнопок
button_width, button_height = 200, 60
reset_button_width = 300
settings_button_width = 400  # Увеличенная ширина для кнопок в настройках
button_radius = 20

def create_rounded_button_image(width, height, radius, bg_color, fill_bg=bg_color):
    image = Image.new("RGBA", (width, height), fill_bg)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([0, 0, width-1, height-1], radius=radius, fill=bg_color)
    return ImageTk.PhotoImage(image)

def update_button_color(button, color):
    width = reset_button_width if button in [reset_button, line_reset_button, quatrain_reset_button] else settings_button_width if button in [open_folder_button, poem_selector_button] else button_width
    new_img = create_rounded_button_image(width, button_height, button_radius, color, bg_color)
    button.config(image=new_img)
    button.image = new_img

def load_text_from_file():
    global original_text, lines, current_line, line_stage, quatrains, current_quatrain
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = None
        supported_extensions = ['.txt', '.md', '.text']
        for ext in supported_extensions:
            potential_path = os.path.join(script_dir, f"stih{ext}")
            if os.path.exists(potential_path):
                file_path = potential_path
                break
        
        if not file_path:
            raise FileNotFoundError("Файл stih с поддерживаемым расширением не найден")

        with open(file_path, "r", encoding="utf-8") as file:
            original_text = file.read().strip()
        
        lines = [line.strip() for line in original_text.split('\n') if line.strip()]
        current_line = 0
        line_stage = 1

        if "\n\n" in original_text:
            quatrains = [block.strip() for block in original_text.split("\n\n") if block.strip()]
        else:
            temp_lines = original_text.split('\n')
            quatrains = ['\n'.join(temp_lines[i:i+4]) for i in range(0, len(temp_lines), 4)]
        current_quatrain = 0

        sample_text.config(state="normal")
        sample_text.delete("1.0", tk.END)
        sample_text.insert(tk.END, original_text)
        sample_text.config(state="disabled")
        
        if lines:
            line_sample_text.config(state="normal")
            line_sample_text.delete("1.0", tk.END)
            line_sample_text.insert(tk.END, lines[current_line])
            line_sample_text.config(state="disabled")
            line_status_label.config(text=translations[language]["status_lines"].format(current_line + 1, len(lines)))
        else:
            line_sample_text.config(state="normal")
            line_sample_text.delete("1.0", tk.END)
            line_sample_text.insert(tk.END, "Text is empty" if language == "English" else "Текст пуст")
            line_sample_text.config(state="disabled")
        
        if quatrains:
            quatrain_sample_text.config(state="normal")
            quatrain_sample_text.delete("1.0", tk.END)
            quatrain_sample_text.insert(tk.END, quatrains[current_quatrain])
            quatrain_sample_text.config(state="disabled")
            quatrain_status_label.config(text=translations[language]["status_para"].format(current_quatrain + 1, len(quatrains)))
        else:
            quatrain_sample_text.config(state="normal")


            quatrain_sample_text.delete("1.0", tk.END)
            quatrain_sample_text.insert(tk.END, "Text is empty" if language == "English" else "Текст пуст")
            quatrain_sample_text.config(state="disabled")
        
        status_label.config(text=translations[language]["status_main"])
    except Exception as e:
        messagebox.showerror("Error" if language == "English" else "Ошибка", f"Failed to load file: {e}")
        original_text = ""
        lines = []
        quatrains = []

def play_sound():
    try:
        winsound.Beep(37, 100)
        winsound.PlaySound("click.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
    except Exception:
        pass

def play_sound1():
    global error_count
    error_count += 1  # Увеличиваем счётчик ошибок
    update_error_label()
    try:
        winsound.Beep(37, 100)
        winsound.PlaySound("click1.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
    except Exception:
        pass

def play_click_sound():
    try:
        winsound.PlaySound("click2.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
    except Exception:
        pass

def check_input():
    global stage
    try:
        if not original_text or original_text.strip() == "":
            messagebox.showwarning("Warning" if language == "English" else "Предупреждение", 
                                 "No text loaded. Please load a text file first." if language == "English" 
                                 else "Текст не загружен. Пожалуйста, сначала загрузите текстовый файл.")
            return
        
        user_input = text_widget.get("1.0", tk.END).strip()
        text_to_compare = original_text.strip()

        if not case_sensitive:
            user_input = user_input.lower()
            text_to_compare = text_to_compare.lower()
        if not punctuation_sensitive:
            for punct in ".,!?;:-—\"'()[]{}":
                user_input = user_input.replace(punct, "")
                text_to_compare = text_to_compare.replace(punct, "")

        if user_input == text_to_compare:
            play_sound()
            if stage == 1:
                update_button_color(check_button, "green")
                check_button.config(text=translations[language]["correct"])
                root.after(delay_time * 1000, proceed_to_stage_2)
            elif stage == 2:
                update_button_color(check_button, "green")
                check_button.config(text=translations[language]["success"])
                root.after(delay_time * 1000, finish_task)
        else:
            play_sound1()
            update_button_color(check_button, "red")
            check_button.config(text=translations[language]["error"])
            root.after(delay_time * 1000, reset_after_error)
    except Exception as e:
        messagebox.showerror("Error" if language == "English" else "Ошибка", 
                           f"An error occurred: {e}" if language == "English" else f"Произошла ошибка: {e}")

def proceed_to_stage_2():
    global stage
    stage = 2
    sample_text.config(state="normal")
    sample_text.delete("1.0", tk.END)
    sample_text.config(state="disabled")
    text_widget.delete("1.0", tk.END)
    status_label.config(text=translations[language]["status_main_memory"])
    update_button_color(check_button, button_color)
    check_button.config(text=translations[language]["check_memory"])

def finish_task():
    status_label.config(text=translations[language]["status_main_done"])
    text_widget.delete("1.0", tk.END)
    check_button.config(state=tk.DISABLED, text=translations[language]["check"])
    reset_button.config(state=tk.NORMAL)
    update_button_color(check_button, button_color)

def reset_after_error():
    global stage
    if stage == 1:
        status_label.config(text=translations[language]["status_main_error"])
        if auto_clear:
            text_widget.delete("1.0", tk.END)
    elif stage == 2:
        stage = 1
        sample_text.config(state="normal")
        sample_text.delete("1.0", tk.END)
        sample_text.insert(tk.END, original_text)
        sample_text.config(state="disabled")
        text_widget.delete("1.0", tk.END)
        status_label.config(text=translations[language]["status_main"])
    update_button_color(check_button, button_color)
    check_button.config(text=translations[language]["check"])

def reset():
    global stage, error_count
    stage = 1
    error_count = 0  # Сбрасываем счётчик ошибок
    update_error_label()
    sample_text.config(state="normal")
    sample_text.delete("1.0", tk.END)
    sample_text.insert(tk.END, original_text)
    sample_text.config(state="disabled")
    text_widget.delete("1.0", tk.END)
    status_label.config(text=translations[language]["status_main"])
    check_button.config(state=tk.NORMAL, text=translations[language]["check"])
    reset_button.config(state=tk.DISABLED)
    update_button_color(check_button, button_color)



def check_line():
    global current_line, line_stage
    user_input = line_text_widget.get("1.0", tk.END).strip()
    text_to_compare = lines[current_line].strip()

    if not case_sensitive:
        user_input = user_input.lower()
        text_to_compare = text_to_compare.lower()
    if not punctuation_sensitive:
        for punct in ".,!?;:-—\"'()[]{}":
            user_input = user_input.replace(punct, "")
            text_to_compare = text_to_compare.replace(punct, "")

    if user_input == text_to_compare:
        play_sound()
        update_button_color(line_check_button, "green")
        line_check_button.config(text=translations[language]["correct"])
        if line_stage == 1:
            root.after(delay_time * 1000, proceed_to_memory_stage)
        elif line_stage == 2:
            root.after(delay_time * 1000, next_line)
    else:
        play_sound1()
        update_button_color(line_check_button, "red")
        line_check_button.config(text=translations[language]["error"])
        root.after(delay_time * 1000, reset_line_error)

def proceed_to_memory_stage():
    global line_stage
    line_stage = 2
    line_sample_text.config(state="normal")
    line_sample_text.delete("1.0", tk.END)
    line_sample_text.config(state="disabled")
    line_text_widget.delete("1.0", tk.END)
    line_status_label.config(text=translations[language]["status_lines_memory"].format(current_line + 1, len(lines)))
    update_button_color(line_check_button, button_color)
    line_check_button.config(text=translations[language]["check_memory"])

def next_line():
    global current_line, line_stage
    current_line += 1
    line_stage = 1
    if current_line < len(lines):
        line_sample_text.config(state="normal")
        line_sample_text.delete("1.0", tk.END)
        line_sample_text.insert(tk.END, lines[current_line])
        line_sample_text.config(state="disabled")
        line_text_widget.delete("1.0", tk.END)
        line_status_label.config(text=translations[language]["status_lines"].format(current_line + 1, len(lines)))
        update_button_color(line_check_button, button_color)
        line_check_button.config(text=translations[language]["check"])
    else:
        line_status_label.config(text=translations[language]["status_lines_done"])
        line_check_button.config(state=tk.DISABLED, text=translations[language]["check"])
        line_reset_button.config(state=tk.NORMAL)

def reset_line_error():
    global line_stage
    if line_stage == 1:
        line_status_label.config(text=translations[language]["status_lines_error"].format(current_line + 1, len(lines)))
    elif line_stage == 2:
        line_stage = 1
        line_sample_text.config(state="normal")
        line_sample_text.delete("1.0", tk.END)
        line_sample_text.insert(tk.END, lines[current_line])
        line_sample_text.config(state="disabled")
        line_status_label.config(text=translations[language]["status_lines_error"].format(current_line + 1, len(lines)))
    if auto_clear:
        line_text_widget.delete("1.0", tk.END)
    update_button_color(line_check_button, button_color)
    line_check_button.config(text=translations[language]["check"])

def reset_lines():
    global current_line, line_stage, error_count
    current_line = 0
    line_stage = 1
    error_count = 0  # Сбрасываем счётчик ошибок
    update_error_label()
    if lines:
        line_sample_text.config(state="normal")
        line_sample_text.delete("1.0", tk.END)
        line_sample_text.insert(tk.END, lines[current_line])
        line_sample_text.config(state="disabled")
    line_text_widget.delete("1.0", tk.END)
    line_status_label.config(text=translations[language]["status_lines"].format(1, len(lines)))
    line_check_button.config(state=tk.NORMAL, text=translations[language]["check"])
    line_reset_button.config(state=tk.DISABLED)
    update_button_color(line_check_button, button_color)

def check_quatrain():

    global current_quatrain
    user_input = quatrain_text_widget.get("1.0", tk.END).strip()
    text_to_compare = quatrains[current_quatrain].strip()

    if not case_sensitive:
        user_input = user_input.lower()
        text_to_compare = text_to_compare.lower()
    if not punctuation_sensitive:
        for punct in ".,!?;:-—\"'()[]{}":
            user_input = user_input.replace(punct, "")
            text_to_compare = text_to_compare.replace(punct, "")

    if user_input == text_to_compare:
        play_sound()
        update_button_color(quatrain_check_button, "green")
        quatrain_check_button.config(text=translations[language]["correct"])
        root.after(delay_time * 1000, next_quatrain)
    else:
        play_sound1()
        update_button_color(quatrain_check_button, "red")
        quatrain_check_button.config(text=translations[language]["error"])
        root.after(delay_time * 1000, reset_quatrain_error)

def next_quatrain():
    global current_quatrain
    current_quatrain += 1
    if current_quatrain < len(quatrains):
        quatrain_sample_text.config(state="normal")
        quatrain_sample_text.delete("1.0", tk.END)
        quatrain_sample_text.insert(tk.END, quatrains[current_quatrain])
        quatrain_sample_text.config(state="disabled")
        quatrain_text_widget.delete("1.0", tk.END)
        quatrain_status_label.config(text=translations[language]["status_para"].format(current_quatrain + 1, len(quatrains)))
        update_button_color(quatrain_check_button, button_color)
        quatrain_check_button.config(text=translations[language]["check"])
    else:
        quatrain_status_label.config(text=translations[language]["status_para_done"])
        quatrain_check_button.config(state=tk.DISABLED, text=translations[language]["check"])
        quatrain_reset_button.config(state=tk.NORMAL)

def reset_quatrain_error():
    quatrain_status_label.config(text=translations[language]["status_para_error"])
    if auto_clear:
        quatrain_text_widget.delete("1.0", tk.END)
    update_button_color(quatrain_check_button, button_color)
    quatrain_check_button.config(text=translations[language]["check"])

def reset_quatrains():
    global current_quatrain, error_count
    current_quatrain = 0
    error_count = 0  # Сбрасываем счётчик ошибок
    update_error_label()
    if quatrains:
        quatrain_sample_text.config(state="normal")
        quatrain_sample_text.delete("1.0", tk.END)
        quatrain_sample_text.insert(tk.END, quatrains[current_quatrain])
        quatrain_sample_text.config(state="disabled")
    quatrain_text_widget.delete("1.0", tk.END)
    quatrain_status_label.config(text=translations[language]["status_para"].format(1, len(quatrains)))
    quatrain_check_button.config(state=tk.NORMAL, text=translations[language]["check"])
    quatrain_reset_button.config(state=tk.DISABLED)
    update_button_color(quatrain_check_button, button_color)

# Функции математического тренажёра
import random

def generate_math_task():
    """Генерирует случайное математическое задание"""
    global math_current_task, math_current_answer, math_operations, math_difficulty, math_difficulty_ranges
    
    # Получаем доступные операции из настроек
    available_ops = [op for op in math_operations if op in ["+", "-", "*", "/"]]
    if not available_ops:
        available_ops = ["+"]  # По умолчанию сложение
    
    # Выбираем случайную операцию
    operation = random.choice(available_ops)
    
    # Получаем диапазон для текущей сложности
    min_val, max_val = math_difficulty_ranges.get(math_difficulty, [1, 100])
    
    # Генерируем числа
    num1 = random.randint(min_val, max_val)
    num2 = random.randint(min_val, max_val)
    
    # Для вычитания и деления убеждаемся, что результат положительный
    if operation == "-":
        if num1 < num2:
            num1, num2 = num2, num1
    elif operation == "/":
        # Для деления делаем так, чтобы результат был целым
        num2 = random.randint(1, min(20, max_val // 2))
        num1 = num2 * random.randint(1, min(20, max_val // num2))
    
    # Вычисляем правильный ответ
    if operation == "+":
        answer = num1 + num2
        op_symbol = "+"
    elif operation == "-":
        answer = num1 - num2
        op_symbol = "-"
    elif operation == "*":
        answer = num1 * num2
        op_symbol = "×"
    elif operation == "/":
        answer = num1 // num2
        op_symbol = "÷"
    
    math_current_task = f"{num1} {op_symbol} {num2} = ?"
    math_current_answer = answer
    
    return math_current_task, math_current_answer

def check_math_answer():
    """Проверяет ответ пользователя"""
    global math_level, math_points, math_tasks_completed, math_difficulty, math_tasks_per_level
    
    try:
        user_answer = int(math_answer_entry.get().strip())
        
        if user_answer == math_current_answer:
            # Правильный ответ
            play_sound()
            
            # Начисляем очки в зависимости от сложности
            points_earned = 0.1 if math_difficulty == "Лёгкий" else (0.3 if math_difficulty == "Нормальный" else 0.5)
            math_points += points_earned
            math_tasks_completed += 1
            
            # Обновляем интерфейс
            update_math_progress_display()
            update_button_color(math_check_button, "green")
            math_status_label.config(text=translations[language]["math_correct"].format(points_earned))
            
            # Проверяем повышение уровня
            if math_tasks_completed >= math_tasks_per_level:
                math_level += 1
                math_tasks_completed = 0
                messagebox.showinfo(translations[language]["success"], 
                                  translations[language]["math_level_up"].format(math_level))
                update_math_progress_display()
            
            # Сохраняем прогресс
            save_settings()
            
            # Очищаем поле и генерируем новое задание через задержку
            root.after(delay_time * 1000, lambda: (math_answer_entry.delete(0, tk.END), 
                                                   generate_new_math_task(), 
                                                   update_button_color(math_check_button, button_color),
                                                   math_status_label.config(text="")))
        else:
            # Неправильный ответ
            play_sound1()
            update_button_color(math_check_button, "red")
            math_status_label.config(text=translations[language]["math_incorrect"].format(math_current_answer))
            root.after(delay_time * 1000, lambda: (update_button_color(math_check_button, button_color),
                                                  math_status_label.config(text="")))
    except ValueError:
        messagebox.showwarning("Warning" if language == "English" else "Предупреждение",
                             "Please enter a valid number" if language == "English" else "Пожалуйста, введите число")

def generate_new_math_task():
    """Генерирует новое задание и обновляет интерфейс"""
    task, answer = generate_math_task()
    math_task_label.config(text=f"{translations[language]['math_task']} {task}")

def update_math_progress_display():
    """Обновляет отображение прогресса"""
    math_level_label.config(text=translations[language]["math_level"].format(math_level))
    math_points_label.config(text=translations[language]["math_points"].format(math_points))
    math_progress_label.config(text=translations[language]["math_progress"].format(math_tasks_completed, math_tasks_per_level))

def update_math_difficulty():
    """Обновляет сложность математического тренажёра"""
    global math_difficulty
    math_difficulty = math_difficulty_var.get()
    generate_new_math_task()

def update_math_operations():
    """Обновляет список доступных операций"""
    global math_operations
    math_operations = []
    if math_add_var.get():
        math_operations.append("+")
    if math_subtract_var.get():
        math_operations.append("-")
    if math_multiply_var.get():
        math_operations.append("*")
    if math_divide_var.get():
        math_operations.append("/")
    # Если ни одна операция не выбрана, добавляем сложение по умолчанию
    if not math_operations:
        math_operations = ["+"]
        math_add_var.set(True)

def update_math_tasks_per_level():
    """Обновляет количество заданий для повышения уровня"""
    global math_tasks_per_level
    try:
        math_tasks_per_level = int(math_tasks_per_level_entry.get())
        if math_tasks_per_level < 1:
            math_tasks_per_level = 10
            math_tasks_per_level_entry.delete(0, tk.END)
            math_tasks_per_level_entry.insert(0, "10")
        if 'math_progress_label' in globals():
            update_math_progress_display()
    except ValueError:
        math_tasks_per_level = 10
        math_tasks_per_level_entry.delete(0, tk.END)
        math_tasks_per_level_entry.insert(0, "10")

def update_math_ranges():
    """Обновляет диапазоны чисел для разных уровней сложности"""
    global math_difficulty_ranges
    try:
        # Лёгкий
        easy_range = math_range_easy_entry.get().strip()
        if "-" in easy_range:
            min_val, max_val = map(int, easy_range.split("-"))
            math_difficulty_ranges["Лёгкий"] = [min_val, max_val]
        
        # Нормальный
        normal_range = math_range_normal_entry.get().strip()
        if "-" in normal_range:
            min_val, max_val = map(int, normal_range.split("-"))
            math_difficulty_ranges["Нормальный"] = [min_val, max_val]
        
        # Сложный
        hard_range = math_range_hard_entry.get().strip()
        if "-" in hard_range:
            min_val, max_val = map(int, hard_range.split("-"))
            math_difficulty_ranges["Сложный"] = [min_val, max_val]
    except (ValueError, AttributeError):
        pass  # Игнорируем ошибки парсинга

def update_case_sensitivity():
    global case_sensitive
    case_sensitive = case_var.get()

def update_punctuation_sensitivity():
    global punctuation_sensitive
    punctuation_sensitive = punct_var.get()

def update_font_size():
    global font_size
    try:
        font_size = int(font_entry.get())
        if font_size < 8:
            font_size = 8
            font_entry.delete(0, tk.END)
            font_entry.insert(0, "8")
        sample_text.config(font=("Courier New", font_size))
        text_widget.config(font=("Courier New", font_size))
        line_sample_text.config(font=("Courier New", font_size))
        line_text_widget.config(font=("Courier New", font_size))
        quatrain_sample_text.config(font=("Courier New", font_size))
        quatrain_text_widget.config(font=("Courier New", font_size))


    except ValueError:
        font_size = 18
        font_entry.delete(0, tk.END)
        font_entry.insert(0, "18")

def update_auto_clear():
    global auto_clear
    auto_clear = auto_clear_var.get()

def update_theme():
    global bg_color, text_bg_color, button_color, text_color, theme
    theme = theme_var.get()
    selected_theme = themes[theme]
    
    bg_color = selected_theme["bg_color"]
    text_bg_color = selected_theme["text_bg_color"]
    button_color = selected_theme["button_color"]
    text_color = selected_theme["text_color"]
    
    root.config(bg=bg_color)
    settings_canvas.config(bg=bg_color)
    settings_frame.config(bg=bg_color)
    sample_text.config(bg=text_bg_color, fg=text_color)
    text_widget.config(bg=text_bg_color, fg=text_color)
    status_label.config(bg=bg_color, fg=text_color)
    error_label.config(bg=bg_color, fg=text_color)
    font_label.config(bg=bg_color, fg=text_color)
    case_check.config(bg=bg_color, fg=text_color)
    punct_check.config(bg=bg_color, fg=text_color)
    auto_clear_check.config(bg=bg_color, fg=text_color)
    line_sample_text.config(bg=text_bg_color, fg=text_color)
    line_text_widget.config(bg=text_bg_color, fg=text_color)
    line_status_label.config(bg=bg_color, fg=text_color)
    quatrain_sample_text.config(bg=text_bg_color, fg=text_color)
    quatrain_text_widget.config(bg=text_bg_color, fg=text_color)
    quatrain_status_label.config(bg=bg_color, fg=text_color)
    theme_label.config(bg=bg_color, fg=text_color)
    language_label.config(bg=bg_color, fg=text_color)
    
    # Обновляем цвета математического тренажёра
    if 'math_frame' in globals() and math_frame:
        math_frame.config(bg=bg_color)
        math_left_frame.config(bg=bg_color)
        math_right_frame.config(bg=bg_color)
        math_level_label.config(bg=bg_color, fg=text_color)
        math_points_label.config(bg=bg_color, fg=text_color)
        math_progress_label.config(bg=bg_color, fg=text_color)
        math_difficulty_label.config(bg=bg_color, fg=text_color)
        math_difficulty_frame.config(bg=bg_color)
        math_task_label.config(bg=bg_color, fg=text_color)
        math_status_label.config(bg=bg_color, fg=text_color)
        math_answer_entry.config(bg=text_bg_color, fg=text_color)
        if 'math_easy_radio' in globals():
            math_easy_radio.config(bg=bg_color, fg=text_color, selectcolor=bg_color)
            math_normal_radio.config(bg=bg_color, fg=text_color, selectcolor=bg_color)
            math_hard_radio.config(bg=bg_color, fg=text_color, selectcolor=bg_color)
    
    # Обновляем цвета подменю стихов
    if poems_submenu_frame:
        poems_submenu_frame.config(bg=bg_color)
        poems_submenu_buttons_frame.config(bg=bg_color)
        poems_submenu_title_label.config(bg=bg_color, fg=text_color)
    
    # Обновляем цвета настроек математики
    if 'math_settings_title' in globals():
        math_settings_title.config(bg=bg_color, fg=text_color)
        math_operations_label.config(bg=bg_color, fg=text_color)
        math_add_check.config(bg=bg_color, fg=text_color)
        math_subtract_check.config(bg=bg_color, fg=text_color)
        math_multiply_check.config(bg=bg_color, fg=text_color)
        math_divide_check.config(bg=bg_color, fg=text_color)
        math_range_easy_label.config(bg=bg_color, fg=text_color)
        math_range_normal_label.config(bg=bg_color, fg=text_color)
        math_range_hard_label.config(bg=bg_color, fg=text_color)
        math_tasks_per_level_label.config(bg=bg_color, fg=text_color)
    
    update_all_buttons()

def update_language():
    global language
    language = language_var.get()
    root.title(translations[language]["title"])
    notebook.tab(frame_main, text=translations[language]["tab_main"])
    notebook.tab(line_frame, text=translations[language]["tab_lines"])
    notebook.tab(quatrain_frame, text=translations[language]["tab_paragraphs"])
    notebook.tab(frame_settings, text=translations[language]["tab_settings"])
    check_button.config(text=translations[language]["check"])
    reset_button.config(text=translations[language]["reset"])
    line_check_button.config(text=translations[language]["check"])
    line_reset_button.config(text=translations[language]["reset"])
    quatrain_check_button.config(text=translations[language]["check"])
    quatrain_reset_button.config(text=translations[language]["reset"])
    case_check.config(text=translations[language]["case_sensitive"])
    punct_check.config(text=translations[language]["punct_sensitive"])
    auto_clear_check.config(text=translations[language]["auto_clear"])
    font_label.config(text=translations[language]["font_size"])
    theme_label.config(text=translations[language]["theme"])
    language_label.config(text=translations[language]["language"])
    open_folder_button.config(text=translations[language]["open_folder"])
    poem_selector_button.config(text=translations[language]["explore_poems"])
    status_label.config(text=translations[language]["status_main"])
    error_label.config(text=translations[language]["errors"].format(error_count))
    MD_label.config(text=translations[language]["MD"])
    # Обновляем кнопки главного меню
    if menu_frame:
        menu_title_label.config(text=translations[language]["title"])
        if 'poems_mode_button' in globals():
            poems_mode_button.config(text=translations[language]["poems"])
        if 'math_mode_button' in globals():
            math_mode_button.config(text=translations[language]["mathematics"])
        settings_mode_button.config(text=translations[language]["tab_settings"])
    # Обновляем подменю стихов
    if poems_submenu_frame:
        poems_submenu_title_label.config(text=translations[language]["poems"])
        if 'poems_main_mode_button' in globals():
            poems_main_mode_button.config(text=translations[language]["tab_main"])
        if 'poems_lines_mode_button' in globals():
            poems_lines_mode_button.config(text=translations[language]["tab_lines"])
        if 'poems_paragraphs_mode_button' in globals():
            poems_paragraphs_mode_button.config(text=translations[language]["tab_paragraphs"])
        if 'poems_back_button' in globals():
            poems_back_button.config(text=translations[language]["back_to_menu"])
    # Обновляем кнопки "Назад"
    if 'back_main_button' in globals():
        back_main_button.config(text=translations[language]["back_to_menu"])
    if 'back_lines_button' in globals():
        back_lines_button.config(text=translations[language]["back_to_menu"])
    if 'back_quatrain_button' in globals():
        back_quatrain_button.config(text=translations[language]["back_to_menu"])
    if 'back_settings_button' in globals():
        back_settings_button.config(text=translations[language]["back_to_menu"])
    # Обновляем математический тренажёр
    if 'math_frame' in globals() and math_frame:
        if 'math_back_button' in globals():
            math_back_button.config(text=translations[language]["back_to_menu"])
        if 'math_level_label' in globals():
            update_math_progress_display()
        if 'math_task_label' in globals() and math_current_task:
            math_task_label.config(text=f"{translations[language]['math_task']} {math_current_task.split('=')[0]} = ?")
        if 'math_check_button' in globals():
            math_check_button.config(text=translations[language]["math_check"])
        if 'math_new_task_button' in globals():
            math_new_task_button.config(text=translations[language]["math_new_task"])
        if 'math_difficulty_label' in globals():
            math_difficulty_label.config(text=translations[language]["math_difficulty"])
        if 'math_easy_radio' in globals():
            math_easy_radio.config(text=translations[language]["math_easy"])
            math_normal_radio.config(text=translations[language]["math_normal"])
            math_hard_radio.config(text=translations[language]["math_hard"])
    # Обновляем настройки математики
    if 'math_settings_title' in globals():
        math_settings_title.config(text=translations[language]["math_settings_title"])
    if 'math_operations_label' in globals():
        math_operations_label.config(text=translations[language]["math_operations"])
    if 'math_add_check' in globals():
        math_add_check.config(text=translations[language]["math_add"])
        math_subtract_check.config(text=translations[language]["math_subtract"])
        math_multiply_check.config(text=translations[language]["math_multiply"])
        math_divide_check.config(text=translations[language]["math_divide"])
    if 'math_range_easy_label' in globals():
        math_range_easy_label.config(text=translations[language]["math_range_easy"])
        math_range_normal_label.config(text=translations[language]["math_range_normal"])
        math_range_hard_label.config(text=translations[language]["math_range_hard"])
    if 'math_tasks_per_level_label' in globals():
        math_tasks_per_level_label.config(text=translations[language]["math_tasks_per_level"])
    if lines:
        line_status_label.config(text=translations[language]["status_lines"].format(current_line + 1, len(lines)))
    if quatrains:
        quatrain_status_label.config(text=translations[language]["status_para"].format(current_quatrain + 1, len(quatrains)))

def save_settings():
    global math_operations, math_difficulty_ranges, math_tasks_per_level
    # Обновляем диапазоны перед сохранением
    update_math_ranges()
    update_math_tasks_per_level()
    
    settings = {
        "case_sensitive": case_sensitive, "punctuation_sensitive": punctuation_sensitive,
        "delay_time": delay_time, "font_size": font_size, "auto_clear": auto_clear,
        "theme": theme_var.get(), "language": language_var.get(),
        "math_operations": math_operations,
        "math_difficulty_ranges": math_difficulty_ranges,
        "math_tasks_per_level": math_tasks_per_level,
        "math_add": math_add_var.get(),
        "math_subtract": math_subtract_var.get(),
        "math_multiply": math_multiply_var.get(),
        "math_divide": math_divide_var.get()
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(script_dir, f"{current_profile}.txt")

    # Сохраняем прогресс математики
    math_progress = {
        "level": math_level,
        "points": math_points,
        "tasks_completed": math_tasks_completed
    }

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            profile_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        profile_data = {"name": current_profile, "password": "", "settings": {}, "math_progress": {}}
    
    profile_data["settings"] = settings
    profile_data["math_progress"] = math_progress
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)

def load_settings():
    global case_sensitive, punctuation_sensitive, delay_time, font_size, auto_clear, theme, language, current_profile
    global math_level, math_points, math_tasks_completed, math_operations, math_difficulty_ranges, math_tasks_per_level
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(script_dir, f"{current_profile}.txt")
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as f:
            profile_data = json.load(f)
            settings = profile_data.get("settings", {})
            case_sensitive = settings.get("case_sensitive", True)
            punctuation_sensitive = settings.get("punctuation_sensitive", True)
            delay_time = settings.get("delay_time", 6)
            font_size = settings.get("font_size", 18)
            auto_clear = settings.get("auto_clear", True)
            theme_var.set(settings.get("theme", "Светлая"))
            language_var.set(settings.get("language", "Русский"))
            case_var.set(case_sensitive)
            punct_var.set(punctuation_sensitive)
            auto_clear_var.set(auto_clear)
            font_entry.delete(0, tk.END)
            font_entry.insert(0, str(font_size))
            
            # Загружаем настройки математики
            math_operations = settings.get("math_operations", ["+", "-", "*", "/"])
            math_difficulty_ranges = settings.get("math_difficulty_ranges", {
                "Лёгкий": [1, 20],
                "Нормальный": [1, 100],
                "Сложный": [1, 1000]
            })
            math_tasks_per_level = settings.get("math_tasks_per_level", 10)
            
            # Загружаем чекбоксы операций
            math_add_var.set(settings.get("math_add", True))
            math_subtract_var.set(settings.get("math_subtract", True))
            math_multiply_var.set(settings.get("math_multiply", True))
            math_divide_var.set(settings.get("math_divide", True))
            
            # Обновляем поля диапазонов
            if 'math_range_easy_entry' in globals():
                math_range_easy_entry.delete(0, tk.END)
                math_range_easy_entry.insert(0, f"{math_difficulty_ranges['Лёгкий'][0]}-{math_difficulty_ranges['Лёгкий'][1]}")
                math_range_normal_entry.delete(0, tk.END)
                math_range_normal_entry.insert(0, f"{math_difficulty_ranges['Нормальный'][0]}-{math_difficulty_ranges['Нормальный'][1]}")
                math_range_hard_entry.delete(0, tk.END)
                math_range_hard_entry.insert(0, f"{math_difficulty_ranges['Сложный'][0]}-{math_difficulty_ranges['Сложный'][1]}")
                math_tasks_per_level_entry.delete(0, tk.END)
                math_tasks_per_level_entry.insert(0, str(math_tasks_per_level))
            
            # Загружаем прогресс математики
            math_progress = profile_data.get("math_progress", {})
            math_level = math_progress.get("level", 1)
            math_points = math_progress.get("points", 0.0)
            math_tasks_completed = math_progress.get("tasks_completed", 0)
            
            update_theme()
            update_language()
            
            # Обновляем отображение прогресса математики если интерфейс создан
            if 'math_level_label' in globals():
                update_math_progress_display()
                if not math_current_task:
                    generate_new_math_task()

def open_folder():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":
            subprocess.run(["open", folder_path])
        elif system == "Linux":
            subprocess.run(["xdg-open", folder_path])
    except Exception as e:
        messagebox.showerror("Error" if language == "English" else "Ошибка", f"Failed to open folder: {e}")

def on_mouse_wheel(event, canvas=None):
    if canvas:
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")


# Исследовать стихи

def fetch_stihi_ru_data():
    try:
        url = "https://stihi.ru"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Запрос главной страницы: статус {response.status_code}")  # Диагностика
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        poem_links = soup.select('.poemlink')
        print(f"Найдено стихов: {len(poem_links)}")  # Диагностика
        poems = []
        for link in poem_links:  # Убрал [:10], чтобы загрузить все стихи
            title = link.text.strip()
            poem_url = "https://stihi.ru" + link['href']
            poem_response = requests.get(poem_url, headers=headers, timeout=10)
            print(f"Запрос стиха {title}: статус {poem_response.status_code}")  # Диагностика
            poem_soup = BeautifulSoup(poem_response.text, 'html.parser')
            
            # Извлечение текста стиха
            poem_text_elem = poem_soup.select_one('div.text')
            poem_text = poem_text_elem.text.strip() if poem_text_elem else "Текст не найден"
            
            # Извлечение автора
            # Попытка 1: селектор .poetauthor
            author_elem = poem_soup.select_one('.poetauthor')
            if author_elem:
                author = author_elem.text.strip()
                print(f"Автор найден через .poetauthor: {author}")  # Диагностика
            else:
                # Попытка 2: поиск <a> с href, начинающимся на /avtor/
                author_link = poem_soup.select_one('a[href^="/avtor/"]')
                if author_link:
                    author = author_link.text.strip()
                    print(f"Автор найден через ссылку /avtor/: {author}")  # Диагностика
                else:
                    # Попытка 3: поиск после заголовка
                    title_elem = poem_soup.select_one('h1')
                    if title_elem:
                        next_elem = title_elem.find_next()
                        if next_elem and next_elem.name in ['div', 'span', 'a']:
                            author = next_elem.text.strip()
                            print(f"Автор найден после заголовка: {author}")  # Диагностика
                        else:
                            author = "Неизвестный автор"
                            print("Автор не найден: использован запасной вариант 'Неизвестный автор'")  # Диагностика
                    else:
                        author = "Неизвестный автор"
                        print("Заголовок не найден, автор установлен как 'Неизвестный автор'")  # Диагностика
            
            # Извлечение даты
            date_elem = poem_soup.select_one('.date')
            date = date_elem.text.strip() if date_elem else "Дата неизвестна"
            
            poems.append({'title': title, 'text': poem_text, 'author': author, 'date': date})
        return poems
    except Exception as e:
        print(f"Ошибка загрузки стихов: {e}")  # Диагностика
        return None

def fetch_poems_incremental(callback, error_callback, completion_callback=None):
    """
    Загружает стихи инкрементально, вызывая callback для каждого загруженного стиха.
    callback(poem) - вызывается для каждого загруженного стиха
    error_callback() - вызывается при ошибке
    completion_callback() - вызывается после завершения загрузки всех стихов
    """
    try:
        url = "https://stihi.ru"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Запрос главной страницы: статус {response.status_code}")  # Диагностика
        if response.status_code != 200:
            root.after(0, error_callback)
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        poem_links = soup.select('.poemlink')
        print(f"Найдено стихов: {len(poem_links)}")  # Диагностика
        
        if not poem_links:
            root.after(0, error_callback)
            return
        
        for link in poem_links:
            try:
                title = link.text.strip()
                poem_url = "https://stihi.ru" + link['href']
                poem_response = requests.get(poem_url, headers=headers, timeout=10)
                print(f"Запрос стиха {title}: статус {poem_response.status_code}")  # Диагностика
                poem_soup = BeautifulSoup(poem_response.text, 'html.parser')
                
                # Извлечение текста стиха
                poem_text_elem = poem_soup.select_one('div.text')
                poem_text = poem_text_elem.text.strip() if poem_text_elem else "Текст не найден"
                
                # Извлечение автора
                author_elem = poem_soup.select_one('.poetauthor')
                if author_elem:
                    author = author_elem.text.strip()
                    print(f"Автор найден через .poetauthor: {author}")  # Диагностика
                else:
                    author_link = poem_soup.select_one('a[href^="/avtor/"]')
                    if author_link:
                        author = author_link.text.strip()
                        print(f"Автор найден через ссылку /avtor/: {author}")  # Диагностика
                    else:
                        title_elem = poem_soup.select_one('h1')
                        if title_elem:
                            next_elem = title_elem.find_next()
                            if next_elem and next_elem.name in ['div', 'span', 'a']:
                                author = next_elem.text.strip()
                                print(f"Автор найден после заголовка: {author}")  # Диагностика
                            else:
                                author = "Неизвестный автор"
                                print("Автор не найден: использован запасной вариант 'Неизвестный автор'")  # Диагностика
                        else:
                            author = "Неизвестный автор"
                            print("Заголовок не найден, автор установлен как 'Неизвестный автор'")  # Диагностика
                
                # Извлечение даты
                date_elem = poem_soup.select_one('.date')
                date = date_elem.text.strip() if date_elem else "Дата неизвестна"
                
                poem = {'title': title, 'text': poem_text, 'author': author, 'date': date}
                # Вызываем callback через root.after() для обновления UI из главного потока
                root.after(0, lambda p=poem: callback(p))
            except Exception as e:
                print(f"Ошибка загрузки стиха {title if 'title' in locals() else 'unknown'}: {e}")  # Диагностика
                continue
        
        # Вызываем completion_callback после завершения загрузки всех стихов
        if completion_callback:
            root.after(0, completion_callback)
    except Exception as e:
        print(f"Ошибка загрузки стихов: {e}")  # Диагностика
        root.after(0, error_callback)

def open_poem_selector():
    # Сохраняем текущий интерфейс
    original_widgets = []
    for widget in root.winfo_children():
        original_widgets.append(widget)
        # Проверяем, что виджет использует grid менеджер перед вызовом grid_remove()
        try:
            widget.grid_info()  # Проверяем, используется ли grid
            widget.grid_remove()  # Скрываем текущий интерфейс
        except (AttributeError, tk.TclError):
            # Если виджет не использует grid (например, Toplevel), просто пропускаем
            pass

    # Создаём фрейм для нового интерфейса
    poem_frame = tk.Frame(root, bg=bg_color)
    poem_frame.place(x=0, y=0, relwidth=1, relheight=1)  # Размещаем поверх всего интерфейса
    root.update_idletasks()  # Принудительно обновляем интерфейс

    # Список стихов
    poem_left_frame = tk.Frame(poem_frame, bg=bg_color)
    poem_left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    poem_left_frame.grid_rowconfigure(1, weight=1)  # Настраиваем расширение для списка
    poem_left_frame.grid_columnconfigure(0, weight=1)
    # Метка загрузки
    poem_loading_label = tk.Label(poem_left_frame, text="", font=("Courier New", 16), fg=text_color, bg=bg_color)
    poem_loading_label.grid(row=0, column=0, pady=5, sticky="ew")
    # Фрейм для списка и скроллбара
    listbox_frame = tk.Frame(poem_left_frame, bg=bg_color)
    listbox_frame.grid(row=1, column=0, sticky="nsew")
    poem_listbox = tk.Listbox(listbox_frame, width=50, font=("Courier New", 16))
    poem_listbox.pack(side="left", fill="both", expand=True)
    poem_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=poem_listbox.yview)
    poem_scrollbar.pack(side="right", fill="y")
    poem_listbox.config(yscrollcommand=poem_scrollbar.set)

    # Предварительный просмотр
    poem_preview_frame = tk.Frame(poem_frame, bg=bg_color)
    poem_preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    poem_preview_title = tk.Label(poem_preview_frame, text="", font=("Courier New", 20, "bold"), bg=bg_color, fg=text_color, wraplength=700, justify="center")
    poem_preview_title.pack(fill="x", padx=10, pady=5)
    poem_preview_author = tk.Label(poem_preview_frame, text="", font=("Courier New", 16, "italic"), bg=bg_color, fg=text_color, wraplength=700)
    poem_preview_author.pack(fill="x", padx=10, pady=5)
    poem_preview_date = tk.Label(poem_preview_frame, text="", font=("Courier New", 16), bg=bg_color, fg=text_color, wraplength=700)
    poem_preview_date.pack(fill="x", padx=10, pady=5)
    poem_preview_text = tk.Text(poem_preview_frame, wrap="word", state="disabled", font=("Courier New", 16), height=25, bg=text_bg_color, fg=text_color)
    poem_preview_text.pack(fill="both", expand=True, padx=10, pady=5)

    # Фрейм для кнопок (все кнопки на одном уровне)
    button_frame = tk.Frame(poem_frame, bg=bg_color)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

    # Кнопка "Добавить в stih.txt"
    poem_add_button_img = create_rounded_button_image(button_width + 50, button_height + 10, button_radius, button_color, bg_color)
    poem_add_button = tk.Button(button_frame, image=poem_add_button_img, text=translations[language]["add_to_stih"], 
                               compound="center", command=lambda: add_to_stih(poem_listbox, poem_frame), state="disabled",
                               fg=text_color, font=("Courier New", 18), borderwidth=0, bg=bg_color, activebackground=bg_color)
    poem_add_button.image = poem_add_button_img
    poem_add_button.grid(row=0, column=0, padx=10)

    # Кнопка "Перейти на stihi.ru"
    poem_site_button_img = create_rounded_button_image(button_width + 50, button_height + 10, button_radius, button_color, bg_color)
    poem_site_button = tk.Button(button_frame, image=poem_site_button_img, text=translations[language]["go_to_stihi"], 
                                compound="center", command=lambda: webbrowser.open("https://stihi.ru"),
                                fg=text_color, font=("Courier New", 18), borderwidth=0, bg=bg_color, activebackground=bg_color)
    poem_site_button.image = poem_site_button_img
    poem_site_button.grid(row=0, column=1, padx=10)

    # Кнопка "Назад"
    back_button_img = create_rounded_button_image(button_width + 50, button_height + 10, button_radius, button_color, bg_color)
    back_button = tk.Button(button_frame, image=back_button_img, text=translations[language]["back"], 
                           compound="center", command=lambda: restore_main_interface(poem_frame, original_widgets),
                           fg=text_color, font=("Courier New", 18), borderwidth=0, bg=bg_color, activebackground=bg_color)
    back_button.image = back_button_img
    back_button.grid(row=0, column=2, padx=10)

    # Кнопка "Повторить"
    retry_button_img = create_rounded_button_image(button_width + 50, button_height + 10, button_radius, button_color, bg_color)
    retry_button = tk.Button(button_frame, image=retry_button_img, text=translations[language]["retry"], compound="center",
                            command=lambda: load_poems(), fg=text_color, font=("Courier New", 18), borderwidth=0, 
                            bg=bg_color, activebackground=bg_color)
    retry_button.image = retry_button_img
    retry_button.grid(row=0, column=3, padx=10)
    retry_button.grid_remove()

    # Метка для ошибок
    poem_error_label = tk.Label(poem_frame, text="", font=("Courier New", 18), fg="red", bg=bg_color)
    poem_error_label.grid(row=2, column=0, columnspan=2, pady=5)

    poem_frame.grid_rowconfigure(0, weight=1)
    poem_frame.grid_columnconfigure(0, weight=1)
    poem_frame.grid_columnconfigure(1, weight=3)

    def load_poems():
        print("Загрузка стихов")  # Диагностика
        poem_listbox.delete(0, tk.END)
        poem_preview_title.config(text="")
        poem_preview_author.config(text="")
        poem_preview_date.config(text="")
        poem_preview_text.config(state="normal")
        poem_preview_text.delete("1.0", tk.END)
        poem_preview_text.config(state="disabled")
        poem_add_button.config(state="disabled")
        poem_error_label.config(text="")
        retry_button.grid_remove()
        
        # Показываем метку загрузки
        poem_loading_label.config(text=translations[language]["loading_poems"])
        
        # Инициализируем список стихов
        poem_frame.poems = []
        poem_frame.loading_complete = False
        
        def add_poem_to_list(poem):
            """Callback для добавления загруженного стиха в список"""
            poem_frame.poems.append(poem)
            poem_listbox.insert(tk.END, poem['title'])
            # Если это первый стих, активируем кнопку добавления
            if len(poem_frame.poems) == 1:
                poem_add_button.config(state="normal")
        
        def finish_loading():
            """Вызывается когда загрузка завершена"""
            poem_frame.loading_complete = True
            poem_loading_label.config(text="")
            print(f"Загрузка завершена. Всего стихов: {len(poem_frame.poems)}")
        
        def handle_error():
            """Callback для обработки ошибок"""
            poem_frame.loading_complete = True
            poem_loading_label.config(text="")
            if not poem_frame.poems:
                poem_error_label.config(text=translations[language]["failed_to_load"])
                retry_button.grid(row=0, column=3, padx=10)
        
        def load_poems_thread():
            """Функция для фонового потока"""
            try:
                fetch_poems_incremental(add_poem_to_list, handle_error, finish_loading)
            except Exception as e:
                print(f"Ошибка в потоке загрузки: {e}")
                root.after(0, handle_error)
        
        threading.Thread(target=load_poems_thread, daemon=True).start()

# Конец выбора стихов

    def on_poem_select(event):
        selection = poem_listbox.curselection()
        if selection:
            index = selection[0]
            poem = poem_frame.poems[index]
            poem_preview_title.config(text=poem['title'])
            poem_preview_author.config(text=f"{translations[language]['author']}: {poem['author']}")
            poem_preview_date.config(text=f"{translations[language]['date']}: {poem['date']}")
            poem_preview_text.config(state="normal")
            poem_preview_text.delete("1.0", tk.END)
            poem_preview_text.insert(tk.END, poem['text'])
            poem_preview_text.config(state="disabled")
            poem_add_button.config(state="normal")

    def add_to_stih(listbox, frame):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            item = frame.poems[index]
            text = item['text']
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "stih.txt")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text + "\n\n")
                messagebox.showinfo(translations[language]["success"], translations[language]["poem_added"])
                load_text_from_file()
                restore_main_interface(frame, original_widgets)
            except Exception as e:
                messagebox.showerror(translations[language]["error"], f"Failed to add poem: {e}")

    def restore_main_interface(frame, original_widgets):
        frame.place_forget()  # Убираем фрейм
        frame.destroy()
        for widget in original_widgets:
            # Восстанавливаем только те виджеты, которые используют grid
            try:
                widget.grid_info()  # Проверяем, использовался ли grid
                widget.grid()  # Восстанавливаем исходный интерфейс
            except (AttributeError, tk.TclError):
                # Если виджет не использует grid, пропускаем
                pass

    poem_listbox.bind("<<ListboxSelect>>", on_poem_select)
    load_poems()

# Конец выбора стихов

def update_all_buttons():

    global check_button, reset_button, line_check_button, line_reset_button, quatrain_check_button, quatrain_reset_button, open_folder_button, poem_selector_button, help_mode_button
    for btn in [check_button, line_check_button, quatrain_check_button]:
        new_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
        btn.config(image=new_img, fg=text_color)
        btn.image = new_img
    for btn in [reset_button, line_reset_button, quatrain_reset_button]:
        new_img = create_rounded_button_image(reset_button_width, button_height, button_radius, button_color, bg_color)
        btn.config(image=new_img, fg=text_color)
        btn.image = new_img
    for btn in [open_folder_button, poem_selector_button]:
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        btn.config(image=new_img, fg=text_color)
        btn.image = new_img
    if 'help_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        help_mode_button.config(image=new_img, fg=text_color)
        help_mode_button.image = new_img
    # Обновляем кнопки математического тренажёра
    if 'math_check_button' in globals():
        new_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
        math_check_button.config(image=new_img, fg=text_color)
        math_check_button.image = new_img
    if 'math_new_task_button' in globals():
        new_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
        math_new_task_button.config(image=new_img, fg=text_color)
        math_new_task_button.image = new_img
    if 'math_back_button' in globals():
        new_img = create_rounded_button_image(150, 40, button_radius, button_color, bg_color)
        math_back_button.config(image=new_img, fg=text_color)
        math_back_button.image = new_img
    # Обновляем кнопки главного меню
    if 'poems_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        poems_mode_button.config(image=new_img, fg=text_color)
        poems_mode_button.image = new_img
    if 'math_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        math_mode_button.config(image=new_img, fg=text_color)
        math_mode_button.image = new_img
    if 'settings_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        settings_mode_button.config(image=new_img, fg=text_color)
        settings_mode_button.image = new_img
    # Обновляем кнопки подменю стихов
    if 'poems_main_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        poems_main_mode_button.config(image=new_img, fg=text_color)
        poems_main_mode_button.image = new_img
    if 'poems_lines_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        poems_lines_mode_button.config(image=new_img, fg=text_color)
        poems_lines_mode_button.image = new_img
    if 'poems_paragraphs_mode_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        poems_paragraphs_mode_button.config(image=new_img, fg=text_color)
        poems_paragraphs_mode_button.image = new_img
    if 'poems_back_button' in globals():
        new_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
        poems_back_button.config(image=new_img, fg=text_color)
        poems_back_button.image = new_img

def switch_profile(profile):
    global current_profile
    script_dir = os.path.dirname(os.path.abspath(__file__))
    profile_path = os.path.join(script_dir, f"{profile}.txt")
    with open(profile_path, "r", encoding="utf-8") as f:
        profile_data = json.load(f)
    
    if profile_data["password"]:
        password_window = tk.Toplevel(root)
        password_window.title(translations[language]["enter_password"])
        password_window.geometry("300x150")
        password_window.transient(root)
        password_window.grab_set()

        tk.Label(password_window, text=translations[language]["enter_password"], font=("Courier New", 16)).pack(pady=10)
        password_entry = tk.Entry(password_window, show="*", font=("Courier New", 16))
        password_entry.pack(pady=10)

        def check_password():
            if password_entry.get() == profile_data["password"]:
                current_profile = profile
                profile_var.set(profile)
                load_settings()
                password_window.destroy()
            else:
                messagebox.showerror("Error" if language == "English" else "Ошибка", 
                                    "Incorrect password" if language == "English" else "Неверный пароль")

        confirm_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
        confirm_button = tk.Button(password_window, image=confirm_button_img, text="OK", compound="center", 
                                   command=check_password, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
        confirm_button.image = confirm_button_img
        confirm_button.pack(pady=10)
    else:
        current_profile = profile
        profile_var.set(profile)
        load_settings()

def create_profile():
    profile_window = tk.Toplevel(root)
    profile_window.title(translations[language]["create_profile"])
    profile_window.geometry("400x250")
    profile_window.transient(root)
    profile_window.grab_set()

    tk.Label(profile_window, text=translations[language]["profile_name"], font=("Courier New", 16)).grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(profile_window, font=("Courier New", 16))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(profile_window, text=translations[language]["profile_password"], font=("Courier New", 16)).grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(profile_window, show="*", font=("Courier New", 16))
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def save_new_profile():
        profile_name = name_entry.get().strip()
        profile_password = password_entry.get().strip()
        if not profile_name:
            messagebox.showerror("Error" if language == "English" else "Ошибка", 
                                "Profile name is required" if language == "English" else "Имя профиля обязательно")
            return
        
        selected_profile = profile_var.get()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        profile_path = os.path.join(script_dir, f"{selected_profile}.txt")
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump({
                "name": profile_name, 
                "password": profile_password, 
                "settings": {},
                "math_progress": {
                    "level": 1,
                    "points": 0.0,
                    "tasks_completed": 0
                }
            }, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Success" if language == "English" else "Успех", 
                           "Profile created" if language == "English" else "Профиль создан")
        profile_window.destroy()

    save_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
    save_button = tk.Button(profile_window, image=save_button_img, text="Save" if language == "English" else "Сохранить", compound="center", 
                            command=save_new_profile, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
    save_button.image = save_button_img
    save_button.grid(row=2, column=0, columnspan=2, pady=20)

def update_error_label():
    error_label.config(text=translations[language]["errors"].format(error_count))

def show_help():
    """Показывает окно помощи с описанием программы"""
    help_window = tk.Toplevel(root)
    help_window.title(translations[language]["help_title"])
    help_window.geometry("800x700")
    help_window.transient(root)
    help_window.config(bg=bg_color)
    
    # Заголовок
    help_title_label = tk.Label(help_window, text=translations[language]["help_title"], 
                               font=("Courier New", 24, "bold"), bg=bg_color, fg=text_color)
    help_title_label.pack(pady=20)
    
    # Фрейм с прокруткой для текста помощи
    help_canvas = tk.Canvas(help_window, bg=bg_color)
    help_scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=help_canvas.yview)
    help_scrollable_frame = tk.Frame(help_canvas, bg=bg_color)
    
    help_scrollable_frame.bind(
        "<Configure>",
        lambda e: help_canvas.configure(scrollregion=help_canvas.bbox("all"))
    )
    
    help_canvas.create_window((0, 0), window=help_scrollable_frame, anchor="nw")
    help_canvas.configure(yscrollcommand=help_scrollbar.set)
    
    # Текст помощи
    help_text_widget = tk.Text(help_scrollable_frame, wrap="word", width=70, height=30,
                              font=("Courier New", 14), bg=text_bg_color, fg=text_color,
                              padx=20, pady=20, state="disabled", exportselection=0)
    help_text_widget.pack(fill="both", expand=True)
    
    # Вставляем текст помощи
    help_text_widget.config(state="normal")
    help_text_widget.insert("1.0", translations[language]["help_text"])
    help_text_widget.config(state="disabled")
    
    # Привязка событий для предотвращения выделения
    help_text_widget.bind("<Button-1>", lambda e: prevent_selection(e, help_text_widget))
    help_text_widget.bind("<B1-Motion>", lambda e: prevent_selection(e, help_text_widget))
    help_text_widget.bind("<Control-a>", lambda e: prevent_selection(e, help_text_widget))
    
    # Кнопка закрытия
    close_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
    close_button = tk.Button(help_window, image=close_button_img, text=translations[language]["back"], 
                            compound="center", command=help_window.destroy,
                            fg=text_color, font=("Courier New", 18), borderwidth=0, 
                            bg=bg_color, activebackground=bg_color)
    close_button.image = close_button_img
    close_button.pack(pady=20)
    
    help_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
    help_scrollbar.pack(side="right", fill="y")
    
    # Привязка прокрутки колесиком мыши
    help_canvas.bind("<MouseWheel>", lambda e: on_mouse_wheel(e, help_canvas))
    
    # Обновление размеров при изменении окна
    def configure_help_scroll(event):
        help_canvas.configure(scrollregion=help_canvas.bbox("all"))
    help_scrollable_frame.bind("<Configure>", configure_help_scroll)

# Функция для создания tooltip
def create_tooltip(widget, text):
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1,
                        font=("Courier New", 12), wraplength=400, justify="left")
        label.pack()
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)

# Функция для предотвращения выделения текста
def prevent_selection(event, text_widget):
    text_widget.tag_remove(tk.SEL, "1.0", tk.END)  # Удаляем любое выделение
    return "break"  # Прерываем дальнейшую обработку события

# Глобальные переменные для навигации
current_mode = None  # Текущий активный режим
menu_frame = None  # Фрейм главного меню
poems_submenu_frame = None  # Фрейм подменю стихов

# Функции навигации
def show_main_menu():
    """Показывает главное меню и скрывает текущий режим"""
    global current_mode, menu_frame, poems_submenu_frame
    
    # Скрываем текущий режим (notebook)
    if notebook.winfo_viewable():
        try:
            notebook.grid_info()
            notebook.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Скрываем подменю стихов если открыто
    if poems_submenu_frame:
        try:
            poems_submenu_frame.grid_info()
            poems_submenu_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Скрываем математический тренажёр если открыт
    if 'math_frame' in globals() and math_frame:
        try:
            math_frame.grid_info()
            math_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Показываем главное меню
    if menu_frame:
        try:
            menu_frame.grid_info()
            menu_frame.grid()
        except (AttributeError, tk.TclError):
            menu_frame.grid(row=0, column=0, sticky="nsew")
    
    current_mode = None

def show_poems_submenu():
    """Показывает подменю для режимов стихов"""
    global poems_submenu_frame
    
    # Скрываем главное меню
    if menu_frame:
        try:
            menu_frame.grid_info()
            menu_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Показываем подменю стихов
    if poems_submenu_frame:
        try:
            poems_submenu_frame.grid_info()
            poems_submenu_frame.grid()
        except (AttributeError, tk.TclError):
            poems_submenu_frame.grid(row=0, column=0, sticky="nsew")

def show_math_trainer():
    """Показывает математический тренажёр"""
    global current_mode
    
    # Скрываем главное меню
    if menu_frame:
        try:
            menu_frame.grid_info()
            menu_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Скрываем подменю стихов если открыто
    if poems_submenu_frame:
        try:
            poems_submenu_frame.grid_info()
            poems_submenu_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Скрываем notebook если открыт
    if notebook.winfo_viewable():
        try:
            notebook.grid_info()
            notebook.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Показываем математический тренажёр
    if 'math_frame' in globals() and math_frame:
        try:
            math_frame.grid_info()
            math_frame.grid(row=0, column=0, sticky="nsew")
        except (AttributeError, tk.TclError):
            math_frame.grid(row=0, column=0, sticky="nsew")
        
        # Генерируем задание если его нет
        if not math_current_task:
            generate_new_math_task()
        update_math_progress_display()
    
    current_mode = "math"

def show_mode(mode):
    """Показывает выбранный режим и скрывает меню"""
    global current_mode
    
    # Скрываем главное меню
    if menu_frame:
        try:
            menu_frame.grid_info()
            menu_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Скрываем подменю стихов если открыто
    if poems_submenu_frame:
        try:
            poems_submenu_frame.grid_info()
            poems_submenu_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Скрываем математический тренажёр если открыт
    if 'math_frame' in globals() and math_frame:
        try:
            math_frame.grid_info()
            math_frame.grid_remove()
        except (AttributeError, tk.TclError):
            pass
    
    # Показываем notebook с выбранным режимом
    try:
        notebook.grid_info()
        notebook.grid(row=1, column=0, pady=20, sticky="nsew")
    except (AttributeError, tk.TclError):
        notebook.grid(row=1, column=0, pady=20, sticky="nsew")
    
    # Переключаемся на нужную вкладку
    if mode == "main":
        notebook.select(0)
    elif mode == "lines":
        notebook.select(1)
    elif mode == "paragraphs":
        notebook.select(2)
    elif mode == "settings":
        notebook.select(3)
    
    current_mode = mode

# Интерфейс
notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, pady=20, sticky="nsew")
notebook.grid_remove()  # Скрываем notebook при запуске, показывается только при выборе режима

# Вкладка "Главная"
frame_main = tk.Frame(notebook, bg=bg_color)
notebook.add(frame_main, text=translations[language]["tab_main"])

# Кнопка "Назад в меню" для режима "Главная"
back_main_button_img = create_rounded_button_image(150, 40, button_radius, button_color, bg_color)
back_main_button = tk.Button(frame_main, image=back_main_button_img, text=translations[language]["back_to_menu"], 
                            compound="center", command=show_main_menu,
                            fg=text_color, font=("Courier New", 14), borderwidth=0, bg=bg_color, activebackground=bg_color)
back_main_button.image = back_main_button_img
back_main_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

sample_text_frame = tk.Frame(frame_main)
sample_text_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
sample_text = tk.Text(sample_text_frame, wrap="word", height=20, width=40, font=("Courier New", font_size), 
                      bg=text_bg_color, fg=text_color, exportselection=0)
sample_text.pack(side="left", fill="both", expand=True)
sample_text.config(state="disabled")

# Привязка событий для предотвращения выделения
sample_text.bind("<Button-1>", lambda e: prevent_selection(e, sample_text))
sample_text.bind("<B1-Motion>", lambda e: prevent_selection(e, sample_text))
sample_text.bind("<Control-a>", lambda e: prevent_selection(e, sample_text))
sample_text.bind("<Shift-Left>", lambda e: prevent_selection(e, sample_text))
sample_text.bind("<Shift-Right>", lambda e: prevent_selection(e, sample_text))
sample_text.bind("<Shift-Up>", lambda e: prevent_selection(e, sample_text))
sample_text.bind("<Shift-Down>", lambda e: prevent_selection(e, sample_text))

sample_scrollbar = tk.Scrollbar(sample_text_frame, orient="vertical", command=sample_text.yview)
sample_scrollbar.pack(side="right", fill="y")
sample_text.config(yscrollcommand=sample_scrollbar.set)

right_frame = tk.Frame(frame_main, bg=bg_color)
right_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

text_widget = tk.Text(right_frame, width=40, height=20, font=("Courier New", font_size), bg=text_bg_color, fg=text_color)
text_widget.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")

status_label = tk.Label(right_frame, text=translations[language]["status_main"], font=("Courier New", 20), bg=bg_color, fg=text_color)
status_label.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")

error_label = tk.Label(right_frame, text=translations[language]["errors"].format(error_count), font=("Courier New", 16), bg=bg_color, fg=text_color)
error_label.grid(row=2, column=0, padx=0, pady=5, sticky="nsew")

check_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
check_button = tk.Button(right_frame, image=check_button_img, text=translations[language]["check"], compound="center", 
                         command=check_input, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
check_button.image = check_button_img
check_button.grid(row=3, column=0, pady=10, sticky="ew")

reset_button_img = create_rounded_button_image(reset_button_width, button_height, button_radius, button_color, bg_color)
reset_button = tk.Button(right_frame, image=reset_button_img, text=translations[language]["reset"], compound="center", 
                         command=reset, state=tk.DISABLED, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
reset_button.image = reset_button_img
reset_button.grid(row=4, column=0, pady=10, sticky="ew")

frame_main.grid_rowconfigure(1, weight=1)
frame_main.grid_columnconfigure(0, weight=1)
frame_main.grid_columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=3)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Вкладка "По строкам"
line_frame = tk.Frame(notebook, bg=bg_color)
notebook.add(line_frame, text=translations[language]["tab_lines"])

# Кнопка "Назад в меню" для режима "По строкам"
back_lines_button_img = create_rounded_button_image(150, 40, button_radius, button_color, bg_color)
back_lines_button = tk.Button(line_frame, image=back_lines_button_img, text=translations[language]["back_to_menu"], 
                             compound="center", command=show_main_menu,
                             fg=text_color, font=("Courier New", 14), borderwidth=0, bg=bg_color, activebackground=bg_color)
back_lines_button.image = back_lines_button_img
back_lines_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

line_sample_text_frame = tk.Frame(line_frame)
line_sample_text_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
line_sample_text = tk.Text(line_sample_text_frame, wrap="word", height=20, width=40, font=("Courier New", font_size), 
                           bg=text_bg_color, fg=text_color, exportselection=0)
line_sample_text.pack(side="left", fill="both", expand=True)
line_sample_text.config(state="disabled")

# Привязка событий для предотвращения выделения
line_sample_text.bind("<Button-1>", lambda e: prevent_selection(e, line_sample_text))
line_sample_text.bind("<B1-Motion>", lambda e: prevent_selection(e, line_sample_text))
line_sample_text.bind("<Control-a>", lambda e: prevent_selection(e, line_sample_text))
line_sample_text.bind("<Shift-Left>", lambda e: prevent_selection(e, line_sample_text))
line_sample_text.bind("<Shift-Right>", lambda e: prevent_selection(e, line_sample_text))
line_sample_text.bind("<Shift-Up>", lambda e: prevent_selection(e, line_sample_text))
line_sample_text.bind("<Shift-Down>", lambda e: prevent_selection(e, line_sample_text))

line_sample_scrollbar = tk.Scrollbar(line_sample_text_frame, orient="vertical", command=line_sample_text.yview)
line_sample_scrollbar.pack(side="right", fill="y")
line_sample_text.config(yscrollcommand=line_sample_scrollbar.set)

line_right_frame = tk.Frame(line_frame, bg=bg_color)
line_right_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

line_text_widget = tk.Text(line_right_frame, width=40, height=20, font=("Courier New", font_size), bg=text_bg_color, fg=text_color)
line_text_widget.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")

line_status_label = tk.Label(line_right_frame, text=" ", font=("Courier New", 20), bg=bg_color, fg=text_color)
line_status_label.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")

line_error_label = tk.Label(line_right_frame, text=translations[language]["errors"].format(error_count), font=("Courier New", 16), bg=bg_color, fg=text_color)
line_error_label.grid(row=2, column=0, padx=0, pady=5, sticky="nsew")

line_check_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
line_check_button = tk.Button(line_right_frame, image=line_check_button_img, text=translations[language]["check"], compound="center", 
                              command=check_line, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
line_check_button.image = line_check_button_img
line_check_button.grid(row=3, column=0, pady=10, sticky="ew")

line_reset_button_img = create_rounded_button_image(reset_button_width, button_height, button_radius, button_color, bg_color)
line_reset_button = tk.Button(line_right_frame, image=line_reset_button_img, text=translations[language]["reset"], compound="center", 
                              command=reset_lines, state=tk.DISABLED, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
line_reset_button.image = line_reset_button_img
line_reset_button.grid(row=4, column=0, pady=10, sticky="ew")

line_frame.grid_rowconfigure(1, weight=1)
line_frame.grid_columnconfigure(0, weight=1)
line_frame.grid_columnconfigure(1, weight=1)
line_right_frame.grid_rowconfigure(0, weight=3)
line_right_frame.grid_rowconfigure(1, weight=1)
line_right_frame.grid_columnconfigure(0, weight=1)

# Вкладка "По абзацам"
quatrain_frame = tk.Frame(notebook, bg=bg_color)
notebook.add(quatrain_frame, text=translations[language]["tab_paragraphs"])

# Кнопка "Назад в меню" для режима "По абзацам"
back_quatrain_button_img = create_rounded_button_image(150, 40, button_radius, button_color, bg_color)
back_quatrain_button = tk.Button(quatrain_frame, image=back_quatrain_button_img, text=translations[language]["back_to_menu"], 
                                 compound="center", command=show_main_menu,
                                 fg=text_color, font=("Courier New", 14), borderwidth=0, bg=bg_color, activebackground=bg_color)
back_quatrain_button.image = back_quatrain_button_img
back_quatrain_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

quatrain_sample_text_frame = tk.Frame(quatrain_frame)
quatrain_sample_text_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
quatrain_sample_text = tk.Text(quatrain_sample_text_frame, wrap="word", height=20, width=40, font=("Courier New", font_size), 
                               bg=text_bg_color, fg=text_color, exportselection=0)
quatrain_sample_text.pack(side="left", fill="both", expand=True)
quatrain_sample_text.config(state="disabled")

# Привязка событий для предотвращения выделения
quatrain_sample_text.bind("<Button-1>", lambda e: prevent_selection(e, quatrain_sample_text))
quatrain_sample_text.bind("<B1-Motion>", lambda e: prevent_selection(e, quatrain_sample_text))
quatrain_sample_text.bind("<Control-a>", lambda e: prevent_selection(e, quatrain_sample_text))
quatrain_sample_text.bind("<Shift-Left>", lambda e: prevent_selection(e, quatrain_sample_text))
quatrain_sample_text.bind("<Shift-Right>", lambda e: prevent_selection(e, quatrain_sample_text))
quatrain_sample_text.bind("<Shift-Up>", lambda e: prevent_selection(e, quatrain_sample_text))
quatrain_sample_text.bind("<Shift-Down>", lambda e: prevent_selection(e, quatrain_sample_text))

quatrain_sample_scrollbar = tk.Scrollbar(quatrain_sample_text_frame, orient="vertical", command=quatrain_sample_text.yview)
quatrain_sample_scrollbar.pack(side="right", fill="y")
quatrain_sample_text.config(yscrollcommand=quatrain_sample_scrollbar.set)

quatrain_right_frame = tk.Frame(quatrain_frame, bg=bg_color)
quatrain_right_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

quatrain_text_widget = tk.Text(quatrain_right_frame, width=40, height=20, font=("Courier New", font_size), bg=text_bg_color, fg=text_color)
quatrain_text_widget.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")

quatrain_status_label = tk.Label(quatrain_right_frame, text=" ", font=("Courier New", 20), bg=bg_color, fg=text_color)
quatrain_status_label.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")

quatrain_error_label = tk.Label(quatrain_right_frame, text=translations[language]["errors"].format(error_count), font=("Courier New", 16), bg=bg_color, fg=text_color)
quatrain_error_label.grid(row=2, column=0, padx=0, pady=5, sticky="nsew")

quatrain_check_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
quatrain_check_button = tk.Button(quatrain_right_frame, image=quatrain_check_button_img, text=translations[language]["check"], compound="center", 
                                  command=check_quatrain, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
quatrain_check_button.image = quatrain_check_button_img
quatrain_check_button.grid(row=3, column=0, pady=10, sticky="ew")

quatrain_reset_button_img = create_rounded_button_image(reset_button_width, button_height, button_radius, button_color, bg_color)
quatrain_reset_button = tk.Button(quatrain_right_frame, image=quatrain_reset_button_img, text=translations[language]["reset"], compound="center", 
                                  command=reset_quatrains, state=tk.DISABLED, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
quatrain_reset_button.image = quatrain_reset_button_img
quatrain_reset_button.grid(row=4, column=0, pady=10, sticky="ew")

quatrain_frame.grid_rowconfigure(1, weight=1)
quatrain_frame.grid_columnconfigure(0, weight=1)
quatrain_frame.grid_columnconfigure(1, weight=1)
quatrain_right_frame.grid_rowconfigure(0, weight=3)
quatrain_right_frame.grid_rowconfigure(1, weight=1)
quatrain_right_frame.grid_columnconfigure(0, weight=1)

# Вкладка "Параметры"
frame_settings = tk.Frame(notebook, bg=bg_color)
notebook.add(frame_settings, text=translations[language]["tab_settings"])

# Кнопка "Назад в меню" для режима "Параметры"
back_settings_button_img = create_rounded_button_image(150, 40, button_radius, button_color, bg_color)
back_settings_button = tk.Button(frame_settings, image=back_settings_button_img, text=translations[language]["back_to_menu"], 
                                compound="center", command=show_main_menu,
                                fg=text_color, font=("Courier New", 14), borderwidth=0, bg=bg_color, activebackground=bg_color)
back_settings_button.image = back_settings_button_img
back_settings_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

settings_canvas = tk.Canvas(frame_settings, bg=bg_color)
settings_scrollbar = ttk.Scrollbar(frame_settings, orient="vertical", command=settings_canvas.yview)
settings_canvas.configure(yscrollcommand=settings_scrollbar.set)

settings_frame = tk.Frame(settings_canvas, bg=bg_color)
settings_canvas.create_window((0, 0), window=settings_frame, anchor="nw")

case_check = tk.Checkbutton(settings_frame, text=translations[language]["case_sensitive"], font=("Courier New", 16), 
                            variable=case_var, command=update_case_sensitivity, bg=bg_color, fg=text_color)
case_check.grid(row=0, column=0, pady=10, sticky="w")

punct_check = tk.Checkbutton(settings_frame, text=translations[language]["punct_sensitive"], font=("Courier New", 16), 
                             variable=punct_var, command=update_punctuation_sensitivity, bg=bg_color, fg=text_color)
punct_check.grid(row=1, column=0, pady=10, sticky="w")

font_label = tk.Label(settings_frame, text=translations[language]["font_size"], font=("Courier New", 16), bg=bg_color, fg=text_color)
font_label.grid(row=3, column=0, pady=10, sticky="w")

font_entry = tk.Entry(settings_frame, width=5, font=("Courier New", 16))
font_entry.grid(row=3, column=0, padx=(250, 0), pady=10, sticky="w")
font_entry.insert(0, "18")
font_entry.bind("<FocusOut>", lambda e: update_font_size())

auto_clear_check = tk.Checkbutton(settings_frame, text=translations[language]["auto_clear"], font=("Courier New", 16), 
                                  variable=auto_clear_var, command=update_auto_clear, bg=bg_color, fg=text_color)
auto_clear_check.grid(row=4, column=0, pady=10, sticky="w")

theme_label = tk.Label(settings_frame, text=translations[language]["theme"], font=("Courier New", 16), bg=bg_color, fg=text_color)
theme_label.grid(row=5, column=0, pady=10, sticky="w")

theme_menu = ttk.OptionMenu(settings_frame, theme_var, "Светлая", "Светлая", "Тёмная", "Ретро", command=lambda e: update_theme())
theme_menu.grid(row=5, column=0, padx=(250, 0), pady=10, sticky="w")

language_label = tk.Label(settings_frame, text=translations[language]["language"], font=("Courier New", 16), bg=bg_color, fg=text_color)
language_label.grid(row=6, column=0, pady=10, sticky="w")

language_menu = ttk.OptionMenu(settings_frame, language_var, "Русский", "Русский", "English", command=lambda e: update_language())
language_menu.grid(row=6, column=0, padx=(250, 0), pady=10, sticky="w")

open_folder_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
open_folder_button = tk.Button(settings_frame, image=open_folder_button_img, text=translations[language]["open_folder"], compound="center", 
                               command=open_folder, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
open_folder_button.image = open_folder_button_img
open_folder_button.grid(row=8, column=0, pady=10, sticky="ew")

poem_selector_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
poem_selector_button = tk.Button(settings_frame, image=poem_selector_button_img, text=translations[language]["explore_poems"], compound="center", 
                                 command=open_poem_selector, fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
poem_selector_button.image = poem_selector_button_img
poem_selector_button.grid(row=9, column=0, pady=10, sticky="ew")
create_tooltip(poem_selector_button, "Исследовать стихи в Бете. Пока что берутся лишь стихи с главной страницы stihi.ru, поиска нет. Там исключительно новые современные стихи.")

# Разделитель
separator1 = tk.Frame(settings_frame, height=2, bg=text_color)
separator1.grid(row=10, column=0, sticky="ew", pady=20)

# Заголовок раздела "Настройки математики"
math_settings_title = tk.Label(settings_frame, text=translations[language]["math_settings_title"], 
                               font=("Courier New", 20, "bold"), bg=bg_color, fg=text_color)
math_settings_title.grid(row=11, column=0, pady=10, sticky="w")

# Операции
math_operations_label = tk.Label(settings_frame, text=translations[language]["math_operations"], 
                                font=("Courier New", 16), bg=bg_color, fg=text_color)
math_operations_label.grid(row=12, column=0, pady=10, sticky="w")

math_add_check = tk.Checkbutton(settings_frame, text=translations[language]["math_add"], 
                                variable=math_add_var, font=("Courier New", 16), 
                                bg=bg_color, fg=text_color, command=lambda: (update_math_operations(), save_settings()))
math_add_check.grid(row=13, column=0, pady=5, sticky="w")

math_subtract_check = tk.Checkbutton(settings_frame, text=translations[language]["math_subtract"], 
                                     variable=math_subtract_var, font=("Courier New", 16), 
                                     bg=bg_color, fg=text_color, command=lambda: (update_math_operations(), save_settings()))
math_subtract_check.grid(row=14, column=0, pady=5, sticky="w")

math_multiply_check = tk.Checkbutton(settings_frame, text=translations[language]["math_multiply"], 
                                     variable=math_multiply_var, font=("Courier New", 16), 
                                     bg=bg_color, fg=text_color, command=lambda: (update_math_operations(), save_settings()))
math_multiply_check.grid(row=15, column=0, pady=5, sticky="w")

math_divide_check = tk.Checkbutton(settings_frame, text=translations[language]["math_divide"], 
                                   variable=math_divide_var, font=("Courier New", 16), 
                                   bg=bg_color, fg=text_color, command=lambda: (update_math_operations(), save_settings()))
math_divide_check.grid(row=16, column=0, pady=5, sticky="w")

# Диапазоны чисел
math_range_easy_label = tk.Label(settings_frame, text=translations[language]["math_range_easy"], 
                                 font=("Courier New", 16), bg=bg_color, fg=text_color)
math_range_easy_label.grid(row=17, column=0, pady=10, sticky="w")

math_range_easy_entry = tk.Entry(settings_frame, width=20, font=("Courier New", 14))
math_range_easy_entry.grid(row=17, column=0, padx=(250, 0), pady=10, sticky="w")
math_range_easy_entry.insert(0, f"{math_difficulty_ranges['Лёгкий'][0]}-{math_difficulty_ranges['Лёгкий'][1]}")
math_range_easy_entry.bind("<FocusOut>", lambda e: (update_math_ranges(), save_settings()))

math_range_normal_label = tk.Label(settings_frame, text=translations[language]["math_range_normal"], 
                                   font=("Courier New", 16), bg=bg_color, fg=text_color)
math_range_normal_label.grid(row=18, column=0, pady=10, sticky="w")

math_range_normal_entry = tk.Entry(settings_frame, width=20, font=("Courier New", 14))
math_range_normal_entry.grid(row=18, column=0, padx=(250, 0), pady=10, sticky="w")
math_range_normal_entry.insert(0, f"{math_difficulty_ranges['Нормальный'][0]}-{math_difficulty_ranges['Нормальный'][1]}")
math_range_normal_entry.bind("<FocusOut>", lambda e: (update_math_ranges(), save_settings()))

math_range_hard_label = tk.Label(settings_frame, text=translations[language]["math_range_hard"], 
                                 font=("Courier New", 16), bg=bg_color, fg=text_color)
math_range_hard_label.grid(row=19, column=0, pady=10, sticky="w")

math_range_hard_entry = tk.Entry(settings_frame, width=20, font=("Courier New", 14))
math_range_hard_entry.grid(row=19, column=0, padx=(250, 0), pady=10, sticky="w")
math_range_hard_entry.insert(0, f"{math_difficulty_ranges['Сложный'][0]}-{math_difficulty_ranges['Сложный'][1]}")
math_range_hard_entry.bind("<FocusOut>", lambda e: (update_math_ranges(), save_settings()))

# Количество заданий для повышения уровня
math_tasks_per_level_label = tk.Label(settings_frame, text=translations[language]["math_tasks_per_level"], 
                                      font=("Courier New", 16), bg=bg_color, fg=text_color)
math_tasks_per_level_label.grid(row=20, column=0, pady=10, sticky="w")

math_tasks_per_level_entry = tk.Entry(settings_frame, width=5, font=("Courier New", 16))
math_tasks_per_level_entry.grid(row=20, column=0, padx=(250, 0), pady=10, sticky="w")
math_tasks_per_level_entry.insert(0, str(math_tasks_per_level))
math_tasks_per_level_entry.bind("<FocusOut>", lambda e: (update_math_tasks_per_level(), save_settings()))

MD_label = tk.Label(settings_frame, text=translations[language]["MD"], font=("Courier New", 13), bg=bg_color, fg=text_color)
MD_label.grid(row=21, column=0, padx=10, pady=20, sticky="ew")

settings_canvas.grid(row=1, column=0, sticky="nsew")
settings_scrollbar.grid(row=1, column=1, sticky="ns")
frame_settings.grid_rowconfigure(1, weight=1)
frame_settings.grid_columnconfigure(0, weight=1)

def configure_settings_scroll(event):
    settings_canvas.configure(scrollregion=settings_canvas.bbox("all"))
    settings_canvas.yview_moveto(0)

settings_frame.bind("<Configure>", configure_settings_scroll)
settings_canvas.bind("<MouseWheel>", lambda e: on_mouse_wheel(e, settings_canvas))

# Главное меню
menu_frame = tk.Frame(root, bg=bg_color)
menu_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)

# Заголовок в меню
menu_title_label = tk.Label(menu_frame, text=translations[language]["title"], font=("Courier New", 40), bg=bg_color, fg=text_color)
menu_title_label.pack(pady=50)

# Фрейм для кнопок режимов
menu_buttons_frame = tk.Frame(menu_frame, bg=bg_color)
menu_buttons_frame.pack(pady=30, padx=50)

# Кнопка "Стихи"
poems_mode_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
poems_mode_button = tk.Button(menu_buttons_frame, image=poems_mode_button_img, text=translations[language]["poems"], 
                             compound="center", command=show_poems_submenu,
                             fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
poems_mode_button.image = poems_mode_button_img
poems_mode_button.pack(pady=15, fill="x")

# Кнопка "Математика"
math_mode_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
math_mode_button = tk.Button(menu_buttons_frame, image=math_mode_button_img, text=translations[language]["mathematics"], 
                             compound="center", command=show_math_trainer,
                             fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
math_mode_button.image = math_mode_button_img
math_mode_button.pack(pady=15, fill="x")

# Кнопка "Параметры"
settings_mode_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
settings_mode_button = tk.Button(menu_buttons_frame, image=settings_mode_button_img, text=translations[language]["tab_settings"], 
                                compound="center", command=lambda: show_mode("settings"),
                                fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
settings_mode_button.image = settings_mode_button_img
settings_mode_button.pack(pady=15, fill="x")

# Подменю для стихов
poems_submenu_frame = tk.Frame(root, bg=bg_color)
poems_submenu_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
poems_submenu_frame.grid_remove()

# Заголовок в подменю стихов
poems_submenu_title_label = tk.Label(poems_submenu_frame, text=translations[language]["poems"], font=("Courier New", 40), bg=bg_color, fg=text_color)
poems_submenu_title_label.pack(pady=50)

# Фрейм для кнопок режимов стихов
poems_submenu_buttons_frame = tk.Frame(poems_submenu_frame, bg=bg_color)
poems_submenu_buttons_frame.pack(pady=30, padx=50)

# Кнопка "Главная" (режим стихов)
poems_main_mode_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
poems_main_mode_button = tk.Button(poems_submenu_buttons_frame, image=poems_main_mode_button_img, text=translations[language]["tab_main"], 
                                   compound="center", command=lambda: show_mode("main"),
                                   fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
poems_main_mode_button.image = poems_main_mode_button_img
poems_main_mode_button.pack(pady=15, fill="x")

# Кнопка "По строкам"
poems_lines_mode_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
poems_lines_mode_button = tk.Button(poems_submenu_buttons_frame, image=poems_lines_mode_button_img, text=translations[language]["tab_lines"], 
                                     compound="center", command=lambda: show_mode("lines"),
                                     fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
poems_lines_mode_button.image = poems_lines_mode_button_img
poems_lines_mode_button.pack(pady=15, fill="x")

# Кнопка "По абзацам"
poems_paragraphs_mode_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
poems_paragraphs_mode_button = tk.Button(poems_submenu_buttons_frame, image=poems_paragraphs_mode_button_img, text=translations[language]["tab_paragraphs"], 
                                          compound="center", command=lambda: show_mode("paragraphs"),
                                          fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
poems_paragraphs_mode_button.image = poems_paragraphs_mode_button_img
poems_paragraphs_mode_button.pack(pady=15, fill="x")

# Кнопка "Назад в меню" для подменю стихов
poems_back_button_img = create_rounded_button_image(settings_button_width, button_height, button_radius, button_color, bg_color)
poems_back_button = tk.Button(poems_submenu_buttons_frame, image=poems_back_button_img, text=translations[language]["back_to_menu"], 
                              compound="center", command=show_main_menu,
                              fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
poems_back_button.image = poems_back_button_img
poems_back_button.pack(pady=15, fill="x")

# Интерфейс математического тренажёра
math_frame = tk.Frame(root, bg=bg_color)
math_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
math_frame.grid_remove()

# Кнопка "Назад в меню" для математического тренажёра
math_back_button_img = create_rounded_button_image(150, 40, button_radius, button_color, bg_color)
math_back_button = tk.Button(math_frame, image=math_back_button_img, text=translations[language]["back_to_menu"], 
                            compound="center", command=show_main_menu,
                            fg=text_color, font=("Courier New", 14), borderwidth=0, bg=bg_color, activebackground=bg_color)
math_back_button.image = math_back_button_img
math_back_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

# Левая часть - информация о прогрессе
math_left_frame = tk.Frame(math_frame, bg=bg_color)
math_left_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

math_level_label = tk.Label(math_left_frame, text=translations[language]["math_level"].format(math_level), 
                           font=("Courier New", 24), bg=bg_color, fg=text_color)
math_level_label.pack(pady=20)

math_points_label = tk.Label(math_left_frame, text=translations[language]["math_points"].format(math_points), 
                            font=("Courier New", 24), bg=bg_color, fg=text_color)
math_points_label.pack(pady=20)

math_progress_label = tk.Label(math_left_frame, text=translations[language]["math_progress"].format(math_tasks_completed, math_tasks_per_level), 
                              font=("Courier New", 20), bg=bg_color, fg=text_color)
math_progress_label.pack(pady=20)

# Выбор сложности
math_difficulty_label = tk.Label(math_left_frame, text=translations[language]["math_difficulty"], 
                                font=("Courier New", 18), bg=bg_color, fg=text_color)
math_difficulty_label.pack(pady=10)

math_difficulty_frame = tk.Frame(math_left_frame, bg=bg_color)
math_difficulty_frame.pack(pady=10)

math_easy_radio = tk.Radiobutton(math_difficulty_frame, text=translations[language]["math_easy"], 
                                 variable=math_difficulty_var, value="Лёгкий", 
                                 command=update_math_difficulty, font=("Courier New", 16), 
                                 bg=bg_color, fg=text_color, selectcolor=bg_color)
math_easy_radio.pack(anchor="w", pady=5)

math_normal_radio = tk.Radiobutton(math_difficulty_frame, text=translations[language]["math_normal"], 
                                   variable=math_difficulty_var, value="Нормальный", 
                                   command=update_math_difficulty, font=("Courier New", 16), 
                                   bg=bg_color, fg=text_color, selectcolor=bg_color)
math_normal_radio.pack(anchor="w", pady=5)

math_hard_radio = tk.Radiobutton(math_difficulty_frame, text=translations[language]["math_hard"], 
                                 variable=math_difficulty_var, value="Сложный", 
                                 command=update_math_difficulty, font=("Courier New", 16), 
                                 bg=bg_color, fg=text_color, selectcolor=bg_color)
math_hard_radio.pack(anchor="w", pady=5)

# Правая часть - задание и ввод
math_right_frame = tk.Frame(math_frame, bg=bg_color)
math_right_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

math_task_label = tk.Label(math_right_frame, text=translations[language]["math_task"], 
                          font=("Courier New", 32), bg=bg_color, fg=text_color)
math_task_label.pack(pady=30)

math_answer_entry = tk.Entry(math_right_frame, font=("Courier New", 32), width=15, justify="center")
math_answer_entry.pack(pady=30)
math_answer_entry.bind("<Return>", lambda e: check_math_answer())

math_status_label = tk.Label(math_right_frame, text="", font=("Courier New", 20), bg=bg_color, fg=text_color)
math_status_label.pack(pady=20)

math_check_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
math_check_button = tk.Button(math_right_frame, image=math_check_button_img, text=translations[language]["math_check"], 
                             compound="center", command=check_math_answer,
                             fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
math_check_button.image = math_check_button_img
math_check_button.pack(pady=20)

math_new_task_button_img = create_rounded_button_image(button_width, button_height, button_radius, button_color, bg_color)
math_new_task_button = tk.Button(math_right_frame, image=math_new_task_button_img, text=translations[language]["math_new_task"], 
                                compound="center", command=generate_new_math_task,
                                fg=text_color, font=("Courier New", 24), borderwidth=0, bg=bg_color, activebackground=bg_color)
math_new_task_button.image = math_new_task_button_img
math_new_task_button.pack(pady=20)

math_frame.grid_rowconfigure(1, weight=1)
math_frame.grid_columnconfigure(0, weight=1)
math_frame.grid_columnconfigure(1, weight=2)

# Инициализация программы
load_settings()
load_text_from_file()

# Показываем главное меню при запуске
show_main_menu()

# Основной цикл
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.mainloop()
