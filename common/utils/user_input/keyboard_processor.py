import pygame
import time


USER_KEYBOARD_EVENTS = [pygame.KEYDOWN, pygame.KEYUP]


class UserKeyboardProcessor:
    def __init__(self, delay: float = 0.6):
        self.__last_pressed_key = None
        self.__time_press = 0.0
        self.__delay = delay
        self.__flag_first_time_process = True

    def process_input(self):
        """
        Передавать только эвенты, которые отвечают keyboard
        """
        for event in pygame.event.get(USER_KEYBOARD_EVENTS):
            self._process_key_event(event)
        return self._final_key()

    def _process_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.__last_pressed_key = event.key
            self.__time_press = time.time()
            self.__flag_first_time_process = True
        elif event.type == pygame.KEYUP:
            if event.key == self.__last_pressed_key:
                self.__last_pressed_key = None

    def _final_key(self):
        """
        Обрабатывается первая нажатая клавиша;
        если клавиша нажата более self._delay секунд, то она также
        пораждает соответствующую ей команду;
        если несколько клавиш нажаты более self._delay секунд,
        то пораждает команду та, которая нажата дольше всего;
        если не нажата ни одна, то возвращается None
        """
        if self.__last_pressed_key is None:
            return None
        if self.__flag_first_time_process:
            self.__flag_first_time_process = False
            return self.__last_pressed_key
        else:
            current_time = time.time()
            delta = current_time - self.__time_press
            if delta > self.__delay:
                return self.__last_pressed_key
            else:
                return None
