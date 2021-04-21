import datetime
from termcolor import colored

from src.util.time import timestamp, format_time


class Timer:
    def __init__(self):
        self.start = datetime.datetime.now()

    def get_ms(self):
        return int((datetime.datetime.now() - self.start).total_seconds() * 1000)


class LoggerRecord:
    def __init__(self, log_type: int, log_name: str, log_msg: str = ""):
        self.log_time = timestamp()
        self.log_type = log_type
        self.log_name = log_name
        self.log_msg = log_msg

    def get_html(self):  # for control_panel
        return "<p style='color: {};'><b>[{}] [{}]</b> {}</p>"\
            .format(["#000000", "#fcdb03", "#ff0000", "#0000ff"][self.log_type],
                    self.log_time.replace("<", "&lt;").replace(">", "&gt;"),
                    self.log_name.replace("<", "&lt;").replace(">", "&gt;"),
                    self.log_msg.replace("<", "&lt;").replace(">", "&gt;").
                    replace(" ", "&nbsp;").replace("\t", "&nbsp;" * 4))\
            .replace("\n", "<br>")


class Logger:
    def __init__(self, fp: str):
        self.fp = fp
        self.write_line()

        self.logs = []

    def log(self, log_type: int, log_name: str, log_msg: str = ""):
        s = " " + ("- [{}] [{}] {}".format(timestamp(), log_name, log_msg).strip())
        print(colored(s, color=[None, "yellow", "red", "blue"][log_type]))

        with open(self.fp, "a") as f:
            f.write(s)

        self.logs.append(LoggerRecord(log_type, log_name, log_msg))

    def info(self, log_msg: str = ""):
        self.log(0, "INFO", log_msg)

    def warn(self, log_msg: str = ""):
        self.log(1, "WARN", log_msg)

    def error(self, log_msg: str = ""):
        self.log(2, "ERROR", log_msg)

    def timed(self, timer: Timer, event_name: str):
        self.log(3, "TIMED", "EVENT \"{}\": START={} | END={} | {}ms".format(
            event_name, format_time(timer.start), format_time(datetime.datetime.now()), timer.get_ms()
        ))

    def write_line(self, log_string: str = ""):
        with open(self.fp, "a") as f:
            f.write(log_string + "\n")


logger = Logger("logs.txt")
