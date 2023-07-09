"""
Honk desktop app
"""
import io
import threading
import tkinter

from PIL import Image, ImageTk, ImageSequence

from utils import Api, Config, FileCache


class Main:
    """
    Main Class
    """

    def __init__(self):
        self.frames = None
        self.image = None
        self.honks = {}
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
        self.show_honks(initial_run=True)
        self.window.bind('<n>', self.display_new_honk)
        self.window.mainloop()

    def show_honks(self, initial_run=False) -> None:
        print(f'show honks called {initial_run}')

    def display_new_honk(self, event) -> None:
        print('Display new honk')

    def update_image(self):
        """
        Update the GIF image
        """
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.gif_label.config(image=self.frames[self.current_frame])
        self.window.after(
            int(1000 / 20), self.update_image
        )  # Change image every 100 ms

    def load_gif_from_url(self, url) -> None:
        """
        Load a GIF from a URL
        """
        self.image = Image.open(io.BytesIO(img_data))
        self.frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for
                       frame in ImageSequence.Iterator(self.image)]
        self.current_frame = 0

        # Displaying the GIF
        self.gif_label = tkinter.Label(self.window, image=self.frames[0])
        self.gif_label.pack()

        self.update_image()


def api_thread(api_singleton: Api):
    """
    api_thread function
    runs in the background, every 10 seconds. Fetches honks from the API.
    :param api_singleton: Api.
    """
    print('api_thread started')
    api_singleton.fetch_honks()
    print('api_thread finished')
    thread = threading.Timer(5, api_thread, args=[api_singleton])
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    config_singleton: Config = Config()
    file_cache_singleton = FileCache(config_singleton)
    api: Api = Api(config_singleton.api_credentials, file_cache_singleton)
    api_thread(api)
    Main().start()
