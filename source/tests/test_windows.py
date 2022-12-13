# Test of windows

import pytest
import sys
import logging

from PyQt5.QtWidgets import QApplication, QMainWindow


@pytest.fixture
def get_FakeBlenderLauncher():

    class FakeBlenderLauncher(QMainWindow):
        logger = logging.getLogger(__name__)
        version = "1.15.1"
        argv = sys.argv
        app = QApplication(argv)
        
    return FakeBlenderLauncher()
