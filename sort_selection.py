from typing import List
from lib import SwapBasedSortMethod


class SelectionSort(SwapBasedSortMethod):
    def sort(self) -> List[int]:
        n = len(self.target)
        for i in range(n - 1):
            self.set("L", i)
            # 最小値のインデックスを探す
            min_index = i
            self.set("R", min_index)
            self.set("MIN", min_index)
            for j in range(i + 1, n):
                self.set("R", j)
                if self.target[j] < self.target[min_index]:
                    min_index = j
                    self.set("MIN", min_index)
            # 最小値を現在の位置と交換
            if min_index != i:
                # self.target[i], self.target[min_index] = self.target[min_index], self.target[i]
                self.swap("L", "MIN")
        return self.target
