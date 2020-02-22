import re
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import get_platform


class Scraper(QThread):
    links = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        self.links.emit(self.get_download_links())
        return

    def get_download_links(self):
        links = []

        # Stable Builds
        links.extend(self.scrap_stable_releases())

        # Daily Builds
        daily_builds = self.scrap_download_links(
            "https://builder.blender.org/download")
        for link in daily_builds:
            links.append(('daily', link))

        # Experimental Branches
        experimental = self.scrap_download_links(
            "https://builder.blender.org/download/branches")
        for link in experimental:
            links.append(('experimental', link))

        return links

    def scrap_download_links(self, url, _limit=None):
        platform = get_platform()
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        links = []

        if platform == 'Windows':
            for link in soup.find_all(limit=_limit, href=re.compile(r'blender-.+win.+64.+zip')):
                links.append(urljoin(url, link['href']).rstrip('/'))
        elif platform == 'Linux':
            for link in soup.find_all(limit=_limit, href=re.compile(r'blender-.+linux.+64.+tar')):
                links.append(urljoin(url, link['href']).rstrip('/'))

        return links

    def scrap_stable_releases(self):
        releases = []
        url = "https://ftp.nluug.nl/pub/graphics/blender/release/"
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')

        for release in soup.find_all(href=re.compile(r'Blender\d+.+')):
            releases.append(urljoin(url, release['href']))

        releases = releases[-4:]
        releases.reverse()
        stable_links = []

        for release in releases:
            links = self.scrap_download_links(release)
            links.reverse()

            for link in links:
                stable_links.append(('stable', link))

        return stable_links