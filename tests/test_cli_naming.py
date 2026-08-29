from genius.naming import genius_name, normalize_purpose


def test_name_code():
    assert genius_name("Code") == "Genius-Code"


def test_name_distributed_systems():
    assert genius_name("Distributed Systems") == "Genius-Distributed-Systems"


def test_normalize_strips_unsafe():
    assert "Genius-" in genius_name("Foo/Bar")
