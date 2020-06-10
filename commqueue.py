import queue
import itertools


class CommandsPriorityQueue:
    def __init__(self, capacity=0):
        self.__queue = queue.PriorityQueue(capacity)
        self.__iter = itertools.count(start=0, step=1)

    def add_command(self, command, priority, block=False, timeout=None):
        self.__queue.put((priority, next(self.__iter), command), block, timeout)

    def pop(self, block=False, timeout=None):
        prio, count, command = self.__queue.get(block, timeout)
        return command

    def empty(self):
        return self.__queue.empty()

    def size(self):
        return self.__queue.qsize()
