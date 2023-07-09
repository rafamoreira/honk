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
        self.message = None
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
        self.message = honk_dict['clown']
        image = Image.open(self.image_path)
        for frame in ImageSequence.Iterator(image):
            self.frames.append(ImageTk.PhotoImage(frame))


class Main:
    """
    Main Class
    """

    def __init__(self):
        self.message_label = None
        self.current_frame = 0
        self.gif_label = None
        self.window = tkinter.Tk()
        self.current_honk = None
        self.current_honk_index = 0
        self.honks = []

    def start(self):
        """
        Start the app
        """
        self.window.title("Honk")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.window.bind('<n>', self.next_honk)
        self.gif_label = tkinter.Label(self.window)
        self.gif_label.pack(fill="both", expand=True, side="top")
        self.message_label = tkinter.Label(self.window)
        self.message_label.pack(fill="both", expand=True, side="bottom")
        self.next_honk(first=True)
        self.show_honks()
        self.window.mainloop()

    def ingest_honks(self, honks):
        """
        Ingest honks
        """

        honk_ids = [honk.id for honk in self.honks]

        for honk in honks:
            if honk['id'] not in honk_ids:
                self.honks.append(Honk(honk))

    def show_honks(self) -> None:
        """
        Show honks
        this ended up being a kitchen sink render function, it probably should
        be refactored into smaller functions. Specifically the part where it
        checks if the honk is a string or an image, or split the rendering
        images and strings into different functions.
        The problem is the desktop paradigm, where you have to render that
        I have no idea how to solve that using a single callback from the
        mainloop.
        """
        # try:
        #     honk = self.honks[self.current_honk]
        # except IndexError:
        #     honk = "End of honks for now!"
        #
        # if isinstance(honk, str):
        #     # If the label is different from the honk, destroy it and create a
        #     # new one with the honk text, this is done to clear the label only
        #     # when necessary, otherwise the label will be cleared every time
        #     # the loop runs flickering the screen.
        #     if self.gif_label.config('text')[-1] != honk:
        #         self.gif_label.destroy()
        #         self.gif_label = tkinter.Label(self.window)
        #
        #     self.gif_label.config(text=honk)
        #     self.gif_label.pack(fill="both", expand=True)
        # else:
        #     # If the label is not empty, destroy it and create a new one
        #     # this happens when a new honk is loaded after the initial loop.
        #     if self.gif_label.config('text')[-1] != "":
        #         self.gif_label.destroy()
        #         self.gif_label = tkinter.Label(self.window)
        #         self.gif_label.pack(fill="both", expand=True)
        if self.current_honk is None:
            self.gif_label.destroy()
            self.gif_label = tkinter.Label(self.window)
            self.gif_label.pack(fill="both", expand=True, side="top")
            self.message_label.config(text="End of honks for now!")
            return self.window.after(50, self.show_honks)

        if self.current_frame >= len(self.current_honk.frames):
            self.current_frame = 0

        self.gif_label.config(
            image=self.current_honk.frames[self.current_frame],
        )
        self.message_label.config(text=self.current_honk.message)

        self.current_frame += 1
        self.window.after(50, self.show_honks)

    def next_honk(self, _=None, first=False):
        """
        Next honk
        """
        if first:
            self.current_honk = self.honks[self.current_honk_index]
            return

        if self.current_honk_index + 1 >= len(self.honks):
            self.current_honk = None
            return

        self.current_honk_index += 1
        self.current_honk = self.honks[self.current_honk_index]


def api_thread(api: Api):
    """
    api_thread function
    runs in the background, every 30 seconds. Fetches honks from the API.
    :param api: Api.
    """
    print('api_thread started')
    api.fetch_honks()
    main.ingest_honks(api.honks.values())
    print('api_thread finished')
    thread = threading.Timer(30, api_thread, args=[api])
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    main = Main()
    config_singleton: Config = Config()
    file_cache_singleton = FileCache(config_singleton)
    api_singleton: Api = Api(
        config_singleton.api_credentials,
        file_cache_singleton,
    )
    api_thread(api_singleton)
    main.start()
    print('after mainloop')
