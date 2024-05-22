import datetime as dt

import pytest
from arpav_ppcv import operations


@pytest.mark.parametrize(
    "range, expected",
    [
        pytest.param("../..", (None, None)),
        pytest.param(
            "1982-12-10T01:01:00Z/..",
            (dt.datetime(1982, 12, 10, 1, 1, 0, tzinfo=dt.timezone.utc), None),
        ),
        pytest.param(
            "1982-12-10T01:01:00+01:00/..",
            (dt.datetime(1982, 12, 10, 0, 1, 0, tzinfo=dt.timezone.utc), None),
        ),
        pytest.param(
            "1982-12-10T01:01:00+02:00/..",
            (dt.datetime(1982, 12, 9, 23, 1, 0, tzinfo=dt.timezone.utc), None),
        ),
    ],
)
def test_parse_temporal_range(range, expected):
    result = operations._parse_temporal_range(range)
    assert result == expected
