class ExpressionError(Exception):
    def __init__(self, msg):
        super().__init__(f'ExpressionError: {msg}')