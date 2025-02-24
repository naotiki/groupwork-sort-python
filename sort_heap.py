from typing import List
from lib import SwapBasedSortMethod

class HeapSort(SwapBasedSortMethod):
    def heap(self, arr: List[int], parent: int, length: int):
        largest = parent
        left = 2 * parent + 1
        right = left + 1
        self.set("PARENT", parent)
        self.set("L", left)
        self.set("R", right)
        self.set("LARGEST", largest)
        if left < length and arr[left] > arr[largest]:
            largest = left
            self.set("LARGEST", left)
        if right < length and arr[right] > arr[largest]:
            largest = right
            self.set("LARGEST", right)
        if largest != parent:
            self.swap("PARENT", "LARGEST")
            #arr[parent], arr[largest] = arr[largest], arr[parent]
            self.heap(arr, largest, length)

    def build_heap(self, arr: List[int], length: int):
        i = len(arr) // 2 - 1
        while i >= 0:
            self.heap(arr, i, length)
            i -= 1

    def sort(self) -> List[int]:
        length = len(self.target)
        self.build_heap(self.target, length)
        for i in range(length - 1, -1, -1):
            self.set("L", 0)
            self.set("R", i)
            #self.target[0], self.target[i] = self.target[i], self.target[0]
            self.swap("L", "R")
            self.heap(self.target, 0, i)
        return self.target
