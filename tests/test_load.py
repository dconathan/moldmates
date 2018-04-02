from moldmates.load import parse_line
from moldmates.objects import Chainline


def test_parse_line():
    assert parse_line('{{1, 2}, {-3,-4}}') == Chainline(xs=[1, -3], ys=[2, -4])
