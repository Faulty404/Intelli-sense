import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango, Gdk, GdkPixbuf

import sys
import enchant

from gi.repository import Gtk, Gio, Pango, Gdk, GdkPixbuf

gi.require_version("Gtk", "3.0")

class NotesApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Enhanced Notes App")
        self.set_default_size(800, 600)

        # Spell checker
        self.spell_checker = enchant.Dict("en_US")

        # Create a notebook for multiple notes
        self.notebook = Gtk.Notebook()
        self.add_new_note()

        # Create buttons to add new notes
        add_note_button = Gtk.Button(label="+ New Note")
        add_note_button.connect("clicked", self.add_new_note)

        # Create a vertical box layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(add_note_button, False, False, 0)
        vbox.pack_start(self.notebook, True, True, 0)

        self.add(vbox)

    def add_new_note(self, widget=None):
        # Create a text view
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)

        # Create a scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(text_view)

        # Create a toolbar for formatting and rich media
        toolbar = Gtk.Toolbar()

        # Font size
        font_size_button = Gtk.ToolButton(label="Font Size")
        font_size_button.connect("clicked", self.change_font_size, text_view)
        toolbar.insert(font_size_button, -1)

        # Font color
        font_color_button = Gtk.ToolButton(label="Font Color")
        font_color_button.connect("clicked", self.change_font_color, text_view)
        toolbar.insert(font_color_button, -1)

        # Insert image
        insert_image_button = Gtk.ToolButton(label="Insert Image")
        insert_image_button.connect("clicked", self.insert_image, text_view)
        toolbar.insert(insert_image_button, -1)

        # Spell check
        spell_check_button = Gtk.ToolButton(label="Spell Check")
        spell_check_button.connect("clicked", self.spell_check, text_view)
        toolbar.insert(spell_check_button, -1)

        # Vertical box for toolbar and text area
        note_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        note_vbox.pack_start(toolbar, False, False, 0)
        note_vbox.pack_start(scrolled_window, True, True, 0)

        # Add the page to the notebook
        self.notebook.append_page(note_vbox, Gtk.Label(label=f"Note {self.notebook.get_n_pages() + 1}"))
        self.notebook.show_all()

    def change_font_size(self, widget, text_view):
        buffer = text_view.get_buffer()
        start, end = buffer.get_selection_bounds()
        if start and end:
            tag = buffer.create_tag("font_size", size_points=20)
            buffer.apply_tag(tag, start, end)

    def change_font_color(self, widget, text_view):
        buffer = text_view.get_buffer()
        start, end = buffer.get_selection_bounds()
        if start and end:
            tag = buffer.create_tag("font_color", foreground="blue")
            buffer.apply_tag(tag, start, end)

    def insert_image(self, widget, text_view):
        dialog = Gtk.FileChooserDialog(title="Select an Image", action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        if dialog.run() == Gtk.ResponseType.OK:
            image_path = dialog.get_filename()
            buffer = text_view.get_buffer()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 200, 200, True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            buffer.insert_pixbuf(buffer.get_end_iter(), pixbuf)
        dialog.destroy()

    def spell_check(self, widget, text_view):
        buffer = text_view.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, True)
        words = text.split()
        for word in words:
            if not self.spell_checker.check(word):
                print(f"Misspelled word: {word}")

app = NotesApp()
app.connect("destroy", Gtk.main_quit)
app.show_all()
Gtk.main()

