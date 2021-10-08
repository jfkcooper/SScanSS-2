######
Themes
######
SScanSS-2 themes allows you to customize the interface colors. The user interface, text and icons will be rendered using
the colours from the selected theme. The software ships with a dark theme in addition to the default light theme and
custom themes can be added via a theme file and the user can select their desired theme from the preference dialog.

.. note::
    Theme changes will not be applied immediately but after the software is restarted

*************
Theme Colours
*************
The theme file is a JSON file which contains key-colour pairs for different components of the GUI. The colour should be
in the hexadecimal format.

====================    ===================
Key                     Description
====================    ===================
background              A colour for the windows background
foreground              A colour for the windows text and icons should contrast with "background"
background.alternate    Used mostly as the background color for text entry widgets
highlight               A color to indicate a selected item or the current item
highlight.alternate     A color for the text of highlighted objects should contrast with "highlight"
midtone                 A colour used by disabled widgets
error.background        A colour for the background of the error banner
error.foreground        A colour for the error text should contrast with "error.background" and 'background'
warning.background      A colour for the background of the warning banner
warning.foreground      A colour for the warning text should contrast with "warning.background"
info.background         A colour for the background of the information banner
info.foreground         A colour for the information text should contrast with "info.background"
====================    ===================

The theme file should contain key and colour entries as strings, any unspecified key or invalid colour would be set to
a default value. For example, the default theme file is::

    {
        "foreground": "#333",
        "background": "#f0f0f0",
        "background.alternate": "#fff",
        "highlight": "#0078d7",
        "highlight.alternate": "#fff",
        "midtone": "#787878",
        "error.background": "#F6A7A3",
        "error.foreground": "#CD6155",
        "warning.background": "#FFD38A",
        "warning.foreground": "#856404",
        "info.background": "#D1ECF1",
        "info.foreground": "#1f8394"
    }


******************
Adding a new theme
******************
To create a new theme, do the following:

1. Create a new file and give it the same name as the theme e.g dark.json.
2. Place the new file in the themes folder (*static/themes*) in the install directory
3. Populate the file with the key and colour pairs as shown in the example above.
4. The user should then be able to select any valid theme via the preferences dialog.

.. note::
    The theme file must contain valid JSON i.e. no missing brackets, quotes or commas. Otherwise the theme would not
    be loadable from the preference dialog.
