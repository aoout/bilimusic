# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from bilimusic import __version__
from bilimusic.urlconvert import *  # pylint: disable=unused-wildcard-import,wildcard-import


def test_version():
    assert __version__ == '0.1.0'


class TestUrlConvert:

    def __init__(self) -> None:
        self.bvid = 'BV1xh411q76p'
        self.av = 207590187  # pylint: disable=invalid-name
        self.url = 'https://www.bilibili.com/video/BV1xh411q76p?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click'

    def test_is_bvid(self):
        assert is_bvid(self.bvid)

    def test_is_av(self):
        assert is_av(self.av)

    def test_is_url(self):
        assert is_url(self.url)

    def test_bvid2url(self):
        assert bvid2url(self.bvid) == self.url

    def test_url2bvid(self):
        assert url2bvid(self.url) == self.bvid

    def test_av2url(self):
        assert av2url(self.av) == self.url

    def test_url2av(self):
        assert url2av(self.url) == self.av
