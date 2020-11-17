from functools import wraps, update_wrapper
import inspect
import types
from .discrepancy_item import DiscrepancyItem
from .exception import TypeMissMatchException


def args_matching(args_dict, types_dict, kwargs, ktypes):
    parameters_count_matching(args_dict, types_dict)
    all_args = dict(list(args_dict.items()) + list(kwargs.items()))
    all_types = dict(list(types_dict.items()) + list(ktypes.items()))
    discrepancies = []
    for key in all_args.keys():
        if isinstance(all_types[key], tuple):
            argument_type = all_types[key][0]
            expected_parameters_count = all_types[key][1]
            given_parameters_count = len(inspect.getfullargspec(all_args[key]).args)
            if expected_parameters_count != given_parameters_count:
                discrepancy_items = discrepancy_item(all_types[key], expected_parameters_count, given_parameters_count)
                discrepancies.append(discrepancy_items)
        if not isinstance(all_args[key], all_types[key]):
            discrepancy_items = discrepancy_item(key, all_types[key].__name__, type(all_args[key]).__name__)
            discrepancies.append(discrepancy_items)
    return discrepancies


def parameters_count_matching(args, types):
    if len(args) != len(types):
        raise Exception(
            'The number of passed arguments and types do not match!'
            )

def structure_converter(args, args_names):
    # return dict((args_names[index], args[index]) for index in range(len(args)))
    parameters_count_matching(args, args_names)
    comparison_dict = {}
    for index in range(len(args)):
        argument = args[index]
        if hasattr(argument, '__check_type__'):
            argument = argument.__check_type__['function']
        arg_name = args_names[index]
        comparison_dict[arg_name] = argument
    return comparison_dict 


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
