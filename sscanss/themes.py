from contextlib import suppress
from enum import Enum, unique
import json
from PyQt5 import QtCore, QtWidgets, QtGui
from sscanss.config import ICONS_PATH, THEME_PATH


GLOBAL_STYLES = """

* {
    font-family: "Helvetica Neue", Helvetica, Arial;
    font-size: 12px;
}

QToolBar {
    spacing: 10px; /* spacing between items in the tool bar */
    padding: 5px;
}

#form-title
{
    font-size: 16px;
    font-weight: 400;
    margin-bottom: 10px;
}

#h2
{
  font-size: 14px;
  font-weight: 600;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox{
  padding: 5px;
}

QPushButton, #DropDownButton {
    padding: 10px 15px;
}

QComboBox QAbstractItemView::item {
    padding: 5px;
}

QStatusBar {
    min-height: 20px;
    border-top: 1px solid palette(mid);
}

QStatusBar::item {
    border: None;
}

QStatusBar QLabel {
    margin-right: 10px;
}

#ToolButton, #MenuButton {
    icon-size: 24px;
    qproperty-autoRaise: true;
}

QToolButton#ToolButton::menu-indicator {
    subcontrol-position: right bottom;
    subcontrol-origin: padding;
    left: 4px;
    top: 4px
}

#MenuButton::menu-indicator {
    image: none;
}

QListWidget {
    show-decoration-selected: 1;
}

#CustomTab{
    padding:10px 5px;
    margin:0;
    Font Weight: 300;
    border-top: 1px transparent;
    border-bottom: 2px solid palette(mid);
    border-right: 1px transparent;
    border-left: 1px transparent;
}

#CustomTab:hover,
#CustomTab:checked,
#CustomTab:checked:focus,
#CustomTab:checked:pressed{
    border-bottom: 2px solid palette(highlight);
}

#Recents{
    background: transparent;
    border: 1px transparent;
}

#Error{
    color: @error.foreground;
}

#Error-Outline {
    border: 1px solid @error.foreground;
}

QProgressBar {
    border: 1px solid palette(shadow);
    border-radius: 2px;
    max-height: 5px;
}

QProgressBar::chunk {
    background-color: palette(highlight);
}


ProjectDialog QProgressBar {
    border: transparent;
    border-radius: 0px;
    background-color: transparent;
}

#MidToolButton {
    icon-size: 28px;
}

QDockWidget::title {
    padding: 5px 0px 5px 0px;
    border: 1px solid palette(mid);
    background: palette(dark);
}


QDockWidget::close-button {
    icon-size: 20px; /* maximum icon size */
}

#Error-Banner{
    padding:3px;
    border:1px solid @error.foreground;
    background-color: @error.background;
}

#Error-Banner QPushButton,
#Error-Banner QPushButton:focus{
    color: @error.foreground;
    font-weight:500;
    border: none;
    background-color: transparent;
}

#Error-Banner QPushButton:hover {border:1px solid @error.foreground;}

#Error-Banner QLabel { color: @error.foreground;}

#Info-Banner{
    padding:3px;
    border:1px solid @info.foreground;
    background-color: @info.background;
}

#Info-Banner QPushButton,
#Info-Banner QPushButton:focus{
    color: @info.foreground;
    font-weight: 500;
    border: none;
    background-color: transparent;
}

#Info-Banner QPushButton:hover {border:1px solid @info.foreground;}

#Info-Banner QLabel { color: @info.foreground;}

#Warning-Banner{
    padding:3px;
    border:1px solid @warning.foreground;
    background-color: @warning.background;
}

#Warning-Banner QPushButton,
#Warning-Banner QPushButton:focus{
    color: @warning.foreground;
    font-weight: 500;
    border: none;
    background-color: transparent;
}

#Warning-Banner QPushButton:hover {border:1px solid @warning.foreground;}

#Warning-Banner QLabel { color: @warning.foreground;}

FilePicker QPushButton {
    padding: 7px 7px;
}

#Normal-Pane {
    border-bottom: 1px solid gray;
}

#Warning-Pane {
    /*background-color: #F4D03F;*/
    background-color: @warning.background;
    border-bottom: 1px solid gray;
}

#Error-Pane {
    /*background-color: #CD6155;*/
    background-color: @error.background;
    border-bottom: 1px solid gray;
}

#Pane-Content {
    border-bottom: 1px solid gray;
}
"""

