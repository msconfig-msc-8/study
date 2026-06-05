APP_STYLE = """
QMainWindow, QDialog {
    background-color: #F0F4F8;
}

QMenuBar {
    background-color: #2C3E50;
    color: #ECF0F1;
    font-size: 13px;
    padding: 2px;
}
QMenuBar::item:selected {
    background-color: #3D5166;
    border-radius: 3px;
}
QMenu {
    background-color: #2C3E50;
    color: #ECF0F1;
    border: 1px solid #3D5166;
}
QMenu::item:selected {
    background-color: #3498DB;
}
QMenu::separator {
    background-color: #3D5166;
    height: 1px;
    margin: 3px 8px;
}

QToolBar {
    background-color: #34495E;
    border: none;
    spacing: 4px;
    padding: 4px 8px;
}
QToolBar QToolButton {
    background-color: transparent;
    color: #ECF0F1;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 12px;
}
QToolBar QToolButton:hover {
    background-color: #3D5166;
    border-color: #5D7A99;
}
QToolBar QToolButton:pressed {
    background-color: #2C3E50;
}
QToolBar::separator {
    background-color: #5D7A99;
    width: 1px;
    margin: 4px 4px;
}

QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #EBF5FB;
    gridline-color: #D5E8F0;
    border: 1px solid #BDC3C7;
    border-radius: 4px;
    font-size: 13px;
    selection-background-color: #3498DB;
    selection-color: #FFFFFF;
}
QTableWidget::item {
    padding: 6px 4px;
}
QHeaderView::section {
    background-color: #2C3E50;
    color: #ECF0F1;
    font-weight: bold;
    font-size: 12px;
    padding: 7px 4px;
    border: none;
    border-right: 1px solid #3D5166;
}
QHeaderView::section:last {
    border-right: none;
}

QPushButton {
    background-color: #3498DB;
    color: #FFFFFF;
    border: none;
    border-radius: 5px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2980B9;
}
QPushButton:pressed {
    background-color: #1F618D;
}
QPushButton:disabled {
    background-color: #95A5A6;
    color: #D0D3D4;
}

QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #D5DBE1;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 13px;
    font-weight: bold;
    color: #2C3E50;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    left: 10px;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #BDC3C7;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 13px;
    color: #2C3E50;
    min-width: 140px;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #3498DB;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #BDC3C7;
    selection-background-color: #3498DB;
    selection-color: #FFFFFF;
}

QRadioButton {
    font-size: 13px;
    color: #2C3E50;
    spacing: 6px;
    min-width: 240px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QLabel {
    color: #2C3E50;
    font-size: 13px;
}

QScrollBar:vertical {
    background: #F0F4F8;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #95A5A6;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #7F8C8D;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
