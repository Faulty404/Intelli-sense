import gi
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango, Gdk

class NotesApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Notes App")
        self.set_default_size(800, 600)

        # Create a notebook for multiple notes
        self.notebook = Gtk.Notebook()

        # Add the first note page
        self.add_new_note()

        # Create buttons to add new notes and search
        add_note_button = Gtk.Button(label="+ New Note")
        add_note_button.connect("clicked", self.add_new_note)

        search_entry = Gtk.Entry()
        search_entry.set_placeholder_text("Search...")
        search_entry.connect("activate", self.search_text)

        replace_entry = Gtk.Entry()
        replace_entry.set_placeholder_text("Replace with...")

        replace_button = Gtk.Button(label="Replace")
        replace_button.connect("clicked", self.replace_text, search_entry, replace_entry)

        # Create a horizontal box for search and replace
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        search_box.pack_start(search_entry, True, True, 0)
        search_box.pack_start(replace_entry, True, True, 0)
        search_box.pack_start(replace_button, False, False, 0)

        # Create a vertical box layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(add_note_button, False, False, 0)
        vbox.pack_start(search_box, False, False, 0)
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

        # Create a toolbar for text formatting
        toolbar = Gtk.Toolbar()

        # Formatting buttons
        buttons = [
            (Gtk.STOCK_BOLD, self.set_bold),
            (Gtk.STOCK_ITALIC, self.set_italic),
            (Gtk.STOCK_UNDERLINE, self.set_underline),
            (Gtk.STOCK_SELECT_COLOR, self.set_highlight),
            (Gtk.STOCK_JUSTIFY_LEFT, self.justify_left),
            (Gtk.STOCK_JUSTIFY_RIGHT, self.justify_right),
            (Gtk.STOCK_ADD, self.add_bullet)
        ]

        for stock, handler in buttons:
            button = Gtk.ToolButton.new_from_stock(stock)
            button.connect("clicked", handler, text_view)
            toolbar.insert(button, -1)

        # Page style buttons
        ruled_page_button = Gtk.ToolButton(label="Ruled")
        ruled_page_button.connect("clicked", self.set_ruled, text_view)
        toolbar.insert(ruled_page_button, -1)

        grid_page_button = Gtk.ToolButton(label="Grid")
        grid_page_button.connect("clicked", self.set_grid, text_view)
        toolbar.insert(grid_page_button, -1)

        # Vertical box for toolbar and text area
        note_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        note_vbox.pack_start(toolbar, False, False, 0)
        note_vbox.pack_start(scrolled_window, True, True, 0)

        # Add the page to the notebook
        self.notebook.append_page(note_vbox, Gtk.Label(label=f"Note {self.notebook.get_n_pages() + 1}"))
        self.notebook.show_all()

    def search_text(self, widget):
        search_query = widget.get_text().lower()
        current_page = self.notebook.get_current_page()
        note_vbox = self.notebook.get_nth_page(current_page)
        scrolled_window = note_vbox.get_children()[1]
        text_view = scrolled_window.get_child()
        buffer = text_view.get_buffer()

        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, True)
        if search_query in text.lower():
            print(f"Found: '{search_query}'")
        else:
            print("Not Found")

    def replace_text(self, widget, search_entry, replace_entry):
        search_query = search_entry.get_text().lower()
        replace_text = replace_entry.get_text()
        current_page = self.notebook.get_current_page()
        note_vbox = self.notebook.get_nth_page(current_page)
        scrolled_window = note_vbox.get_children()[1]
        text_view = scrolled_window.get_child()
        buffer = text_view.get_buffer()

        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, True)
        updated_text = text.replace(search_query, replace_text)
        buffer.set_text(updated_text)

    def set_bold(self, widget, text_view):
        self.apply_tag(text_view, "bold", weight=Pango.Weight.BOLD)

    def set_italic(self, widget, text_view):
        self.apply_tag(text_view, "italic", style=Pango.Style.ITALIC)

    def set_underline(self, widget, text_view):
        self.apply_tag(text_view, "underline", underline=Pango.Underline.SINGLE)

    def set_highlight(self, widget, text_view):
        self.apply_tag(text_view, "highlight", background="yellow")

    def justify_left(self, widget, text_view):
        self.apply_tag(text_view, "justify_left", justification=Pango.Justification.LEFT)

    def justify_right(self, widget, text_view):
        self.apply_tag(text_view, "justify_right", justification=Pango.Justification.RIGHT)

    def add_bullet(self, widget, text_view):
        buffer = text_view.get_buffer()
        buffer.insert_at_cursor("• ")

    def set_ruled(self, widget, text_view):
        text_view.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.9, 0.9, 0.9, 1))

    def set_grid(self, widget, text_view):
        text_view.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.8, 0.8, 0.8, 1))

    def apply_tag(self, text_view, tag_name, **properties):
        buffer = text_view.get_buffer()
        tag = buffer.create_tag(tag_name, **properties)
        start, end = buffer.get_selection_bounds()
        if start and end:
            buffer.apply_tag(tag, start, end)

app = NotesApp()
app.connect("destroy", Gtk.main_quit)
app.show_all()
Gtk.main()

