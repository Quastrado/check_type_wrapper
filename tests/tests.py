import unittest
from exception import TypeMissMatchException
from pythonfile import check_type


class DecoratorTest(unittest.TestCase):

    
    def test_decorator_no_exceptions(self):
        try:
            result = check_type(list)(lambda my_list: len(my_list) != len(set(my_list)))([1, '1'])
            self.assertEqual(result, None)
        except Exception as e: 
            self.fail(e.__str__)


    def test_decorator_type_missmatch_exception(self):
        with self.assertRaises(TypeMissMatchException) as ex:
            check_type(int, str)(lambda integer, string: (integer, string))('str', 'str')
        e = ex.exception.discrepancies
        self.assertEqual((1, 'int', 'str'), (len(e), e[0].expected_type, e[0].argument_type))
            


if __name__ == '__main__':
    unittest.main()
