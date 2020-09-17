

class CustomException(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.discrepancies = args[1]
        

    def __str__(self):
        if self.message:
            return (f'{self.message}', self.discrepancies)


    
    

d = {1: '1'}
raise CustomException('ddd', d)