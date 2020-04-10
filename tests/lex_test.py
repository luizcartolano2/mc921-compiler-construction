# imports
import unittest
from uc_lex import UCLexer
import os


class ucLexTestSuite(unittest.TestCase):


    def print_error(self, msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y))


    def setUp(self):
        """ Executed before every test case """
        # create lexer obj
        self.lexer = UCLexer(self.print_error)
        # build the lexer
        self.lexer.build()
        # setup files
        self.test_inputs = os.path.join(os.getcwd(),'test_cases/')
        self.test_results = os.path.join(os.getcwd(),'test_results/')


    def tearDown(self):
        """ Executed after every test case """
        del self.lexer
        print("\ntearDown executing after the test case. Result:")


    def run_test_case(self, test_case):
        # get the test result
        with open(os.path.join(self.test_results, 'test' + str(test_case) + '.txt')) as f:
            result = f.read()
        
        # get the output
        with open(os.path.join(self.test_inputs, 'test' + str(test_case) + '.txt')) as f:
            output = self.lexer.scan(f.read())
        
        # assert result
        self.assertEqual(output, result)


    def test_1(self):
        self.run_test_case(1)


    def test_2(self):
        self.run_test_case(2)


    def test_3(self):
        self.run_test_case(3)


    def test_4(self):
        self.run_test_case(4)


    def test_5(self):
        self.run_test_case(5)

    
    def test_6(self):
        self.run_test_case(6)        

if __name__ == '__main__':
    unittest.main()

