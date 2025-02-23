from typing import List
from lib import SwapBasedSortMethod


class MergeSort(SwapBasedSortMethod):
    def merge(self, left: List[int], right: List[int]):
        new_arr: List[int] = []
        ll = len(left)
        lr = len(right)

        il = ir = 0
        while il < ll and ir < lr:
            if left[il] < right[ir]:
                new_arr.append(left[il])
                il += 1
            else:
                new_arr.append(right[ir])
                ir += 1

        if il < ll:
            new_arr.extend(left[il:])
        else:
            new_arr.extend(right[ir:])

        return new_arr

    def merge_sort(self, arr: List[int]):
        length = len(arr)
        if length <= 1:
            return arr

        sep = length // 2

        left = self.merge_sort(arr[:sep])
        right = self.merge_sort(arr[sep:])

        return self.merge(left, right)

    def sort(self):
        return self.merge_sort(self.target)
