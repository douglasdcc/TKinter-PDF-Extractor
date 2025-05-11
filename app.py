import tkinter as tk
from tkinter.filedialog import askopenfile

import PyPDF2
from PIL import Image, ImageDraw, ImageTk

from themes import THEMES  # Import the themes


class PDFApp:
    def __init__(self, root_):
        self.root = root_
        self.text_box = None
        self.browse_text = tk.StringVar()
        self.clear_button_text = tk.StringVar()
        self.current_theme = "light"

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

        self.restore_text_box(text_box_content)

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
            text="Page Range:",
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

    def restore_text_box(self, text_box_content):
        """
        Restores the text_box with the given content if it exists.
        """
        if text_box_content is not None:
            self.text_box = tk.Text(
                self.root,
                height=10,
                width=50,
                padx=15,
                pady=15,
                bg=THEMES[self.current_theme]["background"],
                fg=THEMES[self.current_theme]["text"],
            )
            self.text_box.insert("1.0", text_box_content)
            self.text_box.tag_configure("center", justify="center")
            self.text_box.tag_add("center", "1.0", "end")
            self.text_box.grid(column=1, row=4)

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

            # Get the page range from the user input
            page_range = (
                self.page_range_entry.get().strip()
            )  # Read the input from the entry field
            extracted_text = ""

            try:
                if "-" in page_range:  # Handle a range of pages
                    first_page, last_page = map(int, page_range.split("-"))
                    for page_num in range(
                        first_page - 1, last_page
                    ):  # Convert to zero-based index
                        extracted_text += read_pdf.pages[page_num].extract_text() + "\n"
                else:  # Handle a single page
                    page_num = int(page_range) - 1  # Convert to zero-based index
                    extracted_text = read_pdf.pages[page_num].extract_text()
            except (ValueError, IndexError):
                extracted_text = "Invalid page range or page number."

            # Display the extracted text in the text box
            if self.text_box is not None:
                self.text_box.destroy()
            self.text_box = tk.Text(
                self.root,
                height=10,
                width=50,
                padx=15,
                pady=15,
                bg=THEMES[self.current_theme]["background"],
                fg=THEMES[self.current_theme]["text"],
            )
            self.text_box.insert(1.0, extracted_text)
            self.text_box.tag_configure("center", justify="center")
            self.text_box.tag_add("center", 1.0, "end")
            self.text_box.grid(column=1, row=4)

            self.browse_text.set("Browse")
            self.canvas.config(width=600, height=250)
            self.canvas.grid(columnspan=3)

    def clear_text(self):
        """
        Clears the text box content.
        """
        if self.text_box is not None:
            self.text_box.destroy()
            self.canvas.config(width=600, height=300)

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
