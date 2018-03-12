class SymbolTable:
    # class entry:
    #     def __init__(self, lexeme, Etype, offset):
    #         self.lexeme = lexeme
    #         self.Etype = Etype
    #         self.offset = offset

    class SymbolError(Exception):
        pass

    def getType(self, lexeme):
        if self._entryDict.get(lexeme):
            return self._entryDict[lexeme][0]
        else: 
            raise SymbolTable.SymbolError(f"symbol hasn't been declared: {lexeme}")

    def put(self, lexeme, Etype, offset):
        if self._entryDict.get(lexeme):
            raise SymbolTable.SymbolError(f"duplication of symbol name : {lexeme}")
        self._entryDict[lexeme] = (Etype, offset)

    def getAddr(self, lexeme):
        if self._entryDict.get(lexeme):
            return lexeme
        else: 
            raise SymbolTable.SymbolError(f"symbol hasn't been declared: {lexeme}")

    def temp(self):
        newTemp = f'tmp{self.count}'
        self.count += 1
        return newTemp
    
    def newLabel(self):
        newTemp = f'L{self.Lcount}'
        self.Lcount += 1
        return newTemp

    def newEnv(self, envName):
        parentEnv = self._env
        self._env = envName
        self._entryDict = {}
        self._envDict[envName] = (parentEnv, self._entryDict) # 其实是有bug的但..who care
        
    def popEnv(self):
        self._env = self._envDict[self._env][0]
        self._entryDict = self._envDict[self._env][1]

    def __init__(self):
        self._env = 'main'
        self._entryDict = {}
        self._envDict = {'main': (None, self._entryDict)}
        self.count = 0 #临时变量计数
        self.Lcount = 0 #标签计数

    def __str__(self):
        Rstr = ""
        from prettytable import PrettyTable
        for ename, (_, entryDict) in self._envDict.items():
            Rstr += ename+'\n'
            printTable = PrettyTable(['name', 'type', 'offset'])
            for vname, (_type, offset) in entryDict.items():
                printTable.add_row([vname, _type, offset])
            Rstr += printTable.get_string()
            Rstr += '\n\n'
        return Rstr