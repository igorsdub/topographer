from __future__ import annotations

from collections.abc import Hashable


class UnionFind:
    def __init__(self):
        self.parents: dict[Hashable, Hashable] = {}
        self.ranks: dict[Hashable, int] = {}

    def make_set(self, x: Hashable):
        if x in self.parents:
            return

        self.parents[x] = x
        self.ranks[x] = 0

    def find(self, x: Hashable) -> Hashable:
        if x not in self.parents:
            raise KeyError(f"Element {x!r} not found in UnionFind")

        parent = self.parents[x]

        if parent != x:
            self.parents[x] = self.find(parent)

        return self.parents[x]

    def union(self, a: Hashable, b: Hashable) -> Hashable:
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return root_a

        rank_a = self.ranks[root_a]
        rank_b = self.ranks[root_b]

        if rank_a < rank_b:
            self.parents[root_a] = root_b
            return root_b

        if rank_a > rank_b:
            self.parents[root_b] = root_a
            return root_a

        self.parents[root_b] = root_a
        self.ranks[root_a] += 1
        return root_a


__all__ = ["UnionFind"]
