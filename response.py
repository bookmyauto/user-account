class Response:
    def make_error(self, **kwargs):
        error   = {}
        for key, value in kwargs.items:
            error[str(key)]     = value

