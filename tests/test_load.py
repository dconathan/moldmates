from moldmates.load import parse_line


def test_parse_line():
    assert parse_line('{{1, 2}, {-3,-4}}') == ((1, 2), (-3, -4))

if __name__ == '__main__':
    test_parse_line()