## 栈记录类型说明
        class stackRecord:
            def __init__(type):
                if type not in ['ACTION', 'SYN', 'SYMBOL']:
                    raise Exception('Node type incorrect')
                self.type = type
                if type == ACTION:
                    self.inh = {}
                    self.act = None
                elif type == SYN:
                    self.syn = {}
                else:
                    self.inh = {}
                    self.node = None

动作记录可能拥有某些栈的上层记录传递而来的，保存在inh字典中的属性。弹出动作记录时会触发其间保存的动作代码。动作代码在执行时，除inh内的属性外，还可使用recentAttr内的属性。

符号记录保存着该文法符号的继承属性和文法符号值。若为非终止符，则在弹出时触发展开操作，将产生式各节点压入栈中，并将继承属性传递给产生式中的第一个动作记录。(L-属性的SDT中，子节点的继承属性只会使用父节点的继承属性，而没有综合属性)

综合记录保存着文法符号的综合属性，弹出时会将其的值赋予全局变量recentAttr。(通过合理放置动作片段，可以避免综合记录的连续弹出)

## 属性值传递
1. 兄弟节点的属性是沿着分析栈的栈顶向栈底传递的，由于展开时栈记录之间的位置关系已知，可以按需直接复制；
2. 父节点继承属性是由栈底向栈顶传递的，由于不知道后续需要使用继承属性的节点的栈位置，故需要全部复制到下一个动作片段之中
3. 结点的综合属性在结点出栈后放置在RecentAttr中，有必要的话通过后边跟随的动作片段进行相关操作