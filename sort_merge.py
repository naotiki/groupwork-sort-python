from dataclasses import field
from enum import Enum
from typing import Dict, List
from lib import SortMethod

class MergeOp(Enum):
    SetPointer = 1  # ポインターの位置設定
    Split = 2       # 配列の分割
    Update = 3      # 要素の更新
    Merge = 4       # マージ完了

class MergeSort(SortMethod[MergeOp, List[str | int]]):
    pointers: Dict[str, int] = field(default_factory=dict)
    temp_array: List[int] = field(default_factory=list)
    
    def reset(self):
        super().reset()
        self.pointers = {}
        self.temp_array = [0] * len(self.target)
    
    def set(self, name: str, pos: int):
        self.record.append((MergeOp.SetPointer, [name, pos]))
        self.pointers[name] = pos
    
    def split(self, split: int):
        self.record.append((MergeOp.Split, [split]))
    
    def update(self, pos: int, value: int):
        self.record.append((MergeOp.Update, [pos, value]))
        self.target[pos] = value
    
    def do_merge(self, start: int, mid: int, end: int):
        # 作業用配列にコピー
        for i in range(start, end):
            self.temp_array[i] = self.target[i]
        
        i = start
        il = start
        ir = mid
        
        while il < mid and ir < end:            
            if self.temp_array[il] < self.temp_array[ir]:
                self.update(i, self.temp_array[il])
                il += 1
            else:
                self.update(i, self.temp_array[ir])
                ir += 1
            i += 1
        
        # 残りの要素をコピー
        # new_arr.extend(left[il:])
        while il < mid:
            self.update(i, self.temp_array[il])
            il += 1
            i += 1
        # new_arr.extend(right[ir:])
        while ir < end:
            self.update(i, self.temp_array[ir])
            ir += 1
            i += 1
        
        self.record.append((MergeOp.Merge, [start, end]))

    def merge_sort(self, start: int, end: int):
        if end - start <= 1:
            return
        
        mid = (start + end) // 2
        self.split(mid)
        
        self.merge_sort(start, mid)
        self.merge_sort(mid, end)
        self.do_merge(start, mid, end)

    def sort(self):
        self.temp_array = [0] * len(self.target)
        self.merge_sort(0, len(self.target))
        return self.target