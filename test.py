'''
    code for test
    
    TODO unit test
'''
from MyLexer import createMyLexer, tokens
from MySyntaxer import MySyntaxer
import sys
import os

testCode = '''
integer [3] a; integer [10] b;
float [3][5] d;
boolean e;

a[2] = b[3+4]+(4+7);

if (4+7<0) a[1]=a[1]+1;

while (1>2+4)
    d[1][2] = 1.1;    

define integer foo(integer f){
    f = 5323;
    return f;
}

a[1] = 1 + foo(21);
'''


typeErrorCode = '''
integer [1][2] a;
a[1] = 3;
'''

declareErrorCode = '''
boolean a;
float a;
'''

syntaxErrorRecoveryCode = '''
integer +a;
+boolean b;
'''

arraySubErrorCode = '''
boolean [1] a;
a[1][2] = 1;
'''

arrayTypeErrorCode = '''
boolean[1] a;
a[1.1] = 2;
'''

declareCode = "integer [2][3][5]"
declareSeqCode = "integer a;boolean[1][2] b;float c;"
simpleAssign = "integer[2] a; a[1]=1; a[2]=a[1];"
ifCode = "integer a; if (a<3 || false) a = 100;"
whileCode = "integer b; while (b>3) b = b + 1;"
functionCode = "define boolean f(integer a, integer b){a = a + b;}"
syntaxErrorCode = "integer +a; +boolean b;"

lexer = createMyLexer() 
mySytaxer = MySyntaxer(lexer, tokens, debug=True)
mySytaxer.loadSytaxRule(open('LL_with_action.txt'))
mySytaxer.analyze(functionCode)