import tkinter as tk
from tkinter import ttk
from typing import Dict, List
from sort_bubble import BubbleSort
from lib import SwapOp, SortMethod, Task, TkInterTasks
from sort_heap import HeapSort
from sort_insertion import InsertionSort
from sort_merge import MergeOp, MergeSort
from sort_quick import QuickSort
from sort_selection import SelectionSort


class App(tk.Tk):
    sort_methods: Dict[str, SortMethod] = {
        "Quick Sort": QuickSort(),
        "Bubble Sort": BubbleSort(),
        "Selection Sort": SelectionSort(),
        "Insertion Sort": InsertionSort(),
        "Heap Sort": HeapSort(),
        "Merge Sort": MergeSort(),
    }

    def __init__(self):
        super().__init__()

        self.tasks = TkInterTasks(self)

        sort_method_keys = list(self.sort_methods.keys())

        self.title("Super Sort App")
        self.geometry("900x600")

        entry_var = tk.StringVar(self, "4, 10, 5, 2, 1, 7, 8, 6, 3, 9")
        entry = tk.Entry(self, width=30, textvariable=entry_var)
        entry.grid(row=0, column=0, sticky="w")

        combobox = ttk.Combobox(self, values=sort_method_keys, state="readonly")
        combobox.set(sort_method_keys[0])
        combobox.grid(row=0, column=1, sticky="w")

        """ self.button = ttk.Button(
            text="Sort!",
            command=lambda: self.thread_sort(
                combobox.get(), [int(s) for s in entry_var.get().split(",")]
            ),
        ) """
        self.button = ttk.Button(
            text="Sort!",
            command=lambda: self.do_sort(
                combobox.get(),
                [int(s) for s in entry_var.get().split(",")],
            ),
        )
        self.button.grid(row=0, column=2, sticky="w")

        self.canvas = tk.Canvas(
            self, width=800, height=400, relief="ridge", borderwidth="2"
        )
        self.canvas.grid(row=1, column=0, columnspan=3)
        self.speed = tk.IntVar(self, 100)
        tk.Scale(
            self,
            from_=0,
            to=2000,
            orient="horizontal",
            variable=self.speed,
            command=lambda s: self.speed.set(int(float(s))),
            tickinterval=200,
            resolution=10,
            length=500,
        ).grid(row=2, column=0, columnspan=3)
        ttk.Label(self, text="Speed:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.speed).grid(row=3, column=1)

    def do_sort(
        self,
        sort_method: str,
        target_array: List[int],
    ):
        print("Sort started")

        self.button["state"] = "disable"
        sort_way = self.sort_methods[sort_method]
        sort_way.set_target_array(target_array.copy())
        result = sort_way.sort()
        print(result)
        array = target_array.copy()

        pointers: Dict[str, int] = {}

        def update_canvas(op, index):
            cell_size = 50
            self.canvas.delete("all")

            opcode = op[0]
            updated = []
            if opcode == SwapOp.SetPointer:
                [name, pos] = op[1]
                pointers[name] = pos
            elif opcode == SwapOp.Swap:
                [a, b] = op[1]
                a_i = pointers[a]
                b_i = pointers[b]
                tmp = array[a_i]
                array[a_i] = array[b_i]
                array[b_i] = tmp
                updated.append(a_i)
                updated.append(b_i)
            # main.pyのupdate_canvas関数内に追加
            if opcode == MergeOp.SetPointer:
                [name, pos] = op[1]
                pointers[name] = pos
            elif opcode == MergeOp.Update:
                [pos, value] = op[1]
                array[pos] = value
                updated.append(pos)
            elif opcode == MergeOp.Split:
                [split] = op[1]
                # 分割線と範囲を表示
                self.canvas.create_rectangle(
                    0, cell_size,  # 配列の下に表示
                    split * cell_size, cell_size + 10,
                    fill="lightblue",
                    outline="blue"
                )
                self.canvas.create_rectangle(
                    split * cell_size, cell_size,
                    len(array) * cell_size, cell_size + 10,
                    fill="lightgreen",
                    outline="green"
                )
                self.canvas.create_line(
                    split * cell_size, 0,
                    split * cell_size, cell_size + 10,
                    fill="blue",
                    width=10
                )
            elif opcode == MergeOp.Merge:
                [start, end] = op[1]
                # マージ範囲の表示
                self.canvas.create_rectangle(
                    start * cell_size, cell_size,
                    end * cell_size, cell_size + 10,
                    fill="yellow",
                    outline="orange"
                )
            for i, num in enumerate(array):
                x1 = i * cell_size
                x2 = x1 + cell_size
                y1 = 0
                y2 = cell_size
                has_marker = i in list(pointers.values())
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="black",  # 枠線を黒
                    fill=(
                        "red" if (i in updated) else "orange" if (has_marker) else ""
                    ),
                    tags=sort_method,
                )

                self.canvas.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2, text=str(num), tags=sort_method
                )
                if has_marker:
                    names = [a[0] for a in list(pointers.items()) if a[1] == i]
                    for i, n in enumerate(names):
                        self.canvas.create_text(
                            (x1 + x2) // 2,  # 中央に配置
                            y2 + (i + 1) * 20,  # 20ピクセルずつ下にずらす
                            text=n,
                            tags=sort_method,
                        )
            if index == len(sort_way.record) - 1:
                self.button["state"] = "enabled"

        for i, op in enumerate(sort_way.record):
            self.tasks.add_task(
                Task(
                    lambda: int(self.speed.get()),
                    lambda i=i, op=op: update_canvas(op, i),
                )
            )
        self.tasks.consume()


if __name__ == "__main__":
    app = App()
    app.mainloop()
