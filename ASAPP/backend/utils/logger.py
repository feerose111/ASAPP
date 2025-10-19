from abc import ABC, abstractmethod
import datetime
import os
import json

# --- Log Levels ---
# INFO = "INFO"
# WARNING = "WARNING"
# ERROR = "ERROR"


# --- Observer Interface ---
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict, level: str):
        pass

# --- Subject (Observable) ---
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict, level: str):
        for observer in self._observers:
            observer.update(event_type, data, level)


# --- Concrete Observers ---
class ConsoleLogger(Observer):
    def update(self, event_type: str, data: dict, level: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {event_type}: {data}")


class JSONFileLogger(Observer):
    def __init__(self, base_dir="logs"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def update(self, event_type: str, data: dict, level: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "event_type": event_type,
            "data": data
        }

        filename = os.path.join(self.base_dir, f"{level}.json")
        with open(filename, "a", encoding="utf-8") as f:
            json.dump(log_entry, f)
            f.write("\n")

# --- Logger Manager ---
class LoggerManager(Subject):
    def __init__(self, use_console: bool = False):
        """if use_console=True, logs also print to console."""
        super().__init__()
        self.attach(JSONFileLogger())
        if use_console:
            self.attach(ConsoleLogger())

    def log(self, level: str, event_type: str, data: dict):
        self.notify(event_type, data, level)
