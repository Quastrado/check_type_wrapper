

class CustomException(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        

    def __str__(self):
        if self.message:
            return f'{self.message}'
    

raise CustomException('ddd')