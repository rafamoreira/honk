"""
Honk desktop app
"""
import io
import json
import os
import queue
import tkinter
from tkinter import messagebox

import requests
from PIL import Image, ImageTk, ImageSequence

class Main:
    def __init__(self):
        self.frames = None
        self.image = None
        self.honks = {}
        self.honks_queue = queue.Queue()
        self.credentials = Credentials()
        self.api = Api(self.credentials)
        self.gif_label = None
        self.current_frame = 0
        self.window = tkinter.Tk()

    def start(self):
        """
        Start the app
        """
        self.window.title("Honk")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.get_honks_periodically(initial_run=True)
        self.window.bind('<n>', self.display_new_honk)
        self.window.mainloop()

    def get_honks_periodically(self, initial_run=False) -> None:
        """
        Get all honks periodically
        """
        honks = self.api.get_honks()
        if honks:
            self.process_honks(honks)
            if initial_run:
                self.display_new_honk(None)
        elif initial_run:
            messagebox.showinfo("Honk", "No honks to show :(", timeout=10000)
        self.window.after(30000, self.get_honks_periodically)  # Get honks every 1 second

    def process_honks(self, honks) -> None:
        """
        Add new honks to the honks queue
        """
        for honk in honks:
            if honk['id'] not in self.honks:
                self.honks[honk['id']] = honk
                self.honks_queue.put(honk)

    def display_new_honk(self, event):
        """
        Display a new honk when 'N' is pressed
        """
        if not self.honks_queue.empty():
            honk = self.honks_queue.get()
            self.load_gif_from_url(honk['clown_url'], honk['clown'], honk['id'])
        else:
            messagebox.showinfo("Honk", "No new honks available")

    def load_gif_from_url(self, url, message, honk_id) -> None:
        """
        Load gif from URL and save to local cache
        """
        cache_directory = get_or_create_directory('honk_cache')
        cache_file = f'{cache_directory}/{honk_id}.gif'

        # If the GIF is not in cache, download it
        if not os.path.exists(cache_file):
            response = requests.get(url)
            with open(cache_file, 'wb') as f:
                f.write(response.content)

        self.frames = []
        image = Image.open(cache_file)
        for frame in ImageSequence.Iterator(image):
            self.frames.append(ImageTk.PhotoImage(frame))

        if self.gif_label is None:
            self.gif_label = tkinter.Label(
                self.window,
                text=message,
                compound='bottom',
                font=("Arial", 20)
            )
            self.gif_label.pack(fill="both", expand="yes")
        else:
            self.gif_label.config(text=message)

        self.current_frame = 0
        self.update_image()

    def update_image(self):
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.gif_label.config(image=self.frames[self.current_frame])
        self.current_frame += 1
        self.window.after(30, self.update_image)


if __name__ == "__main__":
    Main().start()
