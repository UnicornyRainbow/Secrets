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
    UI_PATH = "src/ui/secrets.ui"
    LOCALE_PATH = "src/mo"
else:
    UI_PATH = "/app/bin/secrets.ui"
    LOCALE_PATH = "/app/share/locale"


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

@dataclass
class State:
    width: int
    height: int
    stackVisible: string

    length: int
    useDigits: bool
    useUpperCase: bool
    useLowerCase: bool
    useSpecialCharacters: bool
    specialCharacters: str
    specialCharactersExpander: bool

    memLength: int
    capitalize: bool
    includeDigits: bool
    delimiter: str
    delimiterExpander: bool

    pinLength: int

@Gtk.Template(filename=UI_PATH)
class MainWindow(Adw.Window):
    __gtype_name__ = "MainWindow"

    # global
    aboutDialog: Adw.AboutDialog = Gtk.Template.Child()
    stack: Adw.ViewStack = Gtk.Template.Child()
    password: Adw.PasswordEntryRow = Gtk.Template.Child()

    # random
    ranLengthSpin: Gtk.SpinButton = Gtk.Template.Child()
    ranLengthSpinAdjustment: Gtk.Adjustment = Gtk.Template.Child()
    useUpperCase: Gtk.Switch = Gtk.Template.Child()
    useLowerCase: Gtk.Switch = Gtk.Template.Child()
    useDigits: Gtk.Switch = Gtk.Template.Child()
    useSpecialCharacters: Gtk.Switch = Gtk.Template.Child()
    specialCharacters: Adw.EntryRow = Gtk.Template.Child()
    specialCharactersExpander: Adw.ExpanderRow = Gtk.Template.Child()

    # memorable
    memLengthSpin: Gtk.SpinButton = Gtk.Template.Child()
    memLengthSpinAdjustment: Gtk.Adjustment = Gtk.Template.Child()
    capitalize: Gtk.Switch = Gtk.Template.Child()
    includeDigits: Gtk.Switch = Gtk.Template.Child()
    delimiter: Adw.EntryRow = Gtk.Template.Child()
    delimiterExpander: Adw.ExpanderRow = Gtk.Template.Child()

    # pin
    pinLengthSpin: Gtk.SpinButton = Gtk.Template.Child()
    pinLengthSpinAdjustment: Gtk.Adjustment = Gtk.Template.Child()

    dictionary = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dictionary = self.read_dictionary()

    def get_hunspell_encoding(_, aff_path):
        try:
            with open(aff_path, "r", encoding="ascii", errors="ignore") as aff:
                for line in aff:
                    if line.startswith("SET "):
                        return line.split(" ")[1].strip()
            print("Could not find encoding in " + aff_path, file=sys.stderr)
        except:
            print("Could not read " + aff_path, file=sys.stderr)
        return "utf-8"

    def read_dictionary(self):
        lang = locale.getlocale()[0]
        dict_dir = "/usr/share/hunspell/"
        dict_path = dict_dir
        words = []

        if os.path.exists(dict_dir + lang + ".dic"):
            dict_path += lang + ".dic"
        elif os.path.exists(dict_dir + lang.split('_')[0] + ".dic"):
            dict_path += lang.split('_')[0] + ".dic"
        elif next(filter(lambda e: e.endswith(".dic") and e.startswith(lang.split('_')[0]),
                        os.listdir(dict_dir)),
                None):
            dict_path += next(filter(lambda e: e.endswith(".dic") and e.startswith(lang.split('_')[0]),
                                    os.listdir(dict_dir)))
        elif next(filter(lambda e: e.endswith(".dic") and e.startswith("en"),
                        os.listdir(dict_dir)),
                None):
            dict_path += next(filter(lambda e: e.endswith(".dic") and e.startswith("en"),
                                    os.listdir(dict_dir)))

        dict_encoding = self.get_hunspell_encoding(dict_path.replace(".dic", ".aff"))

        try:
            with open(dict_path, "r", encoding=dict_encoding) as dict:
                next(dict)
                for line in dict:
                    word = line.split('/')[0].strip().lower()
                    if 8>= len(word) >= 4 and word.isalpha():
                        words.append(word)
        except:
            print("Could not read dictionary for " + lang, file=sys.stderr)

        return words

    def generate_random(self):
        chars = ""
        if self.useDigits.get_active():
            chars += string.digits
        if self.useUpperCase.get_active():
            chars += string.ascii_uppercase
        if self.useLowerCase.get_active():
            chars += string.ascii_lowercase
        if self.useSpecialCharacters.get_active():
            chars += self.specialCharacters.get_text()
        return "".join(secrets.choice(chars)
                       for i in
                       range(int(self.ranLengthSpin.get_value())))

    def generate_memorable(self):
        words = [secrets.choice(self.dictionary) for i in range(int(self.memLengthSpin.get_value()))]

        if self.capitalize.get_active():
            words = [e.capitalize() for e in words]
        if self.includeDigits.get_active():
            words = [e + secrets.choice(string.digits) for e in words]

        return self.delimiter.get_text().join(words)

    def generate_pin(self):
        return "".join(secrets.choice(string.digits)
                       for i in
                       range(int(self.pinLengthSpin.get_value())))

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        with open(XDG_CONFIG_HOME + "/config.json", "w") as file:
            width, height = self.get_default_size()
            state = State(
                width=width,
                height=height,
                stackVisible=self.stack.get_visible_child_name(),

                length=self.ranLengthSpinAdjustment.get_value(),
                useDigits=self.useDigits.get_active(),
                useUpperCase=self.useUpperCase.get_active(),
                useLowerCase=self.useLowerCase.get_active(),
                useSpecialCharacters=self.useSpecialCharacters.get_active(),
                specialCharacters=self.specialCharacters.get_text(),
                specialCharactersExpander=self.specialCharactersExpander.get_expanded(),

                memLength=self.memLengthSpinAdjustment.get_value(),
                capitalize=self.capitalize.get_active(),
                includeDigits=self.includeDigits.get_active(),
                delimiter=self.delimiter.get_text(),
                delimiterExpander=self.delimiterExpander.get_expanded(),

                pinLength=self.pinLengthSpinAdjustment.get_value(),
            )
            jsonstate=json.dumps(asdict(state))
            file.write(jsonstate)

    @Gtk.Template.Callback()
    def generate_clicked(self, widget: Gtk.Button):
        match self.stack.get_visible_child_name():
            case "random":
                password = self.generate_random()
            case "memorable":
                password = self.generate_memorable()
            case "pin":
                password = self.generate_pin()
        self.password.set_text(password)

    @Gtk.Template.Callback()
    def copy_password_clicked(self, widget: Gtk.Button):
        Gdk.Display.get_clipboard(Gdk.Display.get_default()).set_content(
            Gdk.ContentProvider.new_for_value(self.password.get_text())
        )

    @Gtk.Template.Callback()
    def reset_clicked(self, widget: Gtk.Button):

        state = State(
            width=500,
            height=500,
            stackVisible="random",

            length=20,
            useDigits=True,
            useUpperCase=True,
            useLowerCase=True,
            useSpecialCharacters=True,
            specialCharacters=string.punctuation,
            specialCharactersExpander=False,

            memLength=5,
            capitalize=True,
            includeDigits=False,
            delimiter="-",
            delimiterExpander=False,

            pinLength=6,
        )

        self.set_default_size(state.width, state.height)
        self.stack.set_visible_child_name(state.stackVisible)

        self.ranLengthSpinAdjustment.set_value(state.length)
        self.useUpperCase.set_active(state.useUpperCase)
        self.useLowerCase.set_active(state.useLowerCase)
        self.useDigits.set_active(state.useDigits)
        self.useSpecialCharacters.set_active(state.useSpecialCharacters)
        self.specialCharacters.set_text(state.specialCharacters)
        self.specialCharactersExpander.set_expanded(state.specialCharactersExpander)

        self.memLengthSpinAdjustment.set_value(state.memLength)
        self.capitalize.set_active(state.capitalize)
        self.includeDigits.set_active(state.includeDigits)
        self.delimiter.set_text(state.delimiter)
        self.delimiterExpander.set_expanded(state.delimiterExpander)

        self.pinLengthSpinAdjustment.set_value(state.pinLength)
        self.present()

        with open(XDG_CONFIG_HOME + "/config.json", "w") as file:
            jsonstate=json.dumps(asdict(state))
            file.write(jsonstate)

    @Gtk.Template.Callback()
    def about_clicked(self, *args):
        self.aboutDialog.present(self)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        window = MainWindow(application=self)

        window.specialCharacters.set_text(string.punctuation)
        window.delimiter.set_text("-")

        if os.path.exists(XDG_CONFIG_HOME + "/config.json"):
            try:
                with open(XDG_CONFIG_HOME + "/config.json", "r") as file:
                    state = State(**json.load(file))

                    window.set_default_size(state.width, state.height)
                    window.stack.set_visible_child_name(state.stackVisible)

                    window.ranLengthSpinAdjustment.set_value(state.length)
                    window.useUpperCase.set_active(state.useUpperCase)
                    window.useLowerCase.set_active(state.useLowerCase)
                    window.useDigits.set_active(state.useDigits)
                    window.useSpecialCharacters.set_active(state.useSpecialCharacters)
                    window.specialCharacters.set_text(state.specialCharacters)
                    window.specialCharactersExpander.set_expanded(state.specialCharactersExpander)

                    window.memLengthSpinAdjustment.set_value(state.memLength)
                    window.capitalize.set_active(state.capitalize)
                    window.includeDigits.set_active(state.includeDigits)
                    window.delimiter.set_text(state.delimiter)
                    window.delimiterExpander.set_expanded(state.delimiterExpander)

                    window.pinLengthSpinAdjustment.set_value(state.pinLength)
            except:
                pass

        window.aboutDialog.add_credit_section(name=_("App Name"), people=["Brage Fuglseth"])

        window.present()

app2 = MyApp(application_id=APP, flags=Gio.ApplicationFlags.FLAGS_NONE)
app2.run(sys.argv)
