class InvalidADSetup(Exception):
    """Exception when any information regarding AD test setup is incorrect/missing

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidINIFile(Exception):
    """Exception when invalid information is provied in INI file

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)


class PSExecutionException(Exception):
    """Exception when PS Execution did not complete successfully

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)

class InvalidTestSuite(Exception):
    """Exception when test suite format is incorrect

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)
