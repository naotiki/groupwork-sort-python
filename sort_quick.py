from typing import List
from lib import SortMethod


class QuickSort(SortMethod):
    def quick_sort_impl(self, l: int, r: int):
        if l >= r:
            return
        self.set("L", l)
        self.set("R", r)
        ptr = ("L", +1)
        while self.get("L") != self.get("R"):
            if self.target[self.get("L")] > self.target[self.get("R")]:
                self.swap("L", "R")
                ptr = ("R", -1) if ptr[0] == "L" else ("L", +1)
                self.add(ptr[0], ptr[1])
            else:
                self.add(ptr[0], ptr[1])
        middle = self.get("L")
        self.quick_sort_impl(l, middle - 1)
        self.quick_sort_impl(middle + 1, r)

    def sort(self) -> List[int]:
        self.quick_sort_impl(0, len(self.target) - 1)
        return self.target