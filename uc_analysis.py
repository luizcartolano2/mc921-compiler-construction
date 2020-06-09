##################################################
# uc_analysis.py                                 #
#                                                #
# Dataflow Analysis classes.                     #
#                                                #
# Code for Reach Definitions and                 #
# Liveness Analysis for uC.                      #
#                                                #
# Authors: Luiz Cartolano && Erico Faustino      #
##################################################

from uc_block import *
from uc_ast import *

assignment = ('load', 'store', 'literal', 'elem', 'get',
              'add', 'sub', 'mul', 'div', 'mod',
              'lt', 'le', 'ge', 'gt', 'eq', 'ne',
              'and', 'or', 'not',
              'call', 'read')

binary_opcodes = ('add', 'sub', 'mul', 'div', 'mod', 'and', 'or',
                  'not', 'ne', 'eq', 'lt', 'le', 'gt', 'ge')

variable_opcodes = ('load', 'store', 'get')

value_opcodes = ('fptosi', 'sitofp', 'param', 'print', 'return')

binary_fold = {
    'add': lambda l, r: l + r,
    'sub': lambda l, r: l - r,
    'mul': lambda l, r: l * r,
    'div': lambda l, r: l // r,
    'mod': lambda l, r: l % r,
    'and': lambda l, r: l & r,
    'or': lambda l, r: l | r,
    'ne': lambda l, r: int(l != r),
    'eq': lambda l, r: int(l == r),
    'lt': lambda l, r: int(l < r),
    'le': lambda l, r: int(l <= r),
    'gt': lambda l, r: int(l > r),
    'ge': lambda l, r: int(l >= r),
}

