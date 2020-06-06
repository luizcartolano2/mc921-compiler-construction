##################################################
# uc_block.py                                    #
#                                                #
# Basic Blocks classes.                          #
#                                                #
# Code for the Basic Blocks for uC.              #
#                                                #
# Authors: Luiz Cartolano && Erico Faustino      #
##################################################

def format_instruction(t):
    op = t[0]
    if len(t) > 1:
        if op == 'define':
            return f"\n{op} {t[1]}"
        else:
            _str = "" if op.startswith('global') else "  "
            if op == 'jump':
                _str += f"{op} label {t[1]}"
            elif op == 'cbranch':
                _str += f"{op} {t[1]} label {t[2]} label {t[3]}"
            elif op == 'global_string':
                _str += f"{op} {t[1]} \'{t[2]}\'"
            elif op.startswith('return'):
                _str += f"{op} {t[1]}"
            else:
                for _el in t:
                    _str += f"{_el} "
            return _str
    elif op == 'print_void' or op == 'return_void':
        return f"  {op}"
    else:
        return f"{op}"

class Label(object):
    if __init__(self):
        self.lbl = {}

    def make_label(self, label):
        if label not in self.lbl:
            name = label
            self.lbl[label] = 1
        else:
            name = label + '.' + str(self.lbl[label])
            self.lbl[label] += 1
        return name

    def clear_label(self):
        self.lbl = {}

class ReachDefinitions(object):
    def __init__(self):
        self.gen = set()
        self.kill = set()
        self.ins = set()
        self.out = set()

class LiveVariable(object):
    def __init__(self):
        self.use = set()
        self.defs = set()
        self.ins = set()
        self.out = set()

class Block(object):
    def __init__(self, label):
        self.predecessors = []
        self.next_block = None
        self.label = label
        self.instructions = [(self.label[1:] + ':',)] if self.label else []
        self.rd = ReachDefinitions()
        self.lv = LiveVariable()

    def __iter__(self):
        return iter(self.instructions)

    def append(self, instr):
        self.instructions.append(instr)

    def generate_jump(self):
        return self.instructions[-1][0] != 'jump'

class BasicBlock(Block):
    def __init__(self, label):
        super(BasicBlock, self).__init__(label)
        self.branch = None

class ConditionBlock(Block):
    def __init__(self, label):
        super(ConditionBlock, self).__init__(label)
        super.taken = None
        self.fall_through = None

class BlockVisitor(object):
    def visit(self, block):
        while isinstance(block, Block):
            name = "visit_%s" % type(block).__name__
            if hasattr(self, name):
                getattr(self, name)(block)
            block = block.next_block

class EmitBlocks(BlockVisitor):
    def __init__(self):
        self.code = []

    def visit_BasicBlock(self, block):
        for inst in block.instructions:
            self.code.append(inst)

    def visit_ConditionBlock(self, block):
        for inst in block.instructions:
            self.code.append(inst)

class CFG(object):
    def __init__(self, fname):
        self.fname = fname
        self.g = Digraph('g', filename=fname + '.gv', node_attr={}) #todo essa foi uma linha que cortou :/

    def visit_BasicBlock(self, block):
        _name = block.label
        if _name:
            _label = '{' + _name + ":\l\t" #todo what?
            for _inst in block.instructions[1:]:
                _label += format_instruction(_inst) + "\l\t"
            _label += '}'
            self.g.node(_name, _label=_label)
            if block.branch:
                self.g.node(_name, block.branch.label)
        else:
            self.g.node(self.fname, label=None, _attributes ={}) #todo cortou
            self.g.node(self.fname, block.next_block.label)

    def visit_ConditionBlock(self, block):
        _name = block.label
        _label = '{' + _name + ":\l\t"
        for _inst in block.instructions[1:]:
            _label += format_instruction(_inst) + "\l\t"
        _label += "|{<f0>T|<f1>f}}"
        self.g.node(_name, _label=_label)
        self.g.edge(_name + ':f0', block.taken.label)
        self.g.edge(_name + ':f1', block.fall_through.label)

    def view(self, block):
        while isinstance(block, Block):
            name = "visit_%s" %type(block).__name__
            if hasattr(self, name):
                getattr(self, name)(block)
            block = block.next_block
        self.g.view()
