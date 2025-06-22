import pytest
from app.models import Item

def test_item_str():
    item = Item(name="Test", description="Desc")
    assert str(item) == "Test"
