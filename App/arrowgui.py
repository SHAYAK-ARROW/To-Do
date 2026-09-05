import os
import queue as q
import threading as th
import tkinter as tk


window = None
output_box = None
input_box = None

_queue = q.Queue()
_CLEAR_SENTINEL = object()  # ekta bishesh "chinho" object, jeta clear()-er
                            # nirdesh bojhate use hobe, printf-er (text, color)
                            # tuple-er shathe kokhono gulie jabe na
terminal_ready = th.Event()
input_ready = th.Event()
_last_input = None


def creat_fake_terminal(terminal_bg="black", top_most=False):
    global window, output_box, input_box

    window = tk.Tk()
    window.title("ARROW TO-DO MANAGER")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = int(screen_width * 0.7)
    height = int(screen_height * 0.7)
    window.geometry(f"{width}x{height}")

    input_frame = tk.Frame(window, bg="black")
    input_frame.pack(side="bottom", fill="x")

    prompt_label = tk.Label(
        input_frame,
        text=">_ ",
        bg="black",
        fg="lime",
        font=("Consolas", 16),
    )
    prompt_label.pack(side="left")

    input_box = tk.Entry(
        input_frame,
        bg="black",
        fg="white",
        insertbackground="white",
        font=("Consolas", 16),
        bd=0,
        highlightthickness=0,
    )
    input_box.pack(side="left", fill="x", expand=True)

    output_box = tk.Text(
        window,
        bg=terminal_bg,
        fg="white",
        font=("Consolas", 18)
    )
    output_box.pack(fill="both", expand=True)

    def enter(event):
        global _last_input

        user_text = input_box.get()
        output_box.insert("end", f">_: {user_text}\n")
        output_box.see("end")
        input_box.delete(0, "end")
        _last_input = user_text
        input_ready.set()

    def process_queue():
        # ekbare queue-te je koyta item jomeche, shobgulo ekhon-i drain
        # kore fela hoy -- age shudhu 1-ta item processed hoto protibar,
        # tate onek printf() ekjaygay call hole output dekhate deri hoto
        try:
            while True:
                item = _queue.get_nowait()

                if item is _CLEAR_SENTINEL:
                    # eta clear()-er nirdesh, ekhon printf-er shathe
                    # SHOMOI queue-te thakay, order shobshomoy thik thakbe
                    output_box.delete("1.0", "end")
                else:
                    text, color = item
                    output_box.tag_configure(color, foreground=color)
                    output_box.insert("end", text, color)
                    output_box.see("end")
        except q.Empty:
            pass

        window.after(100, process_queue)

    def on_close():
        window.destroy()
        os._exit(0)

    input_box.bind("<Return>", enter)
    terminal_ready.set()
    window.after(100, process_queue)
    window.protocol("WM_DELETE_WINDOW", on_close)

    window.configure(bg=terminal_bg)
    window.mainloop()


def start_terminal(terminal_bg="black"):
    terminal_thread = th.Thread(
        target=creat_fake_terminal,
        args=(terminal_bg,),
        daemon=True
    )
    terminal_thread.start()
    terminal_ready.wait()


def clear():
    # sorasori output_box touch na kore, ekhon _queue-teই ekta special
    # marker pathano hoy -- eivabe printf()-er shathe order-e conflict hoy na
    _queue.put(_CLEAR_SENTINEL)


def printf(*args, sep=" ", end="\n", color="white"):
    text_put = sep.join(str(arg) for arg in args)
    _queue.put((text_put + end, color))


def scanf(prompt="", color="white"):
    if prompt:
        printf(prompt, color=color)

    input_ready.clear()
    input_ready.wait()
    return _last_input