from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
DARK_GREEN = "#006400"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = int(60/10)
SHORT_BREAK_MIN = 5*60
LONG_BREAK_MIN = 20*60
work = True
no_of_sessions = 0
WORK_TEXT = "Work Time"
BREAK_TEXT = "Break Time"
timer = None
pause_count = 0
paused = True

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    heading_label.config(text="Timer", fg=DARK_GREEN)
    check_marks.config(text="")
    global no_of_sessions
    no_of_sessions = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    heading_label["text"] = WORK_TEXT
    countdown(WORK_MIN)


def pause_timer():
    global paused
    if paused:
        heading_label.config(text="Paused")
        window.after_cancel(timer)
        pause_btn.config(text="Continue")
        paused = False
    else:
        countdown(pause_count)
        pause_btn.config(text="Pause")
        paused = True
        if work:
            heading_label.config(text=WORK_TEXT)
        else:
            heading_label.config(text=BREAK_TEXT)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)
# window.minsize(height=300, width=550)

# heading
heading_label = Label()
heading_label.config(text="Timer", fg=DARK_GREEN, bg=YELLOW,
                     font=(FONT_NAME, 40, "bold"))
heading_label.grid(row=0, column=1)

# tomato image
canvas = Canvas(width=200, height=224, bg=YELLOW, bd=0, highlightthickness=0)
tomato_image = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white",
                                font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# start button

start_btn = Button(text="Start", bd=1, highlightthickness=0,
                   command=start_timer)
start_btn.grid(row=2, column=0)

# reset button
reset_btn = Button(text="Reset")
reset_btn.config(bd=1, highlightthickness=0, command=reset_timer)
reset_btn.grid(row=2, column=2)

# pause button
pause_btn = Button(text="Pause", bd=1, highlightthickness=0,
                   command=pause_timer)
pause_btn.grid(row=3, column=0)
# checkmark label
check_marks = Label(text="")
check_marks.config(fg=DARK_GREEN, bg=YELLOW, pady=10,
                   font=(FONT_NAME, 10))
check_marks.grid(row=2, column=1)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def change_session(count):
    global work
    global no_of_sessions
    # checks to see if the timer should show work session or break session time
    if count == 0:
        # checks if a work session or a break session was finished
        if work:
            no_of_sessions += 1
            show_check_mark(no_of_sessions)
            heading_label["text"] = BREAK_TEXT
            # checks for long or short break
            if no_of_sessions % 4 == 0:
                count = LONG_BREAK_MIN
                heading_label.config(fg=RED)
            else:
                count = SHORT_BREAK_MIN
                heading_label.config(fg=PINK)
            work = False
        else:
            heading_label.config(text=WORK_TEXT, fg=DARK_GREEN)
            count = WORK_MIN
            work = True
    return count


def countdown(count):
    count = change_session(count)
    global pause_count
    pause_count = count

    minutes = str(int(count/60))
    if int(minutes) < 10:
        minutes = "0" + minutes
    seconds = str(count % 60)
    if int(seconds) % 60 < 10:
        seconds = "0" + seconds

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count-1)


def show_check_mark(reps):
    check_marks_text = ''
    for i in range(reps):
        check_marks_text += "✔"
    check_marks["text"] = check_marks_text


window.mainloop()
