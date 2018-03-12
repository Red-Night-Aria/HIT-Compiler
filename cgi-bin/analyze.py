import cgi
import sys
import os.path
from io import StringIO

'''处理模块路径问题'''
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from MySyntaxer import MySyntaxer
from MyLexer import createMyLexer, tokens

print("Content-Type: text/html")
print()          

try:
    form = cgi.FieldStorage()
    Lexer = createMyLexer()
    Lexer.input(form['code'].value)
    tok = Lexer.token()
    while tok:
        print(tok)
        tok = Lexer.token()
    analyzer = MySyntaxer(Lexer, tokens, debug=False)
    analyzer.loadSytaxRule(StringIO(form['rule'].value))
    analyzer.analyze(form['code'].value)
except Exception as e:
    print(e)
