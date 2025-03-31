import gi
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

class NotesApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Notes App")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        
        # Set application icon
        try:
            self.set_icon_from_file("notes-icon.png")
        except:
            pass  # Continue if icon not found

        # Create a notebook for multiple notes
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)

        # Add the first note page
        self.add_new_note()

        # Create header bar
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Notes App"
        self.set_titlebar(header)

        # Add note button in header
        add_note_button = Gtk.Button.new_from_icon_name("document-new-symbolic", Gtk.IconSize.BUTTON)
        add_note_button.set_tooltip_text("New Note")
        add_note_button.connect("clicked", self.add_new_note)
        header.pack_start(add_note_button)

        # Create a vertical box layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(self.notebook, True, True, 0)

        self.add(vbox)

    def add_new_note(self, widget=None):
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)

        # Set default font
        font_desc = Pango.FontDescription("Sans 12")
        text_view.override_font(font_desc)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(text_view)

        # Toolbar
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.ICONS)

        # Formatting buttons with proper icons
        button_data = [
            ("format-text-bold", self.set_bold, "Bold"),
            ("format-text-italic", self.set_italic, "Italic"),
            ("format-text-underline", self.set_underline, "Underline"),
            ("format-text-highlight", self.set_highlight, "Highlight"),
            ("format-justify-left", self.justify_left, "Align Left"),
            ("format-justify-center", self.justify_center, "Center"),
            ("format-justify-right", self.justify_right, "Align Right"),
            ("format-list-bulleted", self.add_bullet, "Bullet List")
        ]

        for icon_name, handler, tooltip in button_data:
            image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
            button = Gtk.ToolButton()
            button.set_icon_widget(image)
            button.connect("clicked", handler, text_view)
            button.set_tooltip_text(tooltip)
            toolbar.insert(button, -1)

        # Font size dropdown
        font_size_combo = Gtk.ComboBoxText()
        for size in range(8, 33, 2):
            font_size_combo.append_text(str(size))
        font_size_combo.set_active(2)  # Default size 12
        font_size_combo.connect("changed", self.set_font_size, text_view)
        font_size_combo.set_tooltip_text("Font Size")
        font_size_toolitem = Gtk.ToolItem()
        font_size_toolitem.add(font_size_combo)
        toolbar.insert(font_size_toolitem, -1)

        # Font selection dropdown
        font_combo = Gtk.ComboBoxText()
        fonts = ["Sans", "Serif", "Monospace", "Arial", "Courier", "Verdana"]
        for font in fonts:
            font_combo.append_text(font)
        font_combo.set_active(0)
        font_combo.connect("changed", self.set_font, text_view)
        font_combo.set_tooltip_text("Font Family")
        font_toolitem = Gtk.ToolItem()
        font_toolitem.add(font_combo)
        toolbar.insert(font_toolitem, -1)

        # Vertical box for toolbar and text area
        note_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        note_vbox.pack_start(toolbar, False, False, 0)
        note_vbox.pack_start(scrolled_window, True, True, 0)

        # Add the page to the notebook
        label = Gtk.Label(label=f"Note {self.notebook.get_n_pages() + 1}")
        self.notebook.append_page(note_vbox, label)
        self.notebook.show_all()

    def set_font_size(self, combo, text_view):
        size = combo.get_active_text()
        if size:
            self.apply_tag(text_view, f"font-size-{size}", size_points=int(size))

    def set_font(self, combo, text_view):
        font = combo.get_active_text()
        if font:
            self.apply_tag(text_view, f"font-{font}", family=font)

    def set_bold(self, widget, text_view):
        self.apply_tag(text_view, "bold", weight=Pango.Weight.BOLD)

    def set_italic(self, widget, text_view):
        self.apply_tag(text_view, "italic", style=Pango.Style.ITALIC)

    def set_underline(self, widget, text_view):
        self.apply_tag(text_view, "underline", underline=Pango.Underline.SINGLE)

    def set_highlight(self, widget, text_view):
        self.apply_tag(text_view, "highlight", background="yellow")

    def justify_left(self, widget, text_view):
        self.apply_tag(text_view, "justify_left", justification=Gtk.Justification.LEFT)

    def justify_center(self, widget, text_view):
        self.apply_tag(text_view, "justify_center", justification=Gtk.Justification.CENTER)

    def justify_right(self, widget, text_view):
        self.apply_tag(text_view, "justify_right", justification=Gtk.Justification.RIGHT)

    def add_bullet(self, widget, text_view):
        buffer = text_view.get_buffer()
        buffer.insert_at_cursor("• ")

    def apply_tag(self, text_view, tag_name, **properties):
        buffer = text_view.get_buffer()
        tag = buffer.create_tag(tag_name, **properties)

        try:
            start, end = buffer.get_selection_bounds()
            buffer.remove_tag_by_name(tag_name, start, end)
            buffer.apply_tag(tag, start, end)
        except ValueError:
            insert_iter = buffer.get_insert()
            buffer.apply_tag(tag, insert_iter, insert_iter)

app = NotesApp()
app.connect("destroy", Gtk.main_quit)
app.show_all()
Gtk.main()
