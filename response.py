class Response:

    '''
    create an error data
    '''
    def make_error(self, error_code, error_message, display_message):
        error                       = {}
        error["error_code"]         = str(error_code)
        error["error_message"]      = str(error_message)
        error["display_message"]    = str(display_message)
        return error

    '''
    create a result data
    '''
    def make_result(self, result_code, result_message, display_message):
        result                      = {}
        result["result_code"]        = str(result_code)
        result["result_message"]     = str(result_message)
        result["display_message"]    = str(display_message)
        return result