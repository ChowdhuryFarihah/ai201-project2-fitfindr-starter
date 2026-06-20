from tools import search_listings, suggest_outfit, create_fit_card

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []   # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)


print(test_search_returns_results())
print(test_search_empty_results())
print(test_search_price_filter())

def test_suggest_outfit_empty_wardrobe(monkeypatch):
    def fake_call_llm(prompt):
        return "Style it with baggy jeans, chunky sneakers, and a simple jacket."

    monkeypatch.setattr("tools.call_llm", fake_call_llm)

    new_item = {
        "title": "Faded Band Tee",
        "price": 22,
        "platform": "Depop",
        "style_tags": ["vintage", "grunge"],
    }

    wardrobe = {"items": []}

    result = suggest_outfit(new_item, wardrobe)

    assert isinstance(result, str)
    assert result.strip() != ""
    assert "baggy jeans" in result


def test_suggest_outfit_nonempty_wardrobe(monkeypatch):
    def fake_call_llm(prompt):
        return "Pair the band tee with your wide-leg jeans and platform Docs."

    monkeypatch.setattr("tools.call_llm", fake_call_llm)

    new_item = {
        "title": "Faded Band Tee",
        "price": 22,
        "platform": "Depop",
    }

    wardrobe = {
        "items": [
            {"name": "Wide-leg jeans", "category": "pants"},
            {"name": "Platform Docs", "category": "shoes"},
        ]
    }

    result = suggest_outfit(new_item, wardrobe)
    assert isinstance(result, str)
    assert result.strip() != ""
    assert "wide-leg jeans" in result

def test_create_fit_card_empty_outfit():
    new_item = {
        "title": "Faded Band Tee",
        "price": 22,
        "platform": "Depop",
    }

    result = create_fit_card("", new_item)

    assert isinstance(result, str)
    assert result.strip() != ""
    assert "missing" in result.lower() or "cannot" in result.lower()

def test_create_fit_card_success(monkeypatch):
    def fake_call_llm(prompt):
        return "Thrifted this Faded Band Tee from Depop for $22 and it’s giving 90s grunge."

    monkeypatch.setattr("tools.call_llm", fake_call_llm)

    outfit = "Pair it with wide-leg jeans and chunky sneakers."

    new_item = {
        "title": "Faded Band Tee",
        "price": 22,
        "platform": "Depop",
    }

    result = create_fit_card(outfit, new_item)

    assert isinstance(result, str)
    assert result.strip() != ""
    assert "Faded Band Tee" in result
    assert "Depop" in result
    assert "$22" in result