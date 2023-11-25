from src.JsonParser import parse_incomplete_json


def test_parse_incomplete_json():
    cut_in_key = '{"key": "value", "ke'
    cut_in_value = '{"key": "value", "key": "val'
    cut_in_list = '{"key": ["value", "val'
    empty = ""

    assert parse_incomplete_json(cut_in_key) == {"key": "value"}
    assert parse_incomplete_json(cut_in_value) == {"key": "value"}
    assert parse_incomplete_json(cut_in_list) == {"key": ["value"]}
    assert parse_incomplete_json(empty) == {}

    with open("tests/incomplete.json", "r") as f:
        json_data = f.read()

    for i in range(len(json_data)):
        try:
            parse_incomplete_json(json_data[:i]) == {"key": "value"}
        except Exception:
            assert False, "Should not raise exception"
