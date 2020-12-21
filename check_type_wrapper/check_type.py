import types
from discrepancy_item import DiscrepancyItem
from exception import TypeMissMatchException


def lambda_args_matching(lambda_func, lambda_params):
    discrepancies = []
    req_types = [param for param in lambda_params if param != types.FunctionType]
    passed_types = list(lambda_func.__check_type__['types']) if hasattr(lambda_func, '__check_type__') else lambda_func.__code__.co_varnames   #try to rewrite
    if len(req_types) != len(passed_types):
        return [DiscrepancyItem(
            argument=lambda_params[0].__name__,
            expected_type=lambda_params[0].__name__,
            argument_type=type(lambda_func).__name__ 
        )]

    if not hasattr(lambda_func, '__check_type__'):
        return discrepancies

    for passed_type, req_type in zip(passed_types, req_types):
        if passed_type == req_type:
            if isinstance(passed_type, tuple):
                d = lambda_args_matching(lambda_func.__check_type__['function'], lambda_func.__check_type__['types'])
            continue
        discrepancies.append(DiscrepancyItem(
            argument=passed_type,
            expected_type=req_type.__name__,
            argument_type=passed_type.__name__
        ))
    return discrepancies
    

def args_matching(args_dict, types_dict, kwargs, ktypes):
    if len(args_dict) != len(types_dict):
        raise Exception(
            'The number of passed arguments and types do not match!'
            )
    all_args = dict(list(args_dict.items()) + list(kwargs.items()))
    all_types = dict(list(types_dict.items()) + list(ktypes.items()))
    discrepancies = []
    for key in all_args.keys():
        if isinstance(all_args[key], types.FunctionType):
            discrepancies+=lambda_args_matching(all_args[key], all_types[key])
        
        if not isinstance(all_args[key], all_types[key]):
            discrepancy_items = discrepancy_item(key, all_types[key].__name__, type(all_args[key]).__name__)
            discrepancies.append(discrepancy_items)
    return discrepancies


def structure_converter(args, args_names):
    return dict((args_names[index], args[index]) for index in range(len(args)))


def discrepancy_item(argument, expected_type, argument_type):
    return DiscrepancyItem(
        argument=argument,
        expected_type=expected_type,
        argument_type=argument_type
        )


def check_type(*types, **ktypes):
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_names = inspect.getfullargspec(func).args
            args_dict = structure_converter(args, args_names)
            types_dict = structure_converter(types, args_names)
            discrepancies = args_matching(args_dict, types_dict, kwargs, ktypes)
            if len(discrepancies) > 0:
                raise TypeMissMatchException(discrepancies)
            return_value = func(*args, **kwargs)
            return return_value
        wrapper.__check_type__ = {'function': func, 'types': types, 'ktypes': ktypes}
        return wrapper
    return decorator
