# Test of widgets

import pytest
import sys
import logging

import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

from widgets.base_page_widget import BasePageWidget, SortingType
from widgets.base_tool_box_widget import BaseToolBoxWidget
from widgets.elided_text_label import ElidedTextLabel


@pytest.fixture
def get_FakeBlenderLauncher():

    class FakeBlenderLauncher(QMainWindow):
        logger = logging.getLogger(__name__)
        version = "1.15.1"
        argv = sys.argv
        app = QApplication(argv)
        
    return FakeBlenderLauncher()


@pytest.fixture
def get_BasePageWidget(get_FakeBlenderLauncher):
        
    bl = get_FakeBlenderLauncher

    bpw = BasePageWidget(
        parent=bl,
        page_name="Test",
        time_label="Testing Time",
        info_text="Testing",
        extended_selection=True
    )

    return bpw


def test_subversionLabel_button(qtbot, get_BasePageWidget):

    bpw = get_BasePageWidget

    qtbot.addWidget(bpw)

    qtbot.mouseClick(bpw.subversionLabel, QtCore.Qt.LeftButton)

    assert bpw.sorting_type == SortingType.VERSION


def test_commitTimeLabel_button(qtbot, get_BasePageWidget):

    bpw = get_BasePageWidget

    qtbot.addWidget(bpw)

    qtbot.mouseClick(bpw.commitTimeLabel, QtCore.Qt.LeftButton)

    assert bpw.sorting_type == SortingType.DATETIME


def test_add_page_widget(get_BasePageWidget):

    btbw = BaseToolBoxWidget()

    value = btbw.add_page_widget(get_BasePageWidget, get_BasePageWidget.name)

    assert len(btbw.pages) == 1 and value.parent.name == "Test"


def test_ElidedTestLabel():

    etl = ElidedTextLabel("Test")

    assert etl.text == "Test"
