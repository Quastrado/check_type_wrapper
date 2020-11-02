import inspect
import types
import unittest
from check_type_wrapper.exception import TypeMissMatchException
from check_type_wrapper.check_type import check_type


class DecoratorTest(unittest.TestCase):

    
    def test_expected_return(self):
        result = check_type(int)(lambda my_int: my_int)(5)
        self.assertEqual(result, 5)


    def test_without_specifying_types(self):
        try:
            result = check_type()(lambda my_int: my_int)(5)
        except Exception as e:
            self.assertEqual(
                e.args[0],
                'The number of passed arguments and types do not match!'
                )


    def test_without_expected_arguments(self):
        try:
            result = check_type(int)(lambda my_int: my_int)()
        except Exception as e:
            self.assertEqual(
                e.args[0],
                'The number of passed arguments and types do not match!'
                )

    def test_int_type_match(self):
        function = lambda my_int, another_int: my_int + another_int
        result = check_type(int, int)(function)(5, 1)
        self.assertEqual(result, 6)

    
    def test_type_mismatch_int(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_int, another_int: my_int + another_int
            result = check_type(int, int)(function)(5, '1')


    def test_type_match_float(self):
        function = lambda my_float, my_int: my_float + my_int
        result = check_type(float, int)(function)(1.1, 1)
        self.assertEqual(result, 2.1)
    
    
    def test_type_mismatch_float(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_float, my_int: my_float + my_int
            result = check_type(float, int)(function)(1, '1')


    def test_type_match_complex(self):
        function = lambda my_complex, my_int: my_complex + my_int
        result = check_type(complex, int)(function)(1+2j, 1)
        self.assertEqual(result, 2+2j)
    
    
    def test_type_mismatch_complex(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_complex, my_int: my_complex + my_int
            result = check_type(int, str)(function)(1+2j, '1')


    def test_str_type_match(self):
        function = lambda my_str, another_str: my_str + another_str
        result = check_type(str, str)(function)('5', '1')
        self.assertEqual(result, '51')
    
    
    def test_type_mismatch_str(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_str, another_str: my_str + another_str
            result = check_type(str, str)(function)(5, '1')


    def test_list_type_match(self):
        function = lambda my_list: my_list
        result = check_type(list)(function)(['a', 2, 'c'])
        self.assertEqual(result, ['a', 2, 'c'])
    
    
    def test_type_mismatch_list(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_list: my_list
            result = check_type(list)(function)(('a', 2, 'c'))


    def test_tuple_type_match(self):
        function = lambda my_tuple: my_tuple
        result = check_type(tuple)(function)(('a', 2, 'c'))
        self.assertEqual(result, ('a', 2, 'c'))
    
    
    def test_type_mismatch_tuple(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_list: my_list
            result = check_type(tuple)(function)(['a', 2, 'c'])


    def test_set_type_match(self):
        function = lambda my_set: my_set
        result = check_type(set)(function)({'a', 2, 'c'})
        self.assertEqual(result, {'a', 2, 'c'})
    
        
    def test_type_mismatch_set(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_set: my_set
            result = check_type(set)(function)(['a', 2, 'c'])


    def test_dict_type_match(self):
        function = lambda my_dict: my_dict
        result = check_type(dict)(function)({'key': 'value'})
        self.assertEqual(result, {'key': 'value'})
    
    
    def test_type_mismatch_dict(self):
        with self.assertRaises(TypeMissMatchException) as e:
            function = lambda my_dict: my_dict
            result = check_type(dict)(function)(['a', 2, 'c'])

                
    def test_decorator_no_exceptions(self):
        try:
            result = check_type(list)(lambda my_list: len(my_list) != len(set(my_list)))([1, '1'])
            self.assertEqual(result, False)
        except Exception as e: 
            self.fail(e.__str__)


    def test_decorator_type_missmatch_exception(self):
        with self.assertRaises(TypeMissMatchException) as ex:
            check_type(int, str)(lambda integer, string: (integer, string))('str', 'str')
        e = ex.exception.discrepancies
        self.assertEqual((1, 'int', 'str'), (len(e), e[0].expected_type, e[0].argument_type))


    def test_function_as_argument_success(self):
        func_type = types.FunctionType
        argument_function = lambda some_int: some_int + 1
        result = check_type(func_type, int)(lambda func, some_int: func(some_int))(argument_function, 12)
        self.assertEqual(result, 13)
    
    
    def test_function_as_argument_type_missmatch(self):
        with self.assertRaises(TypeMissMatchException):
            func_type = types.FunctionType
            argument_function = lambda some_int: some_int + 1
            result = check_type(func_type, int)(lambda func, some_int: func(some_int))(argument_function, '12')


    def test_function_as_argument_args_type_count_missmatch(self):
        with self.assertRaises(Exception) as e:
            func_type = types.FunctionType
            argument_function = lambda some_int: some_int + 1
            result = check_type(func_type)(lambda func, some_int: func(some_int))(argument_function, '12')
            self.assertEqual(str(e), 'The number of passed arguments and types do not match!')
    
    
    def test_function_argument_name(self):
        try:
            function = lambda my_int: my_int           
            result = check_type(int)(function)('1')
        except Exception as e:
            discrepancies_argument = e.discrepancies[0].argument
            function_argument = inspect.getfullargspec(function).args[0]
            self.assertEqual(discrepancies_argument, function_argument)

    
    def test_tuple_as_decorator_parameter(self):
        function_type = types.FunctionType
        function = lambda some_function, some_int: some_function(some_int)
        argument_function = lambda some_int: some_int
        result = check_type((function_type, 1), int)(function)(argument_function, 12)
        self.assertEqual(result, 12)


    def test_forgotten_tuple_structure(self):
        with self.assertRaises(Exception):
            function_type = types.FunctionType
            function = lambda some_function, some_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type(function_type, 1, int)(function)(argument_function, 12)


    def test_forgotten_arguments_count_in_tuple(self):
        with self.assertRaises(Exception):
            function_type = types.FunctionType
            function = lambda some_function, some_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type((function_type,), int)(function)(argument_function, 12)


    def test_argument_tuple_in_discreapancies(self):
        try:
            function_type = types.FunctionType
            function = lambda some_function, some_int, another_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type((function_type, 2), int)(function)(argument_function, 12)
        except Exception as e:
            argument = (function_type, 2)
            discrepancies_argument = e.discrepancies[0].argument
            self.assertEqual(discrepancies_argument, argument)


    def test_miss_specifying_a_function(self):
        try:
            function_type = types.FunctionType
            function = lambda some_function, some_int, another_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type((2,), int)(function)(argument_function, 12)
        except Exception as e:
            message = 'tuple index out of range'
            self.assertEqual(str(e), message)
    
    
    def test_pass_function_not_in_tuple(self):
        try:
            function_type = types.FunctionType
            function = lambda some_function, some_int, another_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type(function_type, int)(function)(argument_function, 12)
        except Exception as e:
            message = "<lambda>() missing 1 required positional argument: 'another_int'"
            self.assertEqual(str(e), message)
    
    
    def test_tuple_in_discreapancies_expected_arguments_count(self):
        try:
            function_type = types.FunctionType
            function = lambda some_function, some_int, another_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type((function_type, 2), int)(function)(argument_function, 12)
        except Exception as e:
            expected_arguments_count = 2
            discrepancies_expected_type = e.discrepancies[0].expected_type
            self.assertEqual(discrepancies_expected_type, expected_arguments_count)


    def test_tuple_in_discreapancies_given_arguments_count(self):
        try:
            function_type = types.FunctionType
            function = lambda some_function, some_int, another_int: some_function(some_int)
            argument_function = lambda some_int: some_int
            result = check_type((function_type, 2), int)(function)(argument_function, 12)
        except Exception as e:
            given_arguments_count = 1
            discrepancies_argument_type = e.discrepancies[0].argument_type
            self.assertEqual(discrepancies_argument_type, given_arguments_count)



if __name__ == '__main__':
    unittest.main()
# write more tests for decorator and funk as argument