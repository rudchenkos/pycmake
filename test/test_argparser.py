#!/usr/bin/python

import unittest
import sys
sys.path += '..'

from cmake.lang.argparser import *

class ArgumentListParsingTest(unittest.TestCase):
    
    def testParameterLexer(self):
        lexer = ParameterLexer('name value [CACHE [type]]')
        self.assertEqual('name', lexer.get_token())
        self.assertEqual('value', lexer.get_token())
        self.assertEqual('[', lexer.get_token())
        self.assertEqual('CACHE', lexer.get_token())
        self.assertEqual('[', lexer.get_token())
        self.assertEqual('type', lexer.get_token())
        self.assertEqual(']', lexer.get_token())
        self.assertEqual(']', lexer.get_token())
        self.assertEqual('', lexer.get_token())

    def testParameterLexerPutback(self):
        lexer = ParameterLexer('one four')
        self.assertEqual('one', lexer.get_token())
        lexer.put_token('two')
        lexer.put_token('three')
        self.assertEqual('two', lexer.get_token())
        self.assertEqual('three', lexer.get_token())
        self.assertEqual('four', lexer.get_token())
        self.assertEqual('', lexer.get_token())

    def testSpecParsing(self):
        params = parseParameterSpec('name value [CACHE [type]] [PARENT_SCOPE]')
        self.assertEqual(3, len(params))
        self.assertEqual(True, isinstance(params[0], RequiredParameter))
        self.assertEqual('name', params[0].name)

        self.assertEqual(True, isinstance(params[1], RequiredParameter))
        self.assertEqual('value', params[1].name)

        self.assertEqual(True, isinstance(params[2], AlternativesBlock))
        self.assertEqual(2, len(params[2].alternatives))

        self.assertEqual(True, isinstance(params[2].alternatives[0], OptionalBlock))
        cacheBlock = params[2].alternatives[0]
        self.assertEqual(2, len(cacheBlock.children))

        self.assertEqual(True, isinstance(cacheBlock.children[0], RequiredParameter))
        self.assertEqual('CACHE', cacheBlock.children[0].name)
        self.assertEqual(True, cacheBlock.children[0].is_keyword())

    def testParameterMathing(self):
        args = ['testName', 'testValue', 'CACHE', 'STRING', 'PARENT_SCOPE']
        match = matchParameters('name value [CACHE [type]] [PARENT_SCOPE]', args)
        self.assertEqual('testName', match['name'])
        self.assertEqual('testValue', match['value'])
        self.assertEqual(True, match['CACHE'])
        self.assertEqual('STRING', match['type'])

if __name__ == '__main__':
    unittest.main()
