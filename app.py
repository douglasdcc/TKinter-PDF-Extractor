import tkinter as tk
from tkinter.filedialog import askopenfile

import PyPDF2
from PIL import Image, ImageDraw, ImageTk

from themes import THEMES  # Import the themes


class PDFApp:
    def __init__(self, root_):
        self.root = root_
        self.root.resizable(False, False)
        self.text_box = None
        self.browse_text = tk.StringVar()
        self.clear_button_text = tk.StringVar()
        self.current_theme = "light"
        self.scrollbar = None

        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the GUI, ensuring all widgets are properly placed and styled.
        """
        text_box_content = None
        if self.text_box is not None:
            try:
                text_box_content = self.text_box.get("1.0", "end-1c")
            except tk.TclError:
                self.text_box = None

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=THEMES[self.current_theme]["background"])

        self.canvas = tk.Canvas(
            self.root,
            width=600,
            height=300,
            bg=THEMES[self.current_theme]["background"],
        )
        self.canvas.grid(columnspan=3, rowspan=3)

        self.set_theme_button()
        self.set_logos("images/logo_nobg.png")
        self.setup_instructions()
        self.setup_buttons()
        self.add_bottom_margin()

        self.restore_text_box_and_scrollbar(text_box_content)

    def set_theme_button(self):
        """
        Creates a small "Toggle Theme" button and positions it in the top-right corner.
        """
        toggle_theme_button = tk.Button(
            self.root,
            text="🌓",
            command=self.toggle_theme,
            font="Raleway 10 bold",
            bg=THEMES[self.current_theme]["primary"],
            fg=THEMES[self.current_theme]["secondary"],
            activebackground=THEMES[self.current_theme]["button_active"],
            activeforeground=THEMES[self.current_theme]["secondary"],
            height=1,
            width=3,
        )
        toggle_theme_button.grid(column=1, row=0, sticky="ne", padx=10, pady=10)

    def set_logos(self, logo_path):
        """
        Sets the application logo and icon.
        """
        logo = Image.open(logo_path)

        app_icon_with_circle = self.create_app_icon(logo)
        self.root.iconphoto(False, app_icon_with_circle)

        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg=THEMES[self.current_theme]["background"])
        logo_label.image = logo
        logo_label.grid(column=1, row=1)

    def create_app_icon(self, image):
        """
        Creates a circular app icon from the given image.
        """
        icon_width, icon_height = image.size
        circle_size = (icon_width + 20, icon_height + 20)
        circle_image = Image.new("RGBA", circle_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(circle_image)
        draw.ellipse((0, 0, circle_size[0], circle_size[1]), fill=(255, 255, 255, 255))

        circle_image.paste(image, (10, 10), image)

        return ImageTk.PhotoImage(circle_image)

    def setup_instructions(self):
        """
        Adds instructions to the GUI.
        """
        instructions = tk.Label(
            self.root,
            text="Select a PDF file on your computer to extract all its text",
            font="Raleway",
            bg=THEMES[self.current_theme]["background"],
            fg=THEMES[self.current_theme]["text"],
        )
        instructions.grid(columnspan=3, column=0, row=2)

    def setup_buttons(self):
        """
        Adds buttons for browsing and clearing text, and an entry for specifying the page range.
        """
        button_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["background"])
        button_frame.grid(column=1, row=3, columnspan=2, pady=(5, 20))

        page_range_label = tk.Label(
            button_frame,
            text="Page Range (ex.: 1, 3-7):",
            font="Raleway",
            bg=THEMES[self.current_theme]["background"],
            fg=THEMES[self.current_theme]["text"],
        )
        page_range_label.grid(column=0, row=0, padx=(5, 0), sticky="e")

        self.page_range_entry = tk.Entry(
            button_frame,
            font="Raleway",
            width=10,
            bg=THEMES[self.current_theme]["background"],
            fg=THEMES[self.current_theme]["text"],
        )
        self.page_range_entry.grid(column=1, row=0, padx=5, sticky="w")

        self.page_range_entry.insert(0, "1")

        self.browse_text.set("Browse")
        browse_button = tk.Button(
            button_frame,
            textvariable=self.browse_text,
            command=self.open_file,
            font="Raleway",
            bg=THEMES["light"]["primary"],
            fg=THEMES["light"]["secondary"],
            activebackground=THEMES["light"]["button_active"],
            activeforeground=THEMES["light"]["secondary"],
            height=2,
            width=20,
        )
        browse_button.grid(column=0, row=1, padx=5, pady=5)

        self.clear_button_text.set("Clear Text")
        clear_button = tk.Button(
            button_frame,
            textvariable=self.clear_button_text,
            command=self.clear_text,
            font="Raleway",
            bg=THEMES["light"]["primary"],
            fg=THEMES["light"]["secondary"],
            activebackground=THEMES["light"]["button_active"],
            activeforeground=THEMES["light"]["secondary"],
            height=2,
            width=20,
        )
        clear_button.grid(column=1, row=1, padx=5, pady=5)

    def add_bottom_margin(self):
        """
        Adds a bottom margin to the window.
        """
        bottom_margin = tk.Frame(
            self.root, height=40, bg=THEMES[self.current_theme]["background"]
        )
        bottom_margin.grid(columnspan=3, row=5)

    def restore_text_box_and_scrollbar(self, text_box_content):
        """
        Restores the text box, scrollbar, and copy button with the given content if it exists.
        """
        if text_box_content is not None:
            text_box_frame = tk.Frame(
                self.root, bg=THEMES[self.current_theme]["background"]
            )
            text_box_frame.grid(
                column=4, row=0, rowspan=5, padx=10, pady=(10, 10), sticky="nsew"
            )

            self.scrollbar = tk.Scrollbar(text_box_frame)
            self.scrollbar.pack(side="right", fill="y")

            self.text_box = tk.Text(
                text_box_frame,
                height=20,
                width=50,
                padx=15,
                pady=15,
                wrap="word",
                bg=THEMES[self.current_theme]["background"],
                fg=THEMES[self.current_theme]["text"],
                yscrollcommand=self.scrollbar.set,
            )
            self.text_box.pack(side="left", fill="both", expand=True)
            self.scrollbar.config(command=self.text_box.yview)
            self.text_box.insert("1.0", text_box_content)

            self.create_copy_button()

    def open_file(self):
        """
        Opens a file dialog to select a PDF file and displays its content for the specified page range.
        """
        self.browse_text.set("Loading...")
        file = askopenfile(
            parent=self.root,
            mode="rb",
            title="Choose a file",
            filetype=[("Pdf file", "*.pdf")],
        )
        if file:
            read_pdf = PyPDF2.PdfReader(file)

            page_range = self.page_range_entry.get().strip()
            extracted_text = ""

            try:
                if "-" in page_range:
                    first_page, last_page = map(int, page_range.split("-"))
                    for page_num in range(first_page - 1, last_page):
                        extracted_text += read_pdf.pages[page_num].extract_text() + "\n"
                else:
                    page_num = int(page_range) - 1
                    extracted_text = read_pdf.pages[page_num].extract_text()
            except (ValueError, IndexError):
                extracted_text = "Invalid page range or page number."

            if self.text_box is not None:
                self.text_box.destroy()
                self.text_box = None
            if self.scrollbar is not None:
                self.scrollbar.destroy()
                self.scrollbar = None

            text_box_frame = tk.Frame(
                self.root, bg=THEMES[self.current_theme]["background"]
            )
            text_box_frame.grid(
                column=4, row=0, rowspan=5, padx=10, pady=(10, 10), sticky="nsew"
            )

            self.scrollbar = tk.Scrollbar(text_box_frame)
            self.scrollbar.pack(side="right", fill="y")

            self.text_box = tk.Text(
                text_box_frame,
                height=20,
                width=50,
                padx=15,
                pady=15,
                wrap="word",
                bg=THEMES[self.current_theme]["background"],
                fg=THEMES[self.current_theme]["text"],
                yscrollcommand=self.scrollbar.set,
            )
            self.text_box.pack(side="left", fill="both", expand=True)

            self.scrollbar.config(command=self.text_box.yview)

            self.text_box.insert(1.0, extracted_text)

            copy_button = tk.Button(
                self.root,
                text="Copy",
                command=self.copy_text_box_content,
                font="Raleway",
                bg=THEMES["light"]["primary"],
                fg=THEMES["light"]["secondary"],
                activebackground=THEMES["light"]["button_active"],
                activeforeground=THEMES["light"]["secondary"],
            )
            copy_button.grid(column=4, row=5, pady=(5, 10), sticky="n")

            self.browse_text.set("Browse")

    def create_copy_button(self):
        """
        Creates a "Copy" button below the text box to copy its content to the clipboard.
        """
        copy_button = tk.Button(
            self.root,
            text="Copy",
            command=self.copy_text_box_content,
            font="Raleway",
            bg=THEMES["light"]["primary"],
            fg=THEMES["light"]["secondary"],
            activebackground=THEMES["light"]["button_active"],
            activeforeground=THEMES["light"]["secondary"],
        )
        copy_button.grid(column=4, row=5, pady=(5, 10), sticky="n")

    def copy_text_box_content(self):
        """
        Copies the entire content of the text box to the clipboard.
        """
        if self.text_box is not None:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.text_box.get("1.0", "end-1c"))
            self.root.update()

    def clear_text(self):
        """
        Clears the text box content, hides the scrollbar, and resets the layout.
        """
        if self.text_box is not None:
            self.text_box.destroy()
            self.text_box = None

        if self.scrollbar is not None:
            self.scrollbar.destroy()
            self.scrollbar = None

        self.canvas.config(width=600, height=300)
        self.canvas.grid(column=0, row=0, columnspan=3, rowspan=3)

        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["column"]) == 4:
                widget.destroy()

    def toggle_theme(self):
        """
        Toggles between light and dark themes and updates the GUI.
        """
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.setup_gui()


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()
