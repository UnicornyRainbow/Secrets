#!/usr/bin/env python3

# Secrets, easily generate passwords.
#     Copyright (C) 2023  UnicornyRainbow
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/agpl.html>.

import gi
import sys
import secrets
import string

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gdk, Gio

if __debug__:
    uipath = "src/res/secrets.ui"
else:
    uipath = "/app/bin/secrets.ui"


@Gtk.Template(filename=uipath)
class MainWindow(Adw.Window):
    __gtype_name__ = "MainWindow"

    mainBox: Gtk.Box = Gtk.Template.Child()
    popover: Gtk.Popover = Gtk.Template.Child()
    popoverBox: Gtk.Box = Gtk.Template.Child()
    password: Adw.PasswordEntryRow = Gtk.Template.Child()
    specialCharacters: Adw.EntryRow = Gtk.Template.Child()
    useDigits: Gtk.Switch = Gtk.Template.Child()
    useUpperCase: Gtk.Switch = Gtk.Template.Child()
    useLowerCase: Gtk.Switch = Gtk.Template.Child()
    useSpecialCharacters: Gtk.Switch = Gtk.Template.Child()
    lengthSpin: Gtk.SpinButton = Gtk.Template.Child()
    aboutDialog: Adw.AboutWindow = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        Gtk.main_quit()

    @Gtk.Template.Callback()
    def generate_clicked(self, widget: Gtk.Button):
        chars = ""
        if self.useDigits.get_active():
            chars += string.digits
        if self.useUpperCase.get_active():
            chars += string.ascii_uppercase
        if self.useLowerCase.get_active():
            chars += string.ascii_lowercase
        if self.useSpecialCharacters.get_active():
            chars += self.specialCharacters.get_text()
        self.password.set_text("".join(secrets.choice(chars) for i in range(int(self.lengthSpin.get_value()))))

    @Gtk.Template.Callback()
    def copy_password_clicked(self, widget: Gtk.Button):
        Gdk.Display.get_clipboard(Gdk.Display.get_default()).set_content(
            Gdk.ContentProvider.new_for_value(self.password.get_text())
        )

    @Gtk.Template.Callback()
    def about_clicked(self, *args):
        self.aboutDialog.set_visible(True)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        window = MainWindow(application=self)

        window.mainBox.remove(window.mainBox.get_first_child())
        window.popover.set_child(window.popoverBox)

        window.specialCharacters.set_text(string.punctuation)
        window.present()


app2 = MyApp(application_id='io.github.unicornyrainbow.secrets', flags=Gio.ApplicationFlags.FLAGS_NONE)
app2.run(sys.argv)
