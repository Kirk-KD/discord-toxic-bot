from src.util.time import timestamp


class Logger:
    def __init__(self, fp: str):
        self.fp = fp
        self.write_line()

    def log(self, log_type: str, log_msg: str = ""):
        s = "* [{}] [{}] {}\n".format(timestamp(), log_type, log_msg).strip(" ")
        with open(self.fp, "a") as f:
            f.write(s)

    def write_line(self, log_string: str = ""):
        with open(self.fp, "a") as f:
            f.write(log_string + "\n")


logger = Logger("logs.txt")
