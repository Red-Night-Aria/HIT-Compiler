from http.server import HTTPServer, SimpleHTTPRequestHandler,CGIHTTPRequestHandler, HTTPStatus
from cgi import FieldStorage
from MyLexer import createMyLexer, tokens
from MySyntaxer import MySyntaxer
import sys
from io import StringIO
from prettytable import PrettyTable

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        print(self.path)
        if self.path == '/LifeIsSoHard':
            form = FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                        })
            # backup sysout
            systemOut = StringIO()
            stdout_bak = sys.stdout
            sys.stdout = systemOut
   
            Lexer.input(form['code'].value)
            tok = Lexer.token()
            printTable = PrettyTable(['type', 'attr', 'lineno', 'pos'])
            while tok:    
                if (tok.type != 'ID' and tok.type != 'REAL' and tok.type != 'INT'):
                    printTable.add_row([tok.type, '', tok.lineno, tok.lexpos])
                else:
                    printTable.add_row([tok.type, tok.value, tok.lineno, tok.lexpos])
                tok = Lexer.token()
            print(printTable)
            analyzer = MySyntaxer(Lexer, tokens, debug=False)
            analyzer.loadSytaxRule(StringIO(form['rule'].value))
            analyzer.printFirstSet()
            analyzer.printFollowSet()
            analyzer.printPredictTable()
            analyzer.analyze(form['code'].value)

            # recovery sysout
            sys.stdout = stdout_bak

            # return result to browser
            self.send_response(HTTPStatus.OK, "Script output follows")
            self.flush_headers()
            systemOut.seek(0)
            self.wfile.write(bytes("Content-Type: text/html\n\n"+systemOut.read(), encoding='utf8'))
        else:
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.flush_headers()

server_address = ('', 23456)
Lexer = createMyLexer()

httpd = HTTPServer(server_address, MyHandler)
print("server are running at port 23456.")
httpd.serve_forever()