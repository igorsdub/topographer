import pytest

from topographer.core.unionfind import UnionFind


def test_unionfind_make_set_and_find_round_trip():
    uf = UnionFind()

    uf.make_set("a")
    uf.make_set("b")

    assert uf.find("a") == "a"
    assert uf.find("b") == "b"


def test_unionfind_union_merges_components():
    uf = UnionFind()

    uf.make_set(1)
    uf.make_set(2)
    uf.make_set(3)

    uf.union(1, 2)

    assert uf.find(1) == uf.find(2)
    assert uf.find(3) != uf.find(1)


def test_unionfind_find_raises_for_unknown_element():
    uf = UnionFind()

    with pytest.raises(KeyError, match="not found in UnionFind"):
        uf.find("missing")