default_theme = {
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


def colourize_icon(mask_path, colour):
    """Loads an mask image and fills with given colour

    :param mask_path: mask file path
    :type mask_path: str
    :param colour: fill colour
    :type colour: QtGui.QColor
    :return: coloured icon
    :rtype: QtGui.QIcon
    """
    pixmap = QtGui.QPixmap(mask_path)
    painter = QtGui.QPainter(pixmap)
    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), colour)
    painter.end()

    return QtGui.QIcon(pixmap)


def load_theme(filename):
    """Reads theme colours from json file

    :param filename: theme json file
    :type filename: pathlib.WindowsPath
    :return:
    :rtype: Union[PyQt5.QtGui.QPalette, None, Dict[str, str]]
    """
    theme = default_theme.copy()
    with open(filename) as json_file:
        colours = json.load(json_file)
        for key, value in colours.items():
            if not QtGui.QColor.isValidColor(value):
                continue
            theme[key] = value

    return theme


def create_palette(theme):
    """Creates palette using the given theme colours

    :param theme: theme colours
    :type theme: Dict[str, str]
    :return: theme palette
    :rtype: QtGui.QPalette
    """
    foreground = QtGui.QColor(theme['foreground'])
    background = QtGui.QColor(theme['background'])
    mid_tone = QtGui.QColor(theme['midtone'])
    background_alternate = QtGui.QColor(theme['background.alternate'])
    highlight = QtGui.QColor(theme['highlight'])
    highlight_alternate = QtGui.QColor(theme['highlight.alternate'])

    palette = QtGui.QPalette()

    palette.setColor(QtGui.QPalette.Window, background)
    palette.setColor(QtGui.QPalette.WindowText, foreground)
    palette.setColor(QtGui.QPalette.Base, background_alternate)
    palette.setColor(QtGui.QPalette.AlternateBase, background)
    palette.setColor(QtGui.QPalette.ToolTipBase, highlight)
    palette.setColor(QtGui.QPalette.ToolTipText, foreground)
    palette.setColor(QtGui.QPalette.Text, foreground)
    palette.setColor(QtGui.QPalette.Button, background)
    palette.setColor(QtGui.QPalette.ButtonText, foreground)
    palette.setColor(QtGui.QPalette.Link, highlight)
    palette.setColor(QtGui.QPalette.Highlight, highlight)
    palette.setColor(QtGui.QPalette.HighlightedText, highlight_alternate)

    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, background_alternate)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, mid_tone)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, mid_tone)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, mid_tone)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, background)

    return palette


def create_stylesheet(theme):
    """Fills in theme colours in style sheet

    :param theme: theme colours
    :type theme: Dict[str, str]
    :return: stylesheet
    :rtype: str
    """
    style = GLOBAL_STYLES
    for key, value in theme.items():
        style = style.replace(f'@{key}', value)

    return style


# class Action(QtWidgets.QAction):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._icon_name = ''
#         self.prefix = ''
#         self.default_text = ''
#         self.theme = ThemeManager()
#         self.theme.theme_changed.connect(self.updateIcon)
#
#     @property
#     def icon_name(self):
#         return self._icon_name
#
#     @icon_name.setter
#     def icon_name(self, value):
#         self._icon_name = value
#         self.updateIcon()
#
#     def updateIcon(self):
#         if not self.icon_name:
#             return
#         icon = self.icon()
#         icon.addFile(self.theme.pathFor(self.icon_name))
#         self.setIcon(icon)
#
#     def setTextFormat(self, text_format, default_text):
#         self.prefix = text_format
#         self.default_text = default_text
#
#     def setPrefixedText(self, text):
#         if not text:
#             self.setText(self.default_text)
#         else:
#             self.setText(self.prefix.format(text))


