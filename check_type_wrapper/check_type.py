import inspect
import types
from .discrepancy_item import DiscrepancyItem
from .exception import TypeMissMatchException


def args_matching(args_dict, types_dict, kwargs, ktypes):
    if len(args_dict) != len(types_dict):
        raise Exception(
            'The number of passed arguments and types do not match!'
            )
    all_args = dict(list(args_dict.items()) + list(kwargs.items()))
    all_types = dict(list(types_dict.items()) + list(ktypes.items()))
    discrepancies = []
    for key in all_args.keys():
        if isinstance(all_types[key], tuple):
            argument_type = all_types[key][0]
            expect_parameters_count = all_types[key][1]
            given_parameters_count = len(inspect.getfullargspec(all_args[key]).args)
            if expect_parameters_count != given_parameters_count: #create discrepancy object
                discrepancy_items = discrepancy_item(all_types[key], expect_parameters_count, given_parameters_count)
                discrepancies.append(discrepancy_items)
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
        return wrapper
    return decorator
