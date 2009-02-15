# -*- coding: utf-8 -*-
from uamobile.base import UserAgent, Display
import re

VODAFONE_VENDOR_RE = re.compile(r'V\d+([A-Z]+)')
JPHONE_VENDOR_RE = re.compile(r'J-([A-Z]+)')
CRAWLER_RE = re.compile(r'^(.+?)\([^)]+\)$')

class SoftBankUserAgent(UserAgent):
    carrier = 'SoftBank'
    short_carrier = 'S'

    def __init__(self, *args, **kwds):
        super(SoftBankUserAgent, self).__init__(*args, **kwds)
        self.serialnumber = None

    def supports_cookie(self):
        """
        returns True if the device supports HTTP Cookie.
        For more information, see
        http://www2.developers.softbankmobile.co.jp/dp/tool_dl/download.php?docid=119
        """
        return self.is_3g() or self.is_type_w()

    def is_softbank(self):
        return True

    def is_vodafone(self):
        return True

    def is_jphone(self):
        return True

    def is_3g(self):
        return self._is_3g

    def is_type_c(self):
        """
        returns True if the type is C.
        """
        return not self._is_3g and (self.version.startswith('3.') or self.version.startswith('2.'))

    def is_type_p(self):
        """
        returns True if the type is P.
        """
        return not self._is_3g and self.version.startswith('4.')

    def is_type_w(self):
        """
        returns True if the type is W.
        """
        return not self._is_3g and self.version.startswith('5.')

    def get_jphone_uid(self):
        """
        returns the x-jphone-uid
        for the information about x-jphone-uid, see
        http://developers.softbankmobile.co.jp/dp/tool_dl/web/tech.php
        """
        try:
            return self.environ['HTTP_X_JPHONE_UID']
        except KeyError:
            return None
    jphone_uid = property(get_jphone_uid)

    def get_msname(self):
        return self.environ.get('HTTP_X_JPHONE_MSNAME')
    msname = property(get_msname)

    def make_display(self):
        """
        create a new Display object.
        """
        try:
            width, height = map(int, self.environ['HTTP_X_JPHONE_DISPLAY'].split('*', 1))
        except (KeyError, ValueError, AttributeError):
            width = None
            height = None

        try:
            color_string = self.environ['HTTP_X_JPHONE_COLOR']
            try:
                color = color_string.startswith('C')
            except AttributeError:
                color = False

            try:
                depth = int(color_string[1:])
            except (ValueError, TypeError):
                depth = 0
        except KeyError:
            color = False
            depth = 0

        return Display(width=width, height=height, color=color, depth=depth)
