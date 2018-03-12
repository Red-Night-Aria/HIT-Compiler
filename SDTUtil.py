class SDTUtil:
    def calculateElemType(Etype):
        if not Etype.startswith('array'):
            raise Exception
        else:
            Etype = Etype[6:-1]
            index = Etype.find(',')
            num = int(Etype[:index])
            Etype = Etype[index+2: ]
            return num, Etype

    def calculateWidth(Etype):
        if not Etype.startswith('array'):
            if Etype == 'integer': return 4
            elif Etype == 'float': return 8
            elif Etype == 'boolean': return 1
            else:
                print("????", Etype)
                raise Exception
        else:
            num, Etype = SDTUtil.calculateElemType(Etype)
            return num*SDTUtil.calculateWidth(Etype)

    def _act0(recentAttr, globalAttr, stack, top):
        stack[top-1].inh['t'] = recentAttr['type']
        stack[top-1].inh['w'] = recentAttr['width']

    def _act1(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = recentAttr['type']
        stack[top-1].syn['width'] = recentAttr['width']
    
    def _act2(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = 'integer'
        stack[top-1].syn['width'] = 4

    def _act3(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = 'float'
        stack[top-1].syn['width'] = 8

    def _act4(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = 'boolean'
        stack[top-1].syn['width'] = 1

    def _act5(recentAttr, globalAttr, stack, top):
        stack[top-4].inh['num'] = recentAttr['value']
        stack[top-2].inh['t'] = stack[top].inh['t']
        stack[top-2].inh['w'] = stack[top].inh['w']

    def _act6(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = f"array({stack[top].inh['num']}, {recentAttr['type']})"
        stack[top-1].syn['width'] = stack[top].inh['num']*recentAttr['width']

    def _act7(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = stack[top].inh['t']
        stack[top-1].syn['width'] = stack[top].inh['w'] 

    def _act8(recentAttr, globalAttr, stack, top):
        globalAttr['offset'] = 0

    def _act9(recentAttr, globalAttr, stack, top):
        stack[top-2].inh['Ttype'] = recentAttr['type']
        stack[top-2].inh['Twidth'] = recentAttr['width']

    def _act10(recentAttr, globalAttr, stack, top):
        globalAttr['top'].put(recentAttr['value'], stack[top].inh['Ttype'], globalAttr['offset'])
        globalAttr['offset'] += stack[top].inh['Twidth']

    def _act11(recentAttr, globalAttr, stack, top):
        stack[top-4].inh['Laddr'] = recentAttr['addr']
        stack[top-4].inh['Ltype'] = recentAttr['type']

    def typeCheck(Ltype, Rtype):
        curLtype = SDTUtil.typeMap(Ltype)
        curRtype = SDTUtil.typeMap(Rtype)
        if (curLtype != curRtype):
            raise Exception(f"Type unconsistent: expect {curLtype} get {curRtype}")
        
    def _act12(recentAttr, globalAttr, stack, top):
        SDTUtil.typeCheck(stack[top].inh['Ltype'], recentAttr['type'])
        print(f"{stack[top].inh['Laddr']} = {recentAttr['addr']}")

    def _act13(recentAttr, globalAttr, stack, top):
        stack[top-1].inh['Taddr'] = recentAttr['addr']
        stack[top-1].inh['Ttype'] = recentAttr['type']
    
    def _act14(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['addr'] = recentAttr['addr']
        stack[top-1].syn['type'] = recentAttr['type']

    def typeMap(_type):
        if _type=='INT':
            return 'integer'
        if _type=='LITEAL':
            return 'string'
        if _type=='REAL':
            return 'float'
        else:
            return _type

    def _act15(recentAttr, globalAttr, stack, top):
        SDTUtil.typeCheck(stack[top].inh['Ttype'], recentAttr['type'])
        temp = globalAttr['top'].temp()
        print(f"{temp} = {stack[top].inh['Taddr']} + {recentAttr['addr']}")
        stack[top-1].inh['Taddr'] = temp
        stack[top-1].inh['Ttype'] = stack[top].inh['Ttype'] 

    def _act48(recentAttr, globalAttr, stack, top):
        SDTUtil.typeCheck(stack[top].inh['Ttype'], recentAttr['type'])
        temp = globalAttr['top'].temp()
        print(f"{temp} = {stack[top].inh['Taddr']} - {recentAttr['addr']}")
        stack[top-1].inh['Taddr'] = temp
        stack[top-1].inh['Ttype'] = stack[top].inh['Ttype'] 

    def _act49(recentAttr, globalAttr, stack, top):
        SDTUtil.typeCheck(stack[top].inh['Ttype'], recentAttr['type'])
        temp = globalAttr['top'].temp()
        print(f"{temp} = {stack[top].inh['Taddr']} * {recentAttr['addr']}")
        stack[top-1].inh['Taddr'] = temp
        stack[top-1].inh['Ttype'] = stack[top].inh['Ttype']

    def _act50(recentAttr, globalAttr, stack, top):
        SDTUtil.typeCheck(stack[top].inh['Ttype'], recentAttr['type'])
        temp = globalAttr['top'].temp()
        print(f"{temp} = {stack[top].inh['Taddr']} / {recentAttr['addr']}")
        stack[top-1].inh['Taddr'] = temp
        stack[top-1].inh['Ttype'] = stack[top].inh['Ttype']

    def _act16(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['addr'] = stack[top].inh['Taddr']
        stack[top-1].syn['type'] = stack[top].inh['Ttype']

    def _act17(recentAttr, globalAttr, stack, top):
        stack[top-2].syn['addr'] = recentAttr['addr']
        stack[top-2].syn['type'] = recentAttr['type']
    
    def _act18(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['addr'] = recentAttr['value']
        stack[top-1].syn['type'] = recentAttr['type']
        
    def _act19(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['addr'] = recentAttr['addr']
        stack[top-1].syn['type'] = recentAttr['type']

    def _act20(recentAttr, globalAttr, stack, top):
        stack[top-3].inh['base'] = globalAttr['top'].getAddr(recentAttr['value'])
        stack[top-4].syn['type'] = globalAttr['top'].getType(recentAttr['value'])
        stack[top-1].inh['type'] = globalAttr['top'].getType(recentAttr['value'])
        stack[top-1].inh['base'] = globalAttr['top'].getAddr(recentAttr['value'])

    def _act21(recentAttr, globalAttr, stack, top):
        if recentAttr.get('type'):
            stack[top-1].syn['type'] = recentAttr['type']
        if not recentAttr.get('addr'):
            stack[top-1].syn['addr'] = stack[top].inh['base']
        else:
            t = globalAttr['top'].temp()
            print(f"{t} = {stack[top].inh['base']}[{recentAttr['addr']}]")
            stack[top-1].syn['addr'] = t

    def _act22(recentAttr, globalAttr, stack, top):
        try:
            num, elemType = SDTUtil.calculateElemType(stack[top].inh['type'])
        except Exception:
            raise Exception('Too many subscript') #TODO 数组切片过多
        if SDTUtil.typeMap(recentAttr['type']) != 'integer':
            raise Exception('Array subscript must be integer')
        Ewidth = SDTUtil.calculateWidth(elemType)
        t = globalAttr['top'].temp()
        print(f"{t} = {recentAttr['addr']} * {Ewidth}")
        stack[top-2].inh['type'] = elemType
        stack[top-3].syn['type'] = elemType
        stack[top-4].inh['base'] = t

    def _act23(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = recentAttr['type']
        if recentAttr.get('addr'):
            t0 = globalAttr['top'].temp()
            print(f"{t0} = {stack[top].inh['base']} + {recentAttr['addr']}")
            stack[top-1].syn['addr'] = t0
        else:
            stack[top-1].syn['addr'] = stack[top].inh['base']

    def _act24(recentAttr, globalAttr, stack, top):
        '''
            假设Bool_E的真假出口此时已得到确定
        '''
        stack[top-1].inh['code'] = recentAttr['code']
        stack[top-1].inh['true'] = stack[top].inh['true']
        stack[top-1].inh['false'] = stack[top].inh['false']
     
    def _act25(recentAttr, globalAttr, stack, top):
        '''
            Bool_T的真假出口直到此刻才能确定；利用format回填格式化代码字符串中的true和false
        '''
        B1True = stack[top].inh['true'] if stack[top].inh['true'] != 'fall' else globalAttr['top'].newLabel()
        exec(stack[top].inh['code'].format(true=B1True, false='fall'))
        stack[top-1].inh['true'] = stack[top].inh['true']
        stack[top-1].inh['false'] = stack[top].inh['false']
        if stack[top].inh['true'] == 'fall':
            stack[top-3].inh['true'] = B1True
        
    def _act26(recentAttr, globalAttr, stack, top):
        if stack[top].inh.get('true'):
            print(f"{stack[top].inh['true']}: ", end='')

    def _act27(recentAttr, globalAttr, stack, top):
        B1False = stack[top].inh['false'] if stack[top].inh['false'] != 'fall' else globalAttr['top'].newLabel()
        exec(stack[top].inh['code'].format(true='fall', false=B1False))
        stack[top-1].inh['true'] = stack[top].inh['true']
        stack[top-1].inh['false'] = stack[top].inh['false']
        if stack[top].inh['false'] == 'fall':
            stack[top-3].inh['false'] = B1False
    
    def _act28(recentAttr, globalAttr, stack, top):
        if stack[top].inh.get('false'):
            print(f"{stack[top].inh['false']}: ", end='')

    def _act29(recentAttr, globalAttr, stack, top):
        '''
            act29~act36 : Bool_T有已确定真假出口和未确定真假出口两种形态
        '''
        if stack[top].inh.get('true'):
            stack[top-1].inh['true'] = stack[top].inh['false']
            stack[top-1].inh['false'] = stack[top].inh['true']

    def _act30(recentAttr, globalAttr, stack, top):
        if recentAttr.get('code'):
            tmpStr = recentAttr['code'].replace("{true}", "{tmp}")
            tmpStr = tmpStr.replace("{false}", "{true}")
            stack[top-1].syn['code'] = tmpStr.replace("{tmp}", "{false}") 

    def _act31(recentAttr, globalAttr, stack, top):
        exec(stack[top].inh['code'].format(true=stack[top].inh['true'], false=stack[top].inh['false']))

    def _act32(recentAttr, globalAttr, stack, top):
        stack[top-5].inh['E1Addr'] = recentAttr['addr']
        if stack[top].inh.get('true'):
            stack[top-5].inh['true'] = stack[top].inh['true']
            stack[top-5].inh['false'] = stack[top].inh['false']
        
    def _act33(recentAttr, globalAttr, stack, top):
        stack[top-3].inh['rel'] = recentAttr['value']

    def _act34(recentAttr, globalAttr, stack, top):
        # code = "if {0} {1} {2} goto ".format(stack[top].inh['E1Addr'], stack[top].inh['rel'], recentAttr['addr'])
        # code += "{true}"
        # code += "\n goto {false}"
        # if stack[top].inh.get('true'):
        #     print(code.format(true=stack[top].inh['true'], false=stack[top].inh['false']))
        # else:
        #     stack[top-1].syn['code'] = code
        test = "{0} {1} {2}".format(stack[top].inh['E1Addr'], stack[top].inh['rel'], recentAttr['addr'])
        code = '''
if '{true}' != 'fall' and '{false}' != 'fall':
    print("if {test} goto {true}")
    print("goto {false}")
elif '{true}' != 'fall':
    print("if {test} goto {true}")
elif '{false}' != 'fall':
    print("ifFalse {test} goto {false}")
'''.format(test=test, true="{true}", false="{false}")
        if stack[top].inh.get('true'):
            exec(code.format(true=stack[top].inh['true'], false=stack[top].inh['false']))
        else:
            stack[top-1].syn['code'] = code

    def _act35(recentAttr, globalAttr, stack, top):
        code = '''
if '{true}' != 'fall':
    print("goto {true}")
'''
        if stack[top].inh.get('true'):
            exec(code.format(true=stack[top].inh['true']))
        else:
            stack[top-1].syn['code'] = code

    def _act36(recentAttr, globalAttr, stack, top):
        code = '''
if '{false}' != 'fall':
    print("goto {false}")
'''
        if stack[top].inh.get('true'):
            exec(code.format(false=stack[top].inh['false']))
        else:
            stack[top-1].syn['code'] = code

    def _act37(recentAttr, globalAttr, stack, top):
        stack[top-1].inh['true'] = 'fall'
        stack[top-1].inh['false'] = stack[top].inh['next']
        stack[top-4].inh['next'] = stack[top].inh['next']
        stack[top-6].inh['next'] = stack[top].inh['next']

    def _act38(recentAttr, globalAttr, stack, top):
        newLabel = globalAttr['top'].newLabel()
        stack[top-1].inh['next'] = newLabel
    
    def _act39(recentAttr, globalAttr, stack, top):
        print(f"{stack[top].inh['next']}: ", end="")
        pass

    def _act40(recentAttr, globalAttr, stack, top):
        begin = globalAttr['top'].newLabel()
        stack[top-1].inh['true'] = 'fall'
        stack[top-1].inh['false'] = stack[top].inh['next']
        stack[top-4].inh['next'] = begin
        stack[top-6].inh['begin'] = begin
        stack[top-6].inh['next'] = stack[top].inh['next']
        print(f"{begin}: ", end="")

    def _act41(recentAttr, globalAttr, stack, top):
        print(f"goto {stack[top].inh['begin']}")
        print(f"{stack[top].inh['next']}: ", end="")

    def _act47(recentAttr, globalAttr, stack, top):    
        stack[top-2].inh['type'] = recentAttr['type']

    def _act42(recentAttr, globalAttr, stack, top):
        globalAttr['top'].put(recentAttr['value'], stack[top].inh['type'], "")
        globalAttr['top'].newEnv(recentAttr['value'])

    def _act43(recentAttr, globalAttr, stack, top):
        tmp = globalAttr['top'].temp()
        print(f"{tmp} = call {stack[top].inh['base']}, {recentAttr['num']}")
        stack[top-2].syn['attr'] = tmp

    def _act44(recentAttr, globalAttr, stack, top):
        print(f"param {recentAttr['addr']}")

    def _act45(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['num'] = recentAttr['num'] + 1

    def _act46(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['num'] = 0

    def _act51(recentAttr, globalAttr, stack, top):
        stack[top-1].syn['type'] = 'record'
        stack[top-1].syn['width'] = 0

    def _act52(recentAttr, globalAttr, stack, top):
        print(f"return {recentAttr['addr']}")

    def _act53(recentAttr, globalAttr, stack, top):
        globalAttr['top'].popEnv()

    def execAction(actId, recentAttr, globalAttr, stack, top):
        methodName = f'_act{actId}'
        method = getattr(SDTUtil, methodName)
        method(recentAttr, globalAttr, stack, top)