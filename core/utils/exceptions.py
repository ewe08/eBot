class NotEnoughTokensError(Exception):
    pass


class SendingToYourself(Exception):
    pass


class SendingToBot(Exception):
    pass


class ExceededDailyLimitError(Exception):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit
