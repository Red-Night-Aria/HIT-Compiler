from prettytable import PrettyTable
from SDTUtil import SDTUtil
from symbolTable import SymbolTable

class MySyntaxer:
    def loadSytaxRule(self, fp):
        self.PSet = {}
        self.APSet = {} #APSet: 包含动作片段的产生式
        flag = True
        tokens_S = self.tokens.copy()
        for rule in fp.readlines():
            rule = rule.strip()
            Left, Right = rule.split('->')
            if not self.PSet.get(Left):
                self.PSet[Left] = []
                self.APSet[Left] = []
            self.APSet[Left].append(Right.split(' '))
            self.PSet[Left].append([])
                
            for tok in self.APSet[Left][-1]:
                if tok in tokens_S:
                    tokens_S.remove(tok)
                if not tok.startswith('act'):
                    self.PSet[Left][-1].append(tok)

            '''记录文法开始符号'''
            if flag:
                flag = False
                self.begin = Left
        '''删除未出现的词法单元'''
        for tok in tokens_S:
            self.tokens.remove(tok)

        self._computeFirstSet()
        self._computeFollowSet()
        self._computePredictTable()

    def _computeFS_seq(self, seq):
        '''计算任意串X1X2..Xn的First集合'''
        FS = set()
        for X in seq:
            FS.update(self.First[X])
            if not 'BLANK' in self.First[X]:
                FS.discard('BLANK')
                break
        return FS

    class LLError(Exception):
        pass

    def _computeFS(self, A):
        '''计算单个元素的FS'''
        for seq in self.PSet[A]:
            flag = True
            for X in seq:
                if not self.First.get(X):
                    self.First[X] = set()
                    self._computeFS(X) #LL文法可以保证不存在循环调用

                '''不应该存在First集为空的非终结符号。若存在，则存在循环调用'''
                if self.First[X] == {}:
                    raise MySyntaxer.LLError("computer FS failed")

                '''将First[X]中除空串以外的元素加入First[A]'''
                self.First[A].update(self.First[X].difference({'BLANK'}))
                if not 'BLANK' in self.First[X]:
                    flag = False
                    break

            '''X1X2..Xn均可推导出空串，则将空串加入到A的First集中'''
            if flag:
                self.First[A].add('BLANK')

    def _computeFirstSet(self):
        '''终结符号的First集里仅含有其本身'''
        for token in self.tokens:
            self.First[token] = {token}

        for A in self.PSet.keys():
            if not self.First.get(A):
                self.First[A] = set()
                self._computeFS(A)

    def _computeFollowSet(self):
        '''初始化Follow集'''
        for A in self.PSet.keys():
            if A==self.begin:
                self.Follow[A] = {'EOF'}
            else:
                self.Follow[A] = set()

        while True:
            flag = True
            '''枚举所有产生式'''
            for A in self.PSet.keys():
                for seq in self.PSet[A]:
                    '''对于每个A->alpha_B_beta'''
                    for i in range(len(seq)):
                        B = seq[i]
                        if not B in self.tokens:
                            Follow_B = self.Follow[B].copy()

                            '''如果是A->alpha_B的形式'''
                            if i == len(seq)-1:
                                self.Follow[B].update(self.Follow[A])
                            else:
                                seqFS = self._computeFS_seq(seq[i+1:])
                                if 'BLANK' in seqFS:
                                    self.Follow[B].update(self.Follow[A])
                                self.Follow[B].update(seqFS.difference({'BLANK'}))

                            if not Follow_B == self.Follow[B]:
                                flag = False

            '''若没有任何Follow集合被更新'''
            if flag: break

    def printFirstSet(self):
        if self.First == {}:
            print("First Set hasn't been computed")
        print("-"*50)
        for key, value in self.First.items():
            if not key in self.tokens:
                print(f"{key}: {value}")

    def printFollowSet(self):
        if self.Follow=={}:
            print("Follow Set hasn't been computed")
        print("-"*50)
        for key, value in self.Follow.items():
            print(f"{key}: {value}")

    def _computePredictTable(self):
        for A in self.PSet.keys():
            self.M[A] = {}
            for i in range(len(self.PSet[A])):
                select = self._computeFS_seq(self.PSet[A][i])
                if 'BLANK' in select:
                    select.update(self.Follow[A])
                for ch in select:
                    if self.M[A].get(ch) != None:
                        if self.debug:
                            print(self.M[A][ch], i, A, ch)
                        raise MySyntaxer.LLError("computer Perdict Table failed")
                    else: self.M[A][ch] = i
        
    def printPredictTable(self):
        if self.M=={}:
            print("Predict Table hasn't been computed")        
        header = sorted(list(self.tokens))
        header.insert(0, r'NTS')
        header.remove('BLANK')
        header.append('EOF')
        printTable = PrettyTable(header)
        printTable.padding_width = 1
        for A in self.PSet.keys():
            row = [A]
            for ch in header[1:]:
                num = self.M[A].get(ch)
                if num is not None:
                    seq = self.PSet[A][num]
                    product = f"{A} -> {' '.join(seq)}"
                else:
                    product = ""
                row.append(product)
            printTable.add_row(row)

        print('-'*50)
        print(printTable)
        # with open('M.txt', 'w') as f:
        #     f.write(printTable.get_string())

    class syntaxNode:
        def __init__(self, symbol):
            self.sym = symbol
            #self.lineno = lineno
            self.children = []
            self.val = None

    class stackRecord:
        '''
        符号栈记录，拥有动作记录、综合记录、符号记录三种记录类型
        '''
        def __init__(self, Rtype):
            if Rtype not in ['ACTION', 'SYN', 'SYMBOL']:
                raise Exception('Node type incorrect')
            self.type = Rtype
            if Rtype == 'ACTION':
                self.inh = {}
                self.act = None
            elif Rtype == 'SYN':
                self.syn = {}
            else:
                self.inh = {}
                self.node = None

        def __str__(self):
            if self.type == 'ACTION':
                return f'(ACTION, {self.act})'
            elif self.type == 'SYN':
                return f'(SYN)'
            else: return f'(SYMBOL, {self.node.sym})'

    def _error(self, tok, stack):
        print(f'Error at Line {tok.lineno-1} pos {tok.lexpos}: Syntax Error')
        if self.debug:
            print(tok)
            for i in range(len(stack)-1):
                print(stack[len(stack)-i-1])

    def _debugPrint(symStack, curRecord):
        import sys
        with open('debug.log', 'a') as f: 
            save_stdout = sys.stdout
            sys.stdout = f
            print('-'*50)
            print(f"curRecord:{curRecord}:")
            if curRecord.type == 'SYN':
                for key, value in curRecord.syn.items():
                    print(f"{key}: {value}, ", end='')
                print()
            else:
                for key, value in curRecord.inh.items():
                    print(f"{key}: {value}, ", end='')
                print()
            print('stack view: ')
            for i in range(len(symStack)):
                print(f'{symStack[i]}, ', end="")
            print()
            print('-'*50)
            sys.stdout = save_stdout

    def _pushdown(self):
        '''
        自顶向下预测分析程序语法，同时进行语义分析及中间代码生成
        '''
        tok = self.lexer.token()
        recentAttr = {}
        globalAttr = {'offset': 0, 'top': SymbolTable()}
        '''构建开始文法的结点并将其压入栈中'''
        self.root = MySyntaxer.syntaxNode(self.begin)
        curRecord = MySyntaxer.stackRecord('SYMBOL')
        curRecord.node = self.root
        endRecord = MySyntaxer.stackRecord('SYMBOL')
        endRecord.node = MySyntaxer.syntaxNode('EOF')
        symStack = [endRecord, MySyntaxer.stackRecord('SYN'), curRecord]
        curRecord = symStack[-1]
        syntaxError = False #若已发生语法错误，则停止语义分析

        while curRecord.type != 'SYMBOL' or curRecord.node.sym != 'EOF':
            if self.debug:
                MySyntaxer._debugPrint(symStack, curRecord)
            if curRecord.type == 'SYMBOL':
                '''若为文法结点'''
                X = curRecord.node
                if X.sym == tok.type:
                    '''匹配栈顶终结符号'''
                    recentAttr = {'value': tok.value, 'type': tok.type} #保存终结符号的综合属性
                    X.val = tok.value
                    tok = self.lexer.token()
                    symStack.pop()
                elif X.sym == 'BLANK':
                    '''匹配栈顶空串'''
                    symStack.pop()
                elif X.sym in self.tokens:
                    # 读入的token未能匹配当前栈顶的终结符：
                    # 弹出栈顶终结符，试图继续语法分析
                    self._error(tok, symStack)
                    print(f'pop {X.sym}, continue analyze.')
                    syntaxError = True
                    symStack.pop()
                else:
                    num = self.M[X.sym].get(tok.type)
                    if num is None:
                        # 找不到可行的产生式以展开当前栈顶的非终结符
                        # 采取错误恢复措施：
                        # 1) 若tok.type在X.sym的Follow集内，则弹出X.sym
                        # 2) 否则根据恐慌模式，忽略输入符号a
                        self._error(tok, symStack)
                        syntaxError = True
                        if tok.type in self.Follow[X.sym]:
                            print(f'pop {X.sym}, continue analyze.')
                            symStack.pop()
                        else:
                            print(f'ignore {tok.type}, continue analyze.')
                            tok = self.lexer.token()
                    else:
                        symStack.pop()
                        seq = self.APSet[X.sym][num]
                        _tmp = list(range(len(seq)))
                        actionRecord = None #用以寻找第一个动作片段
                        for i in range(len(seq)):
                            if not seq[i].startswith('act'):
                                _tmp[i] = MySyntaxer.syntaxNode(seq[i])
                        for i in range(len(seq)):
                            '''建立语法分析树'''
                            if not seq[i].startswith('act'):
                                X.children.append(_tmp[i])
                            '''将产生式倒序入栈'''    
                            _X = seq[len(seq)-i-1]
                            if _X.startswith('act'):
                                newRecord = MySyntaxer.stackRecord('ACTION')
                                newRecord.act = _X
                                actionRecord = newRecord
                                symStack.append(newRecord)
                            else:
                                if not _X in self.tokens:
                                    '''仅为非终结符号创建综合记录'''
                                    newRecord = MySyntaxer.stackRecord('SYN')
                                    symStack.append(newRecord)
                                newRecord = MySyntaxer.stackRecord('SYMBOL')
                                newRecord.node = _tmp[len(seq)-i-1]
                                symStack.append(newRecord)
                        if actionRecord:
                            actionRecord.inh = curRecord.inh.copy()
            elif curRecord.type == 'SYN':
                recentAttr = curRecord.syn.copy()
                symStack.pop()
            else:
                actID = int(curRecord.act[3:])
                top = len(symStack)-1
                if not syntaxError:
                    try:
                        SDTUtil.execAction(actID, recentAttr, globalAttr, symStack, top)
                    except Exception as e:
                        print(f"Error at Line {tok.lineno}:\n\t{e}")
                        raise e
                        break
                symStack.pop()

            curRecord = symStack[-1]
        print()
        print("-"*50)
        #print("symbol table:")
        print(globalAttr['top'])
 
    def _printTree(self, curNode, depth):
        if curNode.children==[]:
            print('  '*depth, f'[{curNode.sym}:{curNode.val}]', sep='')
        else:
            print('  '*depth, curNode.sym, sep='')

        for node in curNode.children:
            self._printTree(node, depth+1)

    def analyze(self, code):
        self.lexer.input(code+'$')
        print("-"*50)
        #print("three-address code: ")
        self._pushdown()
        print("-"*50)
        #print("syntax tree:")
        self._printTree(self.root, 0)
        #print("-"*50)

    def __init__(self, lexer, tokens, debug=False):
        self.lexer = lexer
        self.tokens = tokens
        self.First = {}
        self.Follow = {}
        self.M = {}
        self.PSet = {}
        self.APSet = {}
        self.debug = debug
        if debug:
            f = open('debug.log', 'w')
            f.write(" ")
            f.close()