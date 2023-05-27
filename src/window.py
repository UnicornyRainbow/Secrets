# window.py
#
# Copyright 2023 unicorn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import gi
import sys
import secrets
import string

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gdk, Gio

@Gtk.Template(resource_path='/io/github/unicornyrainbow/secrets/window.ui')
class KeycutterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'KeycutterWindow'

    password: Adw.PasswordEntryRow = Gtk.Template.Child()
    specialCharacters: Adw.EntryRow = Gtk.Template.Child()
    useDigits: Gtk.Switch = Gtk.Template.Child()
    useUpperCase: Gtk.Switch = Gtk.Template.Child()
    useLowerCase: Gtk.Switch = Gtk.Template.Child()
    useSpecialCharacters: Gtk.Switch = Gtk.Template.Child()
    lengthSpin: Gtk.SpinButton = Gtk.Template.Child()

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.specialCharacters.set_text(string.punctuation)
