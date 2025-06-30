import re
import unittest

HTML_FILES = ['index.html', 'gift.html', 'hit.html', 'points.html', 'enhancement.html', 'newenchant.html']

class TestDarkMode(unittest.TestCase):
    def test_dark_mode_support(self):
        pattern_root = re.compile(r':root\s*{')
        pattern_dark = re.compile(r'html\.dark\s*{')
        pattern_toggle = re.compile(r'classList\.toggle\(\s*["\']dark["\']\s*\)')
        pattern_btn = re.compile(r'id="(toggleTheme|themeBtn)"')
        for fname in HTML_FILES:
            with self.subTest(page=fname):
                with open(fname, encoding='utf-8') as f:
                    content = f.read()
                self.assertRegex(content, pattern_root, msg=f"{fname} lacks :root")
                self.assertRegex(content, pattern_dark, msg=f"{fname} lacks html.dark")
                self.assertRegex(content, pattern_toggle, msg=f"{fname} lacks dark toggle")
                self.assertRegex(content, pattern_btn, msg=f"{fname} lacks theme button")

if __name__ == '__main__':
    unittest.main()

