#!/usr/bin/env python3

# Secrets, easily generate passwords.
#     Copyright (C) 2022  Unicorn
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
gi.require_version('Gtk','4.0')
gi.require_version('Gdk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk



class window(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacing = 10

        #window
        Gtk.Window.__init__(self, title='Secrets')
        self.set_default_size(960, 540)


        #Define the General structure of the Window

        #Header Bar
        self.headerBar = Gtk.HeaderBar()
        self.set_titlebar(self.headerBar)
        self.headerBar.set_show_title_buttons(True)
        self.title = Gtk.Label()
        self.title.set_label('Secrets')
        self.headerBar.set_title_widget(self.title)

        #Setup general window Structure
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
        self.mainBox.set_margin_start(self.spacing)
        self.mainBox.set_margin_end(self.spacing)
        self.mainBox.set_margin_top(self.spacing)
        self.mainBox.set_margin_bottom(self.spacing)
        self.set_child(self.mainBox)

        #Populate the Header Bar
        #Hamburger Menu
        #Popover and Button
        self.popover = Gtk.Popover(position = Gtk.PositionType.BOTTOM, has_arrow = True)
        self.menuButton = Gtk.MenuButton(popover=self.popover, icon_name = "open-menu-symbolic", primary = True)
        self.headerBar.pack_end(self.menuButton)
        #add a box to the Menu
        self.menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing)
        self.popover.set_child(self.menuBox)
        #add Menu Items
        self.about = Gtk.Button(label = 'About', has_frame = False)
        self.about.connect('clicked', self.aboutClicked)
        self.menuBox.append(self.about)

        #generate Password button
        self.generateButton = Gtk.Button(label = "Generate")
        self.generateButton.connect("clicked", self.generateClicked)
        self.headerBar.pack_start(self.generateButton)
        #hide/show Password toggle
        #self.hideSwitch = Gtk.Switch()
        #self.headerBar.pack_end(self.hideSwitch)

        #Populate the Window itself
        self.passwordBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = self.spacing, hexpand = True)
        self.mainBox.append(self.passwordBox)
        self.password = Gtk.Entry(placeholder_text = "Password", editable = False, secondary_icon_name = "eye-open-negative-filled-symbolic", visibility = False, hexpand = True)
        self.password.connect("icon_press", self.hideClicked, Gtk.EntryIconPosition.SECONDARY)
        self.passwordBox.append(self.password)
        self.copyPasswordButton = Gtk.Button(label = "Copy")
        self.copyPasswordButton.connect("clicked", self.copyPasswordClicked)
        self.passwordBox.append(self.copyPasswordButton)
        self.settingsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)

    def copyPasswordClicked(self, widget):
        Gdk.Display.get_clipboard(Gdk.Display.get_default()).set_content(Gdk.ContentProvider.new_for_value(self.password.get_text()))

    def hideClicked(self, widget, position0, position1):
        if(widget.get_visibility() == False):
            widget.set_visibility(True)
            widget.set_icon_from_icon_name(Gtk.Orientation.VERTICAL, "eye-not-looking-symbolic")
        else:
            widget.set_visibility(False)
            widget.set_icon_from_icon_name(Gtk.Orientation.VERTICAL, "eye-open-negative-filled-symbolic")

    def generateClicked(self, widget):
        self.password.set_text("test")

    def aboutClicked(self, widget):
        self.dialog = Gtk.AboutDialog(authors = ['Unicorn'], artists= ['Unicorn'], comments = 'Easily generate passwords with different conditions to fit the requirements of various websites and apps.', license_type = Gtk.License.GPL_3_0_ONLY, program_name = 'Secrets', version = '1.0.0', website_label = 'Github', website = 'https://github.com/UnicornyRainbow/Secrets')
        self.dialog.set_logo_icon_name('secrets')
        self.dialog.show()

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = window(application = app)
        self.win.present()


app2=MyApp(application_id='io.github.unicorn.secrets')
app2.run(sys.argv)