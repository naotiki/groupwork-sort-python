from typing import List
from lib import SortMethod


class InsertionSort(SortMethod):
    def sort(self) -> List[int]:
        self.set("SORTED", 0)
        while self.get("SORTED") != len(self.target) - 1:
            self.set("L", self.get("SORTED"))
            self.set("R", self.get("SORTED") + 1)
            while (
                self.get("L") >= 0
                and self.target[self.get("L")] > self.target[self.get("R")]
            ):
                self.swap("L", "R")
                self.dec("L")
                self.dec("R")
            self.inc("SORTED")

        return self.target
