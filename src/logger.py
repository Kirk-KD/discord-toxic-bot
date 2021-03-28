from src.util.time import timestamp


class Logger:
    def __init__(self, fp: str):
        self.fp = fp
        with open(self.fp, "a") as f:
            f.write("\n")

    def log(self, log_type: str, log_msg: str=""):
        s = "* [{}] [{}] {}\n".format(timestamp(), log_type, log_msg).strip(" ")
        with open(self.fp, "a") as f:
            f.write(s)


logger = Logger("logs.txt")
