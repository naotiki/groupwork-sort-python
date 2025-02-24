from typing import List
from lib import SwapBasedSortMethod

class BubbleSort(SwapBasedSortMethod):
    def sort(self) -> List[int]:
        n = len(self.target)
        for i in range(n - 1):
            # 隣接する要素を比較して交換
            for j in range(n - i - 1):
                self.set("L", j)
                self.set("R", j + 1)
                if self.target[j] > self.target[j + 1]:
                    # 交換
                    self.swap("L", "R")
        return self.target
