import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hdhr_proxy.mxf import Epg123NoTunersError, import_and_map_mxf_with_epg123  # noqa: E402


class Epg123ImportErrorTests(unittest.TestCase):
    def test_no_tuners_error_is_reported_clearly(self):
        result = mock.Mock(returncode=57005, stdout="[ERROR] There are no devices/tuners configured in the database store.")
        with mock.patch("hdhr_proxy.mxf._find_epg123_client", return_value="epg123Client.exe"), \
                mock.patch("hdhr_proxy.mxf.subprocess.run", return_value=result):
            with self.assertRaises(Epg123NoTunersError):
                import_and_map_mxf_with_epg123("guide.mxf")

    def test_other_failures_are_not_misclassified(self):
        result = mock.Mock(returncode=1, stdout="[ERROR] some other failure")
        with mock.patch("hdhr_proxy.mxf._find_epg123_client", return_value="epg123Client.exe"), \
                mock.patch("hdhr_proxy.mxf.subprocess.run", return_value=result):
            with self.assertRaises(Exception) as raised:
                import_and_map_mxf_with_epg123("guide.mxf")
        self.assertNotIsInstance(raised.exception, Epg123NoTunersError)


if __name__ == "__main__":
    unittest.main()