class Singleton(type(QtCore.QObject), type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Themes(QtCore.QObject, metaclass=Singleton):
    theme_changed = QtCore.pyqtSignal()

    @unique
    class Icons(Enum):
        Checked = 'checked.png'
        Indeterminate = 'indeterminate.png'
        Unchecked = 'unchecked.png'
        Down_Triangle = 'triangle_down.png'
        Right_Triangle = 'triangle_right.png'
        Down_Arrow = 'arrow_up.png'
        Up_Arrow = 'arrow_down.png'
        New_File = 'file.png'
        Open_File = 'folder_open.png'
        Save_File = 'save.png'
        Undo = 'undo.png'
        Redo = 'redo.png'
        Solid = 'solid.png'
        Wireframe = 'wireframe.png'
        Transparent = 'blend.png'
        Toggle = 'exchange.png'
        Bounding_Box = 'bounding_box.png'
        Hide_Coordinate_Frame = 'hide_coordinate_frame.png'
        Hide_Fiducials = 'hide_fiducials.png'
        Hide_Measurements = 'hide_measurements.png'
        Hide_Vectors = 'hide_vectors.png'
        Question = 'question.png'
        Rotate_Sample = 'rotate.png'
        Translate_Sample = 'translate.png'
        Move_Origin = 'origin.png'
        Plane_Align = 'plane_align.png'
        Matrix_Transform = 'transform_matrix.png'
        Play = 'play.png'
        Stop = 'stop.png'
        Base = 'base.png'
        Select = 'select.png'
        Point = 'point.png'
        Line = 'line_tool.png'
        Area = 'area_tool.png'
        Cross = 'cross.png'
        Check = 'check.png'
        Merge = 'merge.png'
        Limit = 'limit.png'
        Lock = 'lock.png'
        Refresh = 'refresh.png'
        Export = 'export.png'
        Chart = 'chart.png'
        Circle_Check = 'circle_check.png'
        Circle_Minus = 'circle_minus.png'
        Circle_Cross = 'circle_cross.png'
        Circle_Exclaim = 'circle_exclaim.png'
        Eye_Slash = 'eye_slash.png'
        Camera = 'camera.png'

        ERROR_Collision = 'collision.png'
        ERROR_Deformed = 'deformed.png'
        ERROR_Limit_Hit = 'limit_hit.png'
        ERROR_Unreachable = 'unreachable.png'

    def __init__(self):
        super().__init__()
        self.default_style = None
        self.current_theme_name = ''
        self.themes = {'default': default_theme}
        self.icons = {}
        self.getThemes()
        self.setTheme('default')

    @property
    def current_theme(self):
        return self.themes[self.current_theme_name]

    def getThemes(self):
        """Loads themes from directory"""
        if not THEME_PATH.is_dir():
            return

        for style in THEME_PATH.iterdir():
            if not style.is_file() or style.suffix != '.json':
                continue

            with suppress(OSError, json.JSONDecodeError):
                self.themes[style.stem] = load_theme(style)

        app = QtWidgets.QApplication.instance()
        self.default_style = app.style().objectName()

    def setTheme(self, name):
        """Sets the current theme

        :param name: theme name
        :type name: str
        """
        if name not in self.themes:
            name = 'default'

        if self.current_theme_name == name:
            return

        app = QtWidgets.QApplication.instance()

        style = self.default_style if name == 'default' else 'Fusion'
        palette = create_palette(self.themes[name])

        app.setStyleSheet('')
        app.setStyle(style)
        app.setPalette(palette)
        QtWidgets.QToolTip.setPalette(palette)
        app.setStyleSheet(create_stylesheet(self.themes[name]))

        self.current_theme_name = name
        self.theme_changed.emit()

    def getIcon(self, name):
        """Gets icon with a given name and colours it to match theme

        :param name: icon name/id
        :type name: Themes.Icons
        :return: icon
        :rtype: QtGui.QIcon
        """
        if name in self.icons:
            return self.icons[name]

        if name.name.startswith('ERROR'):
            colour = QtGui.QColor(self.current_theme['error.foreground'])
        else:
            colour = QtGui.QColor(self.current_theme['foreground'])

        path = self.pathFor(name.value)
        if path:
            icon = colourize_icon(path, colour)
            self.icons[name] = icon
            return icon

        return QtGui.QIcon()

    def isDarkTheme(self):
        """Indicates if theme is dark or not

        :return: indicates if the current theme is a dark theme
        :rtype: bool
        """
        colour = QtGui.QColor(self.current_theme['background'])
        if colour.valueF() > 0.4:
            return False
        return True

    def pathFor(self, filename):
        """Gets full path of image with given filename

        :param filename: base name of image file with extension
        :type filename: str
        :return: full path of image file
        :rtype: str
        """
        path = ICONS_PATH / filename
        if path.is_file():
            return path.as_posix()

        return ''
