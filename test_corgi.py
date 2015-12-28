from datetime import datetime
from parser import org_timestamp_to_dt


class TestParser(object):

    def test_org_timestamp_to_dt(self):
        org_timestamp = '<2013-10-06 Sun 1:18>'
        expected_dt = datetime(2013, 10, 6, 1, 18)
        assert org_timestamp_to_dt(org_timestamp) == expected_dt
