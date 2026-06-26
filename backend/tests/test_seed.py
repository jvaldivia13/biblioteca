from scripts.seed import SAMPLE_BOOKS


def test_sample_books_has_twenty_varied_books():
    categories = {book["categoria"] for book in SAMPLE_BOOKS}
    isbns = [book["isbn"] for book in SAMPLE_BOOKS]

    assert len(SAMPLE_BOOKS) == 20
    assert len(categories) >= 15
    assert len(isbns) == len(set(isbns))
