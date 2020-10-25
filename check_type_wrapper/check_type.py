from .discrepancy_item import DiscrepancyItem
from .exception import TypeMissMatchException


def args_matching(args, types, kwargs, ktypes):
    if len(args) != len(types):
        raise Exception('The number of passed arguments and types do not match!')
    args_dict = structure_converter(args)
    all_args = dict(list(args_dict.items()) + list(kwargs.items()))
    types_dict = structure_converter(types)
    all_types = dict(list(types_dict.items()) + list(ktypes.items()))
    discrepancies = []
    for key in all_args.keys():
        if key not in all_types.keys():
            continue
        if not isinstance(all_args[key], all_types[key]): 
            discrepancy_items = DiscrepancyItem(
                argument=all_args[key],
                expected_type=all_types[key].__name__,
                argument_type=type(all_args[key]).__name__
                )
            discrepancies.append(discrepancy_items)
    return discrepancies


def structure_converter(args):
    return dict((str(index), args[index]) for index in range(len(args)))


def check_type(*types, **ktypes):
    def decorator(func):
        def wrapper(*args, **kwargs):
            discrepancies = args_matching(args, types, kwargs, ktypes)
            if len(discrepancies) > 0:
                raise TypeMissMatchException(discrepancies)
        return wrapper
    return decorator
