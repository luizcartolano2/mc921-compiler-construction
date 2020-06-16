##################################################
# uc_block.py                                    #
#                                                #
# Basic Blocks classes.                          #
#                                                #
# Code for the Basic Blocks for uC.              #
#                                                #
# Authors: Marcio M Pereira - IC - MC921         #
##################################################
from graphviz import Digraph


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
    def __init__(self):
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
        self.successors = []
        self.next_block = None
        self.label = label
        self.instructions = [(self.label[1:],)] if self.label else []
        self.rd = ReachDefinitions()
        self.lv = LiveVariable()
        self.visited = False


    def __iter__(self):
        return iter(self.instructions)


    def append(self, instr):
        self.instructions.append(instr)


    def generate_jump(self):
        return self.instructions[-1][0] != 'jump'


    def take_cbranch(self):
        return self.instructions[-1][-0] == 'cbranch'


class ConditionBlock(Block):
    def __init__(self, label):
        super(ConditionBlock, self).__init__(label)
        # true cond
        self.taken = None
        # false cond
        self.fall_through = None


class BlockVisitor():
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
        self.g = Digraph('g', filename=fname + '.gv', node_attr={'shape': 'record'})
        self.labels = []

    def visit_Block(self, block):
        if block.visited is False:
            # Get the label as node name
            _name = block.label

            # print(f"Block name : {_name}")
            if _name:
                # get the formatted instructions as node label
                _label = "{" + _name + ":\l\t"
                for _inst in block.instructions[1:]:
                    _label += format_instruction(_inst) + "\l\t"
                _label += "}"
                self.g.node(_name, label=_label)
                if block.next_block:
                    self.g.edge(_name, block.next_block.label)

            block.visited = True


    def visit_ConditionBlock(self, block):
        if block.visited is False:
            # Get the label as node name
            _name = block.label
            # print(f"Conditional Block name : {_name}")
            # get the formatted instructions as node label
            _label = "{" + _name + ":\l\t"
            for _inst in block.instructions[1:]:
                _label += format_instruction(_inst) + "\l\t"
            _label +="|{<f0>T|<f1>F}}"
            self.g.node(_name, label=_label)
            self.g.edge(_name + ":f0", block.taken.label)
            self.g.edge(_name + ":f1", block.fall_through.label)

            if isinstance(block.taken, ConditionBlock):
                getattr(self, "visit_ConditionBlock")(block.taken)
            else:
                getattr(self, "visit_Block")(block.taken)

            if isinstance(block.fall_through, ConditionBlock):
                getattr(self, "visit_ConditionBlock")(block.fall_through)
            else:
                getattr(self, "visit_Block")(block.fall_through)

            block.visited = True


    def dfs_util(self, block):
        if block.visited:
            return

        block.visited = True
        self.labels.append(block.label)
        for bb in block.successors:
            if bb.visited is False:
                self.dfs_util(bb)


    def dfs_visit(self, block, all_blocks=[]):
        self.labels = []

        for block in all_blocks:
            block.visited = False

        for block in all_blocks:
            self.dfs_util(block)

        return self.labels


    def view(self, block, all_blocks=[]):

        for bb in all_blocks:
            bb.visited = False

        self.g.node(self.fname, label=None, _attributes={'shape': 'ellipse'})
        self.g.edge(self.fname, block.label)

        while isinstance(block, Block):
            if isinstance(block, ConditionBlock):
                name = "visit_ConditionBlock"
            else:
                name = "visit_%s" % type(block).__name__

            if hasattr(self, name):
                getattr(self, name)(block)

            block = block.next_block

        for block in all_blocks:
            if block.visited is False:
                if isinstance(block, ConditionBlock):
                    getattr(self, "visit_ConditionBlock")(block)
                else:
                    getattr(self, "visit_Block")(block)

        # You can use the next stmt to see the dot file
        self.g.view()


