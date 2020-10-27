

class TypeMissMatchException(Exception):

    def __init__(self, discrepancies=[]):
        self.discrepancies = discrepancies

    def __str__(self):
        messages = []
        for discrepancy in self.discrepancies:
            message = f"""Invalid type of argument {discrepancy.argument}. Expect {discrepancy.expected_type}, not {discrepancy.argument_type}"""
            messages.append(message)
        delimeter = '\n'
        return delimeter + delimeter.join(messages)
