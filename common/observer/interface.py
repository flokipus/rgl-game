from typing import overload

from common.event.event import Event


class Observer:
    @overload
    def on_notify(self, subject, event: Event) -> None: ...

    def on_notify(self, subject, event: Event) -> None:
        pass


class Subject:
    def __init__(self):
        self._observers = []

    @overload
    def register_observer(self, observer: Observer) -> None: ...

    @overload
    def remove_observer(self, observer: Observer) -> None: ...

    @overload
    def notify(self, event: Event) -> None: ...

    def register_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: Event) -> None:
        for observer in self._observers:
            observer.on_notify(subject=self, event=event)
