# -*- coding: utf-8 -*-
from .widgets import SelectorFrame
from .selector_view_model import SelectorViewModel
from .common.util import Util

from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys
import platform

is_WIN = platform.system() == 'Windows'
if is_WIN:
    import win32console


class Selector(object):

    # Properties

    # Magic Methods

    def __init__(self, view_model):
        self._view_model = view_model
        self.last_scene = None
        self.old_out = None
        self.win_out = None

    # Public Methods

    def display(self):
        while True:
            try:
                # save the console so if the program encounters
                # a problem/exception we may be able to restore the console
                self._save_window()
                Screen.wrapper(self._start_app,
                               catch_interrupt=False,
                               arguments=[self.last_scene])
                break
            except ResizeScreenError as e:
                self.last_scene = e.scene
            except Exception as e:
                print('Unhandled exception: ' + str(e))
                self._restore_window()
                raise e

    @staticmethod
    def global_shortcuts(event):
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            # Stop on ctrl+q or ctrl+x
            if c in (17, 24):
                raise StopApplication('User terminated app')

    # Private Methods

    def _restore_window(self):
        if sys.platform == "win32":
            if self.old_out:
                self.old_out.SetConsoleActiveScreenBuffer()
                self.win_out = self.old_out

    def _save_window(self):
        if sys.platform == "win32":
            self.old_out = win32console.PyConsoleScreenBufferType(
                win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE))
            info = self.old_out.GetConsoleScreenBufferInfo()
            self.win_out = win32console.CreateConsoleScreenBuffer()
            self.win_out.SetConsoleScreenBufferSize(info['Size'])
            self.win_out.SetConsoleActiveScreenBuffer()

    def _start_app(self, screen, scene):
        self.screen = screen
        self.screen.set_title('Trove Classifiers')
        self.scenes = []
        self.effects = [
            SelectorFrame(screen, self._view_model)
        ]
        self.scenes.append(Scene(self.effects, -1))

        screen.play(self.scenes,
                    stop_on_resize=True,
                    start_scene=scene,
                    unhandled_input=self.global_shortcuts)


if __name__ == '__main__':
    svm = SelectorViewModel(Util.get_classifiers())
    selector = Selector(svm)
    selector.display()
