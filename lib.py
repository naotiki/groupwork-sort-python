from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from tkinter import Tk
from typing import Dict, List, Tuple, Callable


# GUIでソートをリプレイするための操作一覧
class Op(Enum):
    SetPointer = 1
    Swap = 2


@dataclass
class SortMethod(metaclass=ABCMeta):
    pointers: Dict[str, int] = field(default_factory=dict)
    target: List[int] = field(default_factory=list)
    # 操作のログ
    record: List[Tuple[Op, List[str | int]]] = field(default_factory=list)

    # Set pointer to pos
    def set(self, name: str, pos: int):
        self.record.append((Op.SetPointer, [name, pos]))
        self.pointers[name] = pos

    def dec(self, name: str):
        self.add(name, -1)

    def inc(self, name: str):
        self.add(name, +1)

    def add(self, name: str, value: int):
        self.set(name, self.get(name) + value)

    def get(self, name: str) -> int:
        if name not in self.pointers.keys():
            raise ValueError(
                f"defined pointers are {self.pointers.keys()} but passed {name}"
            )
        return self.pointers[name]

    def swap(self, a: str, b: str):
        if a not in self.pointers.keys() or b not in self.pointers.keys():
            raise ValueError(
                f"defined pointers are {self.pointers.keys()} but passed {a},{b}."
            )
        self.record.append((Op.Swap, [a, b]))
        i = self.pointers[a]
        j = self.pointers[b]
        self.target[i], self.target[j] = self.target[j], self.target[i]

    def reset(self):
        self.target = []
        self.pointers = {}
        self.record = []

    def set_target_array(self, arr: List[int]):
        self.reset()
        self.target = arr.copy()

    @abstractmethod
    def sort(self) -> List[int]:
        pass


@dataclass
class Task:
    delay_ms: int
    task: Callable[[], None]


class TkInterTasks:
    def __init__(self, tk: Tk):
        self.tasks: Dict[str, List[Task]] = {}
        self.progress: Dict[str, int] = {}
        self.tk = tk

    def add_task(self, task: Task, key: str = ""):
        if key not in self.tasks:
            self.tasks[key] = []
        self.tasks[key].append(task)

    def consume(self, key: str = ""):
        if key not in self.tasks:
            return
        self.progress[key] = 0
        task = self.tasks[key][0]
        self.tk.after(
            task.delay_ms,
            lambda b=task.task, k=key: self.do_recursive(b, k)(),
        )

    def next_task(self, key: str):
        self.progress[key] += 1
        if self.progress[key] >= len(self.tasks[key]):
            return None
        return self.tasks[key][self.progress[key]]

    def do_recursive(self, body: Callable[[], None], key: str):
        def inner():
            body()
            next = self.next_task(key)
            if next is None:
                self.progress[key] = 0
                self.tasks[key].clear()
                return None
            return self.tk.after(
                next.delay_ms,
                lambda b=next.task, k=key: self.do_recursive(b, k)(),
            )

        return inner
