#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Key Cutter, easily generate passwords.
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
from dataclasses import dataclass, asdict
import os
import json
import gettext
import locale

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk, Gio

if __debug__:
    UI_PATH = "src/res/secrets.ui"
    LOCALE_PATH = "src/res/po"
else:
    UI_PATH = "/app/bin/secrets.ui"
    LOCALE_PATH = "/app/bin/po"


if os.environ.get("XDG_CACHE_HOME"):
    XDG_CONFIG_HOME = os.environ.get("XDG_CACHE_HOME")
else:
    if not os.path.isdir("~/.cache/keycutter"):
        os.makedirs("~/.cache/keycutter")
    XDG_CONFIG_HOME = "~/.cache/keycutter"

APP = "io.github.unicornyrainbow.secrets"

locale.setlocale(locale.LC_ALL, locale.getlocale())
if sys.platform != "darwin":
    locale.bindtextdomain(APP, LOCALE_PATH)
gettext.bindtextdomain(APP, LOCALE_PATH)
gettext.textdomain(APP)
_ = gettext.gettext
print(_("Generate"))

@dataclass
class State:
    width: int
    height: int
    length: int
    useDigits: bool
    useUpperCase: bool
    useLowerCase: bool
    useSpecialCharacters: bool
    specialCharacters: str
    specialCharactersExpander: bool

@Gtk.Template(filename=UI_PATH)
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
    specialCharactersExpander: Adw.ExpanderRow = Gtk.Template.Child()
    lengthSpin: Gtk.SpinButton = Gtk.Template.Child()
    lengthSpinAdjustment: Gtk.Adjustment = Gtk.Template.Child()
    aboutDialog: Adw.AboutWindow = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        with open(XDG_CONFIG_HOME + "/config.json", "w") as file:
            width, height = self.get_default_size()
            state = State(
                width=width,
                height=height,
                length=self.lengthSpinAdjustment.get_value(),
                useDigits=self.useDigits.get_active(),
                useUpperCase=self.useUpperCase.get_active(),
                useLowerCase=self.useLowerCase.get_active(),
                useSpecialCharacters=self.useSpecialCharacters.get_active(),
                specialCharacters=self.specialCharacters.get_text(),
                specialCharactersExpander=self.specialCharactersExpander.get_expanded()
            )
            jsonstate=json.dumps(asdict(state))
            file.write(jsonstate)

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
    def reset_clicked(self, widget: Gtk.Button):

        state = State(
            width=300,
            height=445,
            length=20,
            useDigits=True,
            useUpperCase=True,
            useLowerCase=True,
            useSpecialCharacters=True,
            specialCharacters=string.punctuation,
            specialCharactersExpander=False
        )

        self.specialCharacters.set_text(state.specialCharacters)
        self.useSpecialCharacters.set_active(state.useSpecialCharacters)
        self.useLowerCase.set_active(state.useLowerCase)
        self.useUpperCase.set_active(state.useUpperCase)
        self.useDigits.set_active(state.useDigits)
        self.lengthSpinAdjustment.set_value(state.length)
        self.set_default_size(state.width, state.height)
        self.specialCharactersExpander.set_expanded(state.specialCharactersExpander)

        with open(XDG_CONFIG_HOME + "/config.json", "w") as file:
            jsonstate=json.dumps(asdict(state))
            file.write(jsonstate)

    @Gtk.Template.Callback()
    def about_clicked(self, *args):
        self.aboutDialog.set_visible(True)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        window = MainWindow(application=self)

        window.mainBox.remove(window.mainBox.get_first_child())
        window.popover.set_child(window.popoverBox)

        window.specialCharacters.set_text(string.punctuation)

        if os.path.exists(XDG_CONFIG_HOME + "/config.json"):
            try:
                with open(XDG_CONFIG_HOME + "/config.json", "r") as file:
                    state = State(**json.load(file))

                    window.specialCharacters.set_text(state.specialCharacters)
                    window.useSpecialCharacters.set_active(state.useSpecialCharacters)
                    window.useLowerCase.set_active(state.useLowerCase)
                    window.useUpperCase.set_active(state.useUpperCase)
                    window.useDigits.set_active(state.useDigits)
                    window.lengthSpinAdjustment.set_value(state.length)
                    window.set_default_size(state.width, state.height)
                    window.specialCharactersExpander.set_expanded(state.specialCharactersExpander)
            except:
                pass

        window.aboutDialog.add_credit_section(name=_("App Name"), people=["Brage Fuglseth"])

        window.present()

app2 = MyApp(application_id=APP, flags=Gio.ApplicationFlags.FLAGS_NONE)
app2.run(sys.argv)
