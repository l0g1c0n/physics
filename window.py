
import tkinter as tk

class TextRendererApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Renderer")
        self.text_frame = tk.Text(root, width=200, height=60)
        self.text_frame.pack()



        self.text_frame.configure(foreground='white', background='black')
    def update_text_frame(self, text):
        self.text_frame.delete("1.0", "end")
        self.text_frame.insert("1.0", text)
        self.root.update()





def render_text_frame(function):
    frame_count = 0
    text_renderer = TextRendererApp(tk.Tk())

    while True:
        # Generate the text frame based on your logic
        text_frame = generate_text_frame(function)

        # Update the text frame in the app window
        text_renderer.update_text_frame(text_frame)

        # Increment frame count
        frame_count += 1

def generate_text_frame(function):
    # Generate the text frame based on the frame count or any other logic
    text_frame = function()
    return text_frame


def Runtime(func):
    def wrapper():
        render_text_frame(func)
    wrapper()
