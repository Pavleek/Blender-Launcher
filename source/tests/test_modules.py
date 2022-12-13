# Test of modules

import pytest
import sys

from modules._platform import get_platform, set_locale


def test_get_platform_windows(monkeypatch):

    monkeypatch.setattr(sys, "platform", "win32")

    assert get_platform() == "Windows"


def test_get_platform_linux(monkeypatch):

    monkeypatch.setattr(sys, "platform", "linux")

    assert get_platform() == "Linux"


def test_get_platform_mac(monkeypatch):

    monkeypatch.setattr(sys, "platform", "darwin")

    assert get_platform() == "macOS"


def test_set_locale_windows(monkeypatch):

    def stub():
        return 'Windows'

    def mock(_, input):
        assert input == 'eng_usa'
        
    monkeypatch.setattr("modules._platform.get_platform", stub)
    monkeypatch.setattr("modules._platform.setlocale", mock)

    set_locale()


def test_set_locale_linux(monkeypatch):

    def stub():
        return 'Linux'

    def mock(_, input):
        assert input == 'en_US.UTF-8'
        
    monkeypatch.setattr("modules._platform.get_platform", stub)
    monkeypatch.setattr("modules._platform.setlocale", mock)

    set_locale()


def test_set_locale_mac(monkeypatch):

    def stub():
        return 'macOS'

    def mock(_, input):
        assert input == 'en_US.UTF-8'
        
    monkeypatch.setattr("modules._platform.get_platform", stub)
    monkeypatch.setattr("modules._platform.setlocale", mock)

    set_locale()
