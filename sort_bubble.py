from typing import List
from lib import SortMethod


class BubbleSort(SortMethod):
    def sort(self) -> List[int]:
        n = len(self.target)
        for i in range(n - 1):
            # 隣接する要素を比較して交換
            for j in range(n - i - 1):
                self.set("L", j)
                self.set("R", j + 1)
                if self.target[j] > self.target[j + 1]:
                    # 交換
                    # self.target[j], self.target[j + 1] = (
                    # self.target[j + 1],
                    # self.target[j],
                    # )
                    self.swap("L", "R")
        return self.target
