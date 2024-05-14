import threading
import time

class Timer:

    def __init__(self, duration):
        self.__duration = duration
        self.__is_running = False
        self.__thread = None
        self.__stop_thread = threading.Event()

    @property
    def duration(self):
        return self.__duration

    @property
    def is_running(self):
        return self.__is_running

    @duration.setter
    def duration(self, time):
        try:
            self.__duration = int(time)
        except ValueError:
            print("\033[31m" + "Ошибка: Количество секунд должно быть целым числом." + "\033[0m")

    def reset(self):
        self.__duration = 0
        self.__is_running = False
        self.__thread = None

    def start(self):
        if not self.__is_running:
            self.__is_running = True
            self.__thread = threading.Thread(target=self.run)
            self.__thread.start()

    def stop(self):
        self.__stop_thread.set()
        self.__thread.join()

    def run(self):
        while self.__is_running and self.__duration > 0:
            time.sleep(1)
            self.__duration -= 1
            if self.__duration == 0 and self.__is_running:
                self.__is_running = False
            if self.__stop_thread.is_set():
                break