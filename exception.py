

class CustomException(Exception):

    def __init__(self, *args):
        if args:
            self.discrepancies = args[0]


    def __str__(self):
        messages = []
        for discrepancy in self.discrepancies:
            messages.append(f'Invalid type of argument {discrepancy[0]}. Expect {discrepancy[1]}, not {discrepancy[2]}')
        return str('\n'.join(messages))
    
    

# d = {1: '1'}
# raise CustomException('ddd', d)