class DataFlow(NodeVisitor):
    def __init__(self, viewcfg, debug):
        self.viewcfg = viewcfg
        self.debug = debug
        self.code = []
        self.func = []
        self.rd_block = []
        self.lv_block = []


    def show(self, buf=sys.stdout):
        _str = ""
        for _code in self.code:
            _str += format_instruction(_code) + "\n"
        buf.write(_str)


    def appendOptimizedCode(self, cfg):
        bb = EmitBlocks()
        bb.visit(cfg)
        for _code in bb.code:
            self.code.append(_code)


    def buildRD_blocks(self, cfg):
        self.rd_block = []
        bb = cfg
        while bb:
            self.rd_block.append(bb)
            bb = bb.next_block


    def buildLV_blocks(self, cfg):
        self.lv_block = []
        bb = cfg
        while bb:
            self.lv_block.append(bb)
            bb = bb.next_block


    def _is_assignment(self, inst):
        op = inst[0].split('_')[0]
        return op in assignment


    def compute_RD_gen_kill(self):
        defs = {}
        for _idx, bb in enumerate(self.rd_block):
            for _pos, inst in enumerate(bb.instructions):
                if self._is_assignment(inst):
                    target = inst[-1]
                    if target not in defs.keys():
                        defs[target] = [(_idx, _pos)]
                    else:
                        defs[target].append((_idx, _pos))
        for _idx, bb in enumerate(self.rd_block):
            for _pos, inst in enumerate(bb.instructions):
                if self._is_assignment(inst):
                    target = inst[-1]
                    kills = set(defs[target]) - set([_idx, _pos])
                    bb.rd.kill = bb.rd.kill.union(kills)
                    gen = set([_idx, _pos])
                    bb.rd.gen = gen.union(bb.rd.gen - kills)


    def computeRD_in_out(self):
        changed = set(self.rd_block)
        while changed:
            b = changed.pop()
            b.rd.ins = set()
            for p in b.predecessors:
                b.rd.ins = b.rd.ins.union(p.rd.out)
            old_out = b.rd.out
            b.rd.out = b.rd.gen.union(b.rd.ins - b.rd.kill)
            if b.rd.out != old_out:
                if isinstance(b, BasicBlock):
                    if b.branch:
                        changed = changed.union(set([b.branch]))
                elif isinstance(b, ConditionBlock):
                    changed = changed.union(set([b.taken, b.fall_through]))
        if self.debug:
            print()
            print('==Reaching Definitions==')
            for bb in self.rd_block:
                print(bb.label)
                print('  gen:  ', sorted(bb.rd.gen))
                print('  kill: ', sorted(bb.rd.kill))
                print('  in :  ', sorted(bb.rd.ins))
                print('  out:  ', sorted(bb.rd.out))


    def _op_is_binary(self, inst):
        op = inst[0].split('_')[0]
        return op in binary_opcodes

    #todo missing functions

    def constant_propagation(self):
        for _lbl, b in enumerate(self.rd_block):
            ctes = {}
            for _idx, _pos in b.rd.ins:
                inst = inst.rd_block[_idx].instructions[_pos]
                target = inst[-1]
                op = inst[0].split('_')[0]
                if op == 'literal':
                    if target not in ctes:
                        ctes[target] = inst[1]
                    elif ctes[target] != inst[1]:
                        ctes[target] = 'NAC'
                else:
                    ctes[target] = 'NAC'

    #todo missing functions

    def computeLV_use_def(self):
        for bb in self.rd_block:
            for inst in bb.instructions:
                use, defs = self._getLV_use_def(inst)
                bb.lv.use = bb.lv.use.union(use)
                bb.lv.defs = bb.lv.defs.union(defs)


    def computeLV_in_out(self):
        changed = True
        while changed:
            changed = False
            for bb in list(reversed(self.lv_block)):
                old_in = bb.lv.ins
                old_out = bb.lv.out
                if isinstance(bb, BasicBlock):
                    if bb.branch:
                        bb.lv.out = bb.branch.lv.ins
                elif isinstance(bb, ConditionBlock):
                    bb.lv.out = bb.taken.lv.ins.union(bb.fall_through.lv.ins)
                bb.lv.ins = bb.lv.use.union(bb.lv.out - bb.lv.defs)
                if bb.lv.out != old_out or bb.lv.ins != old_in:
                    changed = True
        if self.debug:
            print()
            print('== Live Variable Analysis ==')
            for bb in self.lv_block:
                print(bb.label)
                print('  use:  ', sorted(bb.lv.use))
                print('  def:  ', sorted(bb.lv.defs))
                print('  in :  ', sorted(bb.lv.ins))
                print('  out:  ', sorted(bb.lv.out))


    def deadcode_elimination(self):
        for bb in self.lv_block:
            dead_code = set()
            live_variables = bb.lv.defs.intersection(bb.lv.out)
            for _pos, inst in reversed(list(enumerate(bb.instructions))):
                use, defs = self._get_full_use_def(inst)
                _is_dead = False
                for d in defs:
                    if d not in live_variables:
                        _is_dead = True
                if _is_dead:
                    dead_code.add(_pos)
                    live_variables = live_variables.union(use)
            updated_instructions = []
            for _pos, inst in enumerate(bb.instructions):
                if not _pos in dead_code:
                    updated_instructions.append(inst)
            bb.instructions = updated_instructions


    def short_circuit_jumps(self, cfg):
        bb = cfg
        while bb.next_block:
            prev = bb
            bb = bb.next_block
            if len(bb.instructions) == 2:
                if bb.instructions[-1][0] == 'jump':
                    target = bb.instructions[-1][1]
                    for p in bb.predecessors:
                        if isinstance(p, BasicBlock):
                            p.instructions[-1] = ('jump', target)
                            p.branch = bb.branch
                        elif isinstance(p, ConditionBlock):
                            op, expr_test, lbl_taken, lbl_fall_through = p.instructions[-1]
                            if lbl_taken == bb.label:
                                lbl_taken = target
                                p.taken = bb.branch
                            elif lbl_fall_through == bb.label:
                                lbl_fall_through = target
                                p.fall_through = bb.branch
                            p.instructions[-1] = (op, expr_test, lbl_taken, lbl_fall_through)
                    prev.next_block = bb.next_block
                    bb = prev


    def visit_Program(self, node):
        self.code = node.text
        for _decl in node.gdecls:
            if isinstance(_decl, FuncDef):
                self.buildRD_blocks(_decl.cfg)
                self.computeRD_gen_kill()
                self.computeRD_in_out()
                self.constant_propagation()
                self.appendOptimizedCode(_decl.cfg)
                self.buildLV_blocks(_decl.cfg)
                self.computeLV_use_def()
                self.computeLV_in_out()
                self.deadcode_elimination()
                self.short_circuit_jumps(_decl.cfg)
                self.appendOptimizedCode(_decl.cfg)
        if self.viewcfg:
            for _decl in node.gdecls:
                if isinstance(_decl, FuncDef):
                    dot = CFG(_decl.decl.name.name + '.opt')
                    dot.view(_decl.cfg)
