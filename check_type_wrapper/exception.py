

class TypeMissMatchException(Exception):

    def __init__(self, discrepancies=[]):
        self.discrepancies = discrepancies

    def __str__(self):
        messages = []
        for discrepancy in self.discrepancies:
            message = 'Invalid type of argument {0}. Expect {1}, not {2}'.format(
                discrepancy.argument,
                discrepancy.expected_type,
                discrepancy.argument_type
                )
            messages.append(message)
        delimeter = '\n'
        return delimeter + delimeter.join(messages)
