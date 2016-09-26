from asciimatics.event import KeyboardEvent
from asciimatics.event import MouseEvent
from asciimatics.widgets import Frame, Layout, Label, Divider, CheckBox, Button, PopUpDialog
from asciimatics.screen import Screen
from asciimatics.exceptions import StopApplication
# from asciimatics.exceptions import ResizeScreenError
# from asciimatics.widgets import TextBox, Text, RadioButtons
# from asciimatics.scene import Scene
# from asciimatics.widgets import Widget
# from asciimatics.exceptions import NextScene
from quickprompts.common.util import Util


# Initial data for the form
form_data = {
}


class SelectorFrame(Frame):

    # Properties

    @property
    def layouts(self):
        return self._layouts

    # Magic Methods

    def __init__(self, screen, menu_view_model):
        super(SelectorFrame, self).__init__(screen,
                                            int(screen.height),
                                            int(screen.width),
                                            data=form_data,
                                            name="Menu",
                                            title="Trove Classifiers")
        self._menu_view_model = menu_view_model
        self._screen = screen
        self._place_widgets()

    # Public Methods

    def set_title(self, new_title):
        self._title = ' ' + new_title[0:self._canvas.width - 4] + ' ' if new_title else ''

    # Private Methods

    def _ascend(self):
        item_stepped_out_of = self._menu_view_model.step_out_of_item()
        for layout in reversed(self.layouts):
            for column in reversed(layout.columns):
                for i in range(len(column)):
                    column.pop()
                layout.columns.pop()
            self.layouts.pop()
        self._place_widgets()
        if item_stepped_out_of:
            for layout in self.layouts:
                for column_index in range(len(layout.columns)):
                    for widget_index in range(len(layout.columns[column_index])):
                        if layout.columns[column_index][widget_index].name:
                            if layout.columns[column_index][widget_index].name[:-2].strip() == item_stepped_out_of:
                                self.switch_focus(layout, column_index, widget_index)

    def _descend(self, item_text):
        self._menu_view_model.step_into_item(item_text)
        for layout in reversed(self.layouts):
            for column in reversed(layout.columns):
                for i in range(len(column)):
                    column.pop()
                layout.columns.pop()
            self.layouts.pop()
        self._place_widgets()
        # raise NextScene()

    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def _place_widgets(self):
        self.set_title('Trove Classifiers')
        if self._menu_view_model.bread_crumbs:
            self.set_title('Trove Classifiers: ' + '::'.join(self._menu_view_model.bread_crumbs))

        layout = SelectorLayout([4, 27], on_left_arrow=self._ascend)
        self.add_layout(layout)
        self._reset_button = Button("Reset", self._reset)
        display_overhead = 4
        if self._menu_view_model.bread_crumbs:
            layout.add_widget(Label(''), 0)
            layout.add_widget(BackButton('<<< ..', self._ascend), 1)
            display_overhead = 5
        layout.add_widget(Label(" Options:"), 0)
        name_base = '::'.join(self._menu_view_model.bread_crumbs) + '::' if self._menu_view_model.bread_crumbs else ''
        for option in self._menu_view_model:
            if Util.str_ends_in_substr(option, ' >>'):
                layout.add_widget(ArrowButton(option, self._descend), 1)
            else:
                layout.add_widget(
                    RightSelectCheckBox(option, name=name_base + option, on_change=self._on_change), 1)
        for i in range(self._screen.height - len(self._menu_view_model) - display_overhead):
            layout.add_widget(Label(""), 1)
        layout2 = SelectorLayout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider(height=1), 0)
        layout2.add_widget(Divider(height=1), 1)
        layout2.add_widget(Divider(height=1), 2)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)
        self._reset_button.disabled = True
        for key, value in self.data.items():
            if value:
                self._reset_button.disabled = False
                break
        self.fix()

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")

    def _reset(self):
        self.data = {}
        while self._menu_view_model.bread_crumbs:
            self._ascend()
        self._ascend()
        # self.reset()
        # raise NextScene()

    def _view(self):
        # Build result of this form and display it.
        self.save()
        copy_data = dict(self.data)
        for key, value in copy_data.items():
            if not value:
                self.data.pop(key)
        message = "Values entered are:\n\n"
        for key, value in self.data.items():
            message += "- {}: {}\n".format(key, value)
        self._scene.add_effect(
            PopUpDialog(self._screen, message, ["OK"]))


