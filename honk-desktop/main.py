"""
Honk desktop app
"""
import io
import threading
import tkinter

from PIL import Image, ImageTk, ImageSequence

from utils import Api, Config, FileCache


class Honk:
    """
    Honk class
    """

    def __init__(self, honk_dict):
        self.id = None
        self.clown_url = None
        self.created_at = None
        self.image_path = None
        self.frames = []
        self.extract_params(honk_dict)

    def extract_params(self, honk_dict):
        """
        Extract params from the honk dict
        """

        self.id = honk_dict['id']
        self.clown_url = honk_dict['clown_url']
        self.created_at = honk_dict['created_at']
        self.image_path = honk_dict['image_path']
        image = Image.open(self.image_path)
        for frame in ImageSequence.Iterator(image):
            self.frames.append(ImageTk.PhotoImage(frame))


class Main:
    """
    Main Class
    """

    def __init__(self):
        self.gif_label = None
        self.window = tkinter.Tk()
        self.current_honk = None
        self.honks = [
            'lol1',
            'lol2',
            'lol3',
        ]

    def start(self):
        """
        Start the app
        """
        self.window.title("Honk")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.display_new_honk()
        self.window.bind('<n>', self.display_new_honk)
        self.window.mainloop()

    def show_honks(self, initial_run=False) -> None:
        self.gif_label = tkinter.Label(self.window, text=self.honks.pop())
        self.gif_label.pack()

    def display_new_honk(self, event=None) -> None:
        if self.gif_label:
            self.gif_label.destroy()

        try:
            label = self.honks.pop()
        except IndexError:
            label = "End of honks for now!"

        self.gif_label = tkinter.Label(self.window, text=label)
        self.gif_label.pack()
        self.window.after(1000, self.display_new_honk)

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
    main = Main()
    main.start()
    print('after mainloop')
