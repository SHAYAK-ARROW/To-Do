import queue as q
import threading as th
import tkinter as tk

window = None
output_box = None
input_box = None

_queue = q.Queue()
_clear_flag = th.Event()
terminal_ready = th.Event()
input_ready = th.Event()
_last_input = None


def creat_fake_terminal():
    global window, output_box, input_box

    window = tk.Tk()
    window.title("ARROW TO-DO MANAGER")

    scren_w = window.winfo_screenwidth()
    scren_h = window.winfo_screenheight()

    w = int(scren_w * 0.7)
    h = int(scren_h * 0.7)
    window.geometry(f"{w}x{h}")

    input_frame = tk.Frame(window, bg="black")
    input_frame.pack(side="bottom", fill="x")

    prompt_label = tk.Label(input_frame, text=">_ ", bg="black", fg="lime", font=("Consolas", 16))
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

    output_box = tk.Text(window, bg="black", fg="white", font=("Consolas", 18))
    output_box.pack(fill="both", expand=True)

    def enter(event):
        user_text = input_box.get()
        output_box.insert("end", f">_: {user_text}\n")
        output_box.see("end")
        input_box.delete(0, "end")

        global _last_input
        _last_input = user_text
        input_ready.set()

    def process_queue():
        try:
            text = _queue.get_nowait()
            output_box.insert("end", text)
            output_box.see("end")
        except q.Empty:
            pass

        if _clear_flag.is_set():
            output_box.delete("1.0", "end")
            _clear_flag.clear()

        window.after(100, process_queue)

    input_box.bind("<Return>", enter)
    terminal_ready.set()
    window.after(100, process_queue)
    window.mainloop()


def start_terminal():
    t = th.Thread(target=creat_fake_terminal, daemon=True)
    t.start()
    terminal_ready.wait()


def clear():
    _clear_flag.set()


def printf(*args, sep=" ", end="\n"):
    text = sep.join(str(a) for a in args)
    _queue.put(text + end)


def scanf(prompt=""):
    if prompt:
        printf(prompt)
    input_ready.clear()
    input_ready.wait()
    return _last_input