class SelectorLayout(Layout):

    # Properties

    @property
    def columns(self):
        return self._columns

    # Magic Methods

    def __init__(self, *args, **kwargs):
        self._on_left_arrow = None
        if 'on_left_arrow' in kwargs.keys():
            self._on_left_arrow = kwargs['on_left_arrow']
            kwargs.pop('on_left_arrow')
        super(SelectorLayout, self).__init__(*args, **kwargs)

    # Public Methods

    def process_event(self, event, hover_focus):
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_DOWN:
                event.key_code = Screen.KEY_TAB
            if event.key_code == Screen.KEY_UP:
                event.key_code = Screen.KEY_BACK_TAB
            if event.key_code == Screen.KEY_LEFT:
                if self._on_left_arrow:
                    self._on_left_arrow()
                    return
        return super(SelectorLayout, self).process_event(event, hover_focus)


class ArrowButton(Button):

    # Properties

    # Magic Methods

    def __init__(self, *args, **kwargs):
        args = args[:2]
        if 'label' in kwargs:
            kwargs['label'] = None
        super(ArrowButton, self).__init__(*args, **kwargs)
        self._text = args[0]
        self._name = self._text

    # Public Methods

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord(" "), 10, 13, Screen.KEY_RIGHT]:
                self._on_click(self._text)
                return
            else:
                # Ignore any other key press.
                return event
        elif isinstance(event, MouseEvent):
            new_event = self._frame.rebase_event(event)
            if event.buttons != 0:
                if (self._x <= new_event.x < self._x + self._w and
                        self._y <= new_event.y < self._y + self._h):
                    self._on_click(self._text)
                    return
        return event

    def set_layout(self, x, y, offset, w, h):
        super(Button, self).set_layout(x, y, offset, w, h)
        self._w = min(self._w, len(self._text))

    def update(self, frame_no):
        self._draw_label()

        (colour, attr, bg) = self._pick_colours("field", self._has_focus)
        self._frame.canvas.print_at(
            self._text[:-2],
            self._x + self._offset + 4,
            self._y,
            colour, attr, bg)

        (colour, attr, bg) = self._pick_colours("control", self._has_focus)
        self._frame.canvas.print_at(
            self._text[-2:],
            self._x + self._offset + 4 + len(self._text[:-2]),
            self._y,
            colour, attr, bg)

    # Private Methods


class BackButton(Button):

    # Properties

    # Magic Methods

    def __init__(self, *args, **kwargs):
        super(BackButton, self).__init__(*args, **kwargs)
        self._text = args[0]

    # Public Methods

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord(" "), 10, 13, Screen.KEY_LEFT]:
                self._on_click()
                return
            else:
                # Ignore any other key press.
                return event
        elif isinstance(event, MouseEvent):
            new_event = self._frame.rebase_event(event)
            if event.buttons != 0:
                if (self._x <= new_event.x < self._x + self._w and
                        self._y <= new_event.y < self._y + self._h):
                    self._on_click()
                    return
        return event

    def set_layout(self, x, y, offset, w, h):
        super(Button, self).set_layout(x, y, offset, w, h)
        self._w = min(self._w, len(self._text))

    def update(self, frame_no):
        self._draw_label()

        (colour, attr, bg) = self._pick_colours("field", self._has_focus)
        self._frame.canvas.print_at(
            self._text[4:],
            self._x + self._offset + 4,
            self._y,
            colour, attr, bg)

        (colour, attr, bg) = self._pick_colours("control", self._has_focus)
        self._frame.canvas.print_at(
            self._text[:4],
            self._x + self._offset,
            self._y,
            colour, attr, bg)

    # Private Methods


class RightSelectCheckBox(CheckBox):

    # Properties

    # Magic Methods

    def __init__(self, *args, **kwargs):
        super(RightSelectCheckBox, self).__init__(*args, **kwargs)

    # Public Methods

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_RIGHT:
                event.key_code = ord(" ")
        return super(RightSelectCheckBox, self).process_event(event)

    # Private Methods
