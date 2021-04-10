from src.bot.util.time import timestamp


class LoggerRecord:
    def __init__(self, log_type: int, log_name: str, log_msg: str = ""):
        self.log_time = timestamp()
        self.log_type = log_type
        self.log_name = log_name
        self.log_msg = log_msg

    def get_html(self):
        return "<p style='color: {};'><b>[{}] [{}]</b> {}</p>"\
            .format(["#000000", "#fcdb03", "#ff0000"][self.log_type],
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
        s = "* [{}] [{}] {}\n".format(timestamp(), log_name, log_msg).strip(" ")
        with open(self.fp, "a") as f:
            f.write(s)

        self.logs.append(LoggerRecord(log_type, log_name, log_msg))

    def info(self, log_msg: str = ""):
        self.log(0, "INFO", log_msg)

    def warn(self, log_msg: str = ""):
        self.log(1, "WARN", log_msg)

    def error(self, log_msg: str = ""):
        self.log(2, "ERROR", log_msg)

    def write_line(self, log_string: str = ""):
        with open(self.fp, "a") as f:
            f.write(log_string + "\n")


logger = Logger("logs.txt")
