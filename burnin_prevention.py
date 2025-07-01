import time
import threading
import argparse
import tkinter as tk
from pynput import mouse, keyboard
from threading import Timer

# Default inactivity timeout
DEFAULT_TIMEOUT = 300  # 5 minutes
# DEFAULT_TIMEOUT = 600 # 10 minutes


import time
import threading
import tkinter as tk
from pynput import mouse, keyboard
import ctypes

DEFAULT_TIMEOUT = 300  # 5 minutes

import time
import threading
import tkinter as tk
from pynput import mouse, keyboard
import ctypes

DEFAULT_TIMEOUT = 300  # 5 minutes

class BurnInPrevention:
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.fade_duration = 0.5  # seconds
        self.last_input_time = time.time()
        self.running = False
        self.overlay_active = False
        self.fade_job = None
        self.fading = False

    def _show_start_popup(self):
        ctypes.windll.user32.MessageBoxW(0, "Burn-In Prevention is now active.", "Burn-In Prevention", 0x40)

    def _show_black_overlay(self):
        print("[INFO] Launching black screen overlay...")
        self.overlay_active = True
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.config(cursor="none")
        self.root.attributes("-alpha", 0.0)

        # Message label
        self.message_label = tk.Label(
            self.root,
            text="Starting Burn-In Prevention",
            font=("Helvetica", 32),
            fg="white",
            bg="black"
        )
        self.message_label.pack(expand=True)
        self.root.after(2000, self._hide_message)

        self.root.bind("<Motion>", self._exit_overlay)
        self.root.bind("<Key>", self._exit_overlay)
        self.root.bind("<Button>", self._exit_overlay)

        self._fade_in()
        self.root.mainloop()

    def _hide_message(self):
        if hasattr(self, 'message_label'):
            self.message_label.destroy()

    def _fade_in(self):
        self._cancel_fade()
        self.fading = True
        total_steps = int(self.fade_duration * 1000 / 50)
        step = 1.0 / total_steps

        def do_fade():
            try:
                alpha = self.root.attributes("-alpha")
                if alpha < 1.0:
                    self.root.attributes("-alpha", min(alpha + step, 1.0))
                    self.fade_job = self.root.after(50, do_fade)
                else:
                    self.fading = False
                    self.fade_job = None
            except tk.TclError:
                self.fading = False
                self.fade_job = None

        do_fade()

    def _fade_out(self):
        self._cancel_fade()
        self.fading = True
        total_steps = int(self.fade_duration * 1000 / 50)
        step = 1.0 / total_steps

        def do_fade():
            try:
                alpha = self.root.attributes("-alpha")
                if alpha > 0.0:
                    self.root.attributes("-alpha", max(alpha - step, 0.0))
                    self.fade_job = self.root.after(50, do_fade)
                else:
                    self.fading = False
                    self.fade_job = None
                    self.root.destroy()
            except tk.TclError:
                self.fading = False
                self.fade_job = None

        do_fade()

    def _cancel_fade(self):
        if self.fade_job:
            try:
                self.root.after_cancel(self.fade_job)
            except Exception:
                pass
            self.fade_job = None
        self.fading = False

    def _exit_overlay(self, event=None):
        if self.overlay_active:
            print("[INFO] Exiting overlay.")
            self.overlay_active = False
            self._cancel_fade()
            self._fade_out()

    def _input_listener(self):
        def on_input(_):
            self.last_input_time = time.time()
        with mouse.Listener(on_move=on_input, on_click=on_input, on_scroll=on_input), \
             keyboard.Listener(on_press=on_input, on_release=on_input):
            while self.running:
                time.sleep(1)

    def _monitor_loop(self):
        while self.running:
            idle_time = time.time() - self.last_input_time
            if idle_time >= self.timeout and not self.overlay_active:
                print(f"[INFO] Idle for {int(idle_time)}s — triggering overlay.")
                self._show_black_overlay()
            time.sleep(1)

    def start(self):
        if self.running:
            print("[WARN] Already running.")
            return
        print("[INFO] Starting burn-in prevention...")
        self._show_start_popup()
        self.running = True
        self.last_input_time = time.time()
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        threading.Thread(target=self._input_listener, daemon=True).start()

    def stop(self):
        print("[INFO] Stopping burn-in prevention...")
        self.running = False




def main():
    parser = argparse.ArgumentParser(description="OLED Burn-In Prevention Script")
    parser.add_argument('--enable', action='store_true', help="Start burn-in prevention")
    parser.add_argument('--disable', action='store_true', help="Stop burn-in prevention")
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help="Inactivity timeout in seconds")

    args = parser.parse_args()
    burnin = BurnInPrevention(timeout=args.timeout)

    # 👇 Fix: Only auto-enable if neither flag is passed
    if not args.enable and not args.disable:
        args.enable = True

    if args.enable:
        burnin.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            burnin.stop()
    elif args.disable:
        burnin.stop()
    else:
        print("Use --enable to start or --disable to stop.")



if __name__ == "__main__":
    main()
