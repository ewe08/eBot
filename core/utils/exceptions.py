class NotEnoughTokensError(Exception):
    pass


class SendingToYourselfError(Exception):
    pass


class SendingToBotError(Exception):
    pass


class MessageInPrivateError(Exception):
    pass


class MessageInChatError(Exception):
    pass


class ExceededDailyLimitError(Exception):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit
