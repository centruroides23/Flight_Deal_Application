import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Flight Deal Application")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=2)



if __name__ == "__main__":
    app = App()
    app.mainloop()