from typing import List
from lib import SwapBasedSortMethod

class QuickSort(SwapBasedSortMethod):
    def quick_sort_impl(self, left: int, right: int):
        if left >= right:
            return
        self.set("L", left)
        self.set("R", right)
        ptr = ("L", +1)
        while self.get("L") != self.get("R"):
            if self.target[self.get("L")] > self.target[self.get("R")]:
                self.swap("L", "R")
                ptr = ("R", -1) if ptr[0] == "L" else ("L", +1)
                self.add(ptr[0], ptr[1])
            else:
                self.add(ptr[0], ptr[1])
        middle = self.get("L")
        self.quick_sort_impl(left, middle - 1)
        self.quick_sort_impl(middle + 1, right)

    def sort(self) -> List[int]:
        self.quick_sort_impl(0, len(self.target) - 1)
        return self.target
