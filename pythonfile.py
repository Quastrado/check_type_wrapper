from exception import CustomException

user_list = ['a', 'b', 1, 'c']
string = 'a'
var2 = 2


# def my_func(my_list):
#     if not isinstance(my_list, list):
#         raise Exception('asjsdkfgsdgfks')
    
#     return len(my_list) != len(set(my_list))
    
# print(my_func(my_list))

def args_matching(args, types):
    if len(args) != len(types):
        raise Exception('The number of passed arguments and types do not match!')
    discrepancies = []
    for key in args.keys():
        if not isinstance(args[key], types[key]):
            discrepancies.append((args[key], types[key].__name__, type(args[key]).__name__))
    return discrepancies


def structure_converter(args):
    return dict((str(index), args[index]) for index in range(len(args)))


def check_type(*types, **ktypes):
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_dict = structure_converter(args)
            all_args = dict(list(args_dict.items()) + list(kwargs.items()))

            types_dict = structure_converter(types)
            all_types = dict(list(types_dict.items()) + list(ktypes.items()))
            discrepancies = args_matching(all_args, all_types)
            if len(discrepancies) > 0:
                raise CustomException(discrepancies)
            #return func(*args, **kwargs)
        return wrapper
    return decorator

# def hz(*args, **kwargs):
#     args_dict = structure_converter(args)
#     all_args = dict(list(args_dict.items()) + list(kwargs.items()))


# def check_type(*types, **ktypes):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             args_matching(hz(args, kwargs), hz(types, ktypes))
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

# def hz(*args, **kwargs):
#     return dict(list(structure_converter(args).items()) + list(kwargs.items()))


@check_type(list, int, string=str, another_list=list)
def my_func(my_list, integer, string='some string', another_list=None):
    return len(another_list) != len(set(another_list))


@check_type(z_type=int, x_type=int, y_type=str)
def inc(z, x=1, y='a'):
    return x + 1

# @check_type(x=Point, y=Point)
# def sum(x, y):
#     return x + y

print(my_func(user_list, 'a', string=1, another_list=[1, 1, '1']))
# print(my_func(user_list, 5, another_list=[1, 1, '1'], string='some string'))
# print(my_func(10, 5, another_list=3, string='some string'))

