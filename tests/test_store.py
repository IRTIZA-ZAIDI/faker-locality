from faker_locality.store import load_localities, load_exonyms


def test_load_localities():
    df = load_localities()
    assert not df.empty
    assert "city" in df.columns
    assert "country" in df.columns
    assert "province" in df.columns


def test_load_exonyms():
    df = load_exonyms()
    assert not df.empty
    assert "exonym" in df.columns
