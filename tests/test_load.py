from moldmates.load import parse_line


def test_parse_line():
    assert parse_line('{{1, 2}, {-3,-4}}').xs == [1, -3]
    assert parse_line('{{1, 2}, {-3,-4}}').ys == [2, -4]
