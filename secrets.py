# Secrets, easily generate passwords.
#     Copyright (C) 2022  UnicornyRainbow
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import gi
import sys
import random
gi.require_version('Gtk','4.0')
gi.require_version('Gdk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, Gio

if __debug__:
    uipath = "secrets.ui"
else:
    uipath = "/app/bin/secrets.ui"

@Gtk.Template(filename=uipath)
class main_window(Gtk.Window):
    __gtype_name__ = "main_window"

    mainBox = Gtk.Template.Child()
    popover = Gtk.Template.Child()
    popoverBox = Gtk.Template.Child()
    password = Gtk.Template.Child()
    specialCharacters = Gtk.Template.Child()
    extendedSpecialCharacters = Gtk.Template.Child()
    useDigits = Gtk.Template.Child()
    useUpperCase = Gtk.Template.Child()
    useLowerCase = Gtk.Template.Child()
    useSpecialCharacters = Gtk.Template.Child()
    useExtendedSpecialCharacters = Gtk.Template.Child()
    lengthSpin = Gtk.Template.Child()
    aboutDialog = Gtk.Template.Child()

    uchars = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
    lchars = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
    digits = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    schars = ("@", "%", "+", "\\", "/", "'", "!", "#", "$", "^", "?", ";", ",", "(", ")", "{", "}", "[", "]", "~", "`", "-", "_", ".")
    echars = ('*', '+', ':', '<', '>', '=', '|', '"')

    @Gtk.Template.Callback()
    def onDestroy(self, *args):
        Gtk.main_quit()

    @Gtk.Template.Callback()
    def generateClicked(self, widget):
        secret = []
        chars = []
        if self.useDigits.get_active() == True:
            for item in self.digits:
                chars.append(item)
        if self.useUpperCase.get_active() == True:
            for item in self.uchars:
                chars.append(item)
        if self.useLowerCase.get_active() == True:
            for item in self.lchars:
                chars.append(item)
        if self.useSpecialCharacters.get_active() == True:
            for item in self.schars:
                chars.append(item)
        if self.useExtendedSpecialCharacters.get_active() == True:
            for item in self.echars:
                chars.append(item)
        for i in range(int(self.lengthSpin.get_value())):
            secret.append(random.choice(chars))
        self.password.set_text("".join(secret))

    @Gtk.Template.Callback()
    def hideClicked(self, widget, position):
        if(widget.get_visibility() == False):
            widget.set_visibility(True)
            widget.set_icon_from_icon_name(Gtk.Orientation.VERTICAL, "eye-not-looking-symbolic")
        else:
            widget.set_visibility(False)
            widget.set_icon_from_icon_name(Gtk.Orientation.VERTICAL, "eye-open-negative-filled-symbolic")

    @Gtk.Template.Callback()
    def copyPasswordClicked(self, widget):
        print("2")
        Gdk.Display.get_clipboard(Gdk.Display.get_default()).set_content(Gdk.ContentProvider.new_for_value(self.password.get_text()))

    @Gtk.Template.Callback()
    def editSpecialClicked(self, widget):
        self.specialCharacters.set_editable(widget.get_active())

    @Gtk.Template.Callback()
    def editExtendedSpecialClicked(self, widget):
        self.extendedSpecialCharacters.set_editable(widget.get_active())
        
    @Gtk.Template.Callback()
    def aboutClicked(self, *args):
        self.aboutDialog.set_logo_icon_name("io.github.unicornyrainbow.secrets")
        self.aboutDialog.show()
    

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        window = main_window(application = self)

        window.mainBox.remove(window.mainBox.get_first_child())
        window.popover.set_child(window.popoverBox)

        window.specialCharacters.set_text(" ".join(window.schars))
        window.extendedSpecialCharacters.set_text(" ".join(window.echars))
        window.lengthSpin.set_value(20)
        window.present()


app2 = MyApp(application_id='io.github.unicornyrainbow.secrets', flags=Gio.ApplicationFlags.FLAGS_NONE)
app2.run(sys.argv)