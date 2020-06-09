from uc_block import Block, ConditionBlock


class DataFlow():
    def __init__(self, blocks_control):
        self.blocks_control = blocks_control
        self.variable_ops = ['load', 'store', 'get']
        self.binary_ops = ['add', 'sub', 'mul', 'div', 'mod', 'and', 'or',
                           'not', 'ne', 'eq', 'lt', 'le', 'gt', 'ge']
        self.values_ops = ['fptosi', 'sitofp', 'param', 'print', 'return']


    def _set_use_def(self, inst):
        op = inst[0].split('_')[0]

        if op in self.variable_ops:
            return {inst[1]}, {inst[2]}
        elif op in self.binary_ops or op == 'elem':
            return {inst[1], inst[2]}, {inst[3]}
        elif op == 'literal':
            return {}, {inst[2]}
        elif op in self.values_ops and inst[0] != 'return_void':
            return {inst[1]}, {}
        else:
            return {}, {inst[1]}


    def computeLV_use_def(self, func):
        for block_lb in func:
            block = func[block_lb]
            for inst in block.instructions[1:]:
                use, defs = self._set_use_def(inst=inst)
                block.lv.use = block.lv.use.union(use)
                block.lv.defs = block.lv.defs.union(defs)


    def computeLV_in_out(self, func):
        changed = True
        block_labels = list(func.keys())

        while changed:
            changed = False
            for block_lb in list(reversed(block_labels)):
                block = func[block_lb]

                old_in = block.lv.ins
                old_out = block.lv.out

                if isinstance(block, ConditionBlock):
                    block.lv.out = block.taken.lv.ins.union(block.fall_through.lv.ins)
                else:
                    if block.next_block:
                        block.lv.out = block.next_block.lv.ins

                block.lv.ins = block.lv.use.union(block.lv.out - block.lv.defs)

                if block.lv.out != old_out or block.lv.ins != old_in:
                    changed = True

        print('== Live Variable Analysis ==')
        for block_lb in func:
            bb = func[block_lb]
            print(bb.label)
            print('  use:  ', sorted(bb.lv.use))
            print('  def:  ', sorted(bb.lv.defs))
            print('  in :  ', sorted(bb.lv.ins))
            print('  out:  ', sorted(bb.lv.out))


    def optimize_code(self):
        for func in self.blocks_control.functions:

            self.computeLV_use_def(self.blocks_control.functions[func])
            self.computeLV_in_out(self.blocks_control.functions[func])

        # import pdb; pdb.set_trace()
        # print('oi')
