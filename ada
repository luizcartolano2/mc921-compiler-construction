from uc_block import Block, ConditionBlock, CFG
import numpy as np


class DataFlow():
    def __init__(self, blocks_control):
        self.all_blocks = []
        self.blocks_control = blocks_control
        self.code_to_eliminate = set()
        self.variable_ops = ['load', 'store', 'get']
        self.binary_ops = ['add', 'sub', 'mul', 'div', 'mod', 'and', 'or',
                           'not', 'ne', 'eq', 'lt', 'le', 'gt', 'ge']
        self.values_ops = ['fptosi', 'sitofp', 'param', 'print', 'return']
        self.assignment_op = ('load', 'store', 'literal', 'elem', 'get',
                              'add', 'sub', 'mul', 'div', 'mod', 'lt',
                              'le', 'ge', 'gt', 'eq', 'ne', 'and', 'or',
                              'not', 'call', 'read')
        # CHANGE
        self.comparison_ops = {'and', 'or', 'ne', 'eq', 'lt', 'le', 'gt', 'ge'}

        self.binary_fold = {'add': np.add,
                            'sub': np.subtract,
                            'mul': np.multiply,
                            'div': np.floor_divide,
                            'mod': np.mod,
                            'and': np.logical_and,
                            'or': np.logical_or,
                            'ne': np.logical_not,
                            'eq': np.equal,
                            'lt': np.less,
                            'le': np.less_equal,
                            'gt': np.greater,
                            'ge': np.greater_equal,
                            }


    def __set_use_def(self, inst):
        """CHANGE"""
        op = inst[0].split('_')[0]

        if op in self.variable_ops:
            return {inst[1]}, {inst[2]}
        elif op in self.binary_ops or op == 'elem':
            return {inst[1], inst[2]}, {inst[3]}
        elif op == 'literal':
            return {}, {inst[2]}
        elif op in self.values_ops and inst[0] != 'return_void':
            return {inst[1]}, {}
        elif op == 'call':
            return {}, {inst[2]}
        elif op == 'cbranch':
            return {inst[1]}, {}
        elif op == 'read':
            return {}, {inst[1]}
        else:
            return {}, {}


    def __get_full_use_def(self, inst):
        """CHANGE"""
        op = inst[0].split('_')[0]
        if op == 'alloc':
            return {}, {inst[1]}
        else:
            return self.__set_use_def(inst)


    def __compute_lv_use_def(self, func):
        for block_lb in func:
            block = func[block_lb]
            for inst in block.instructions:
                use, defs = self.__set_use_def(inst=inst)
                block.lv.use = block.lv.use.union(use)
                block.lv.defs = block.lv.defs.union(defs)


    def compute_lv_in_out(self, func, debug=False):
        """CHANGE LOGIC WHILE"""
        # first compute use
        # and def to all blocks
        self.__compute_lv_use_def(func)

        changed = True

        # get blocks labels
        cfg = CFG("teste")
        block_labels = cfg.dfs_visit(
            func['%entry'],
            self.all_blocks
        )

        # block_labels = list(func.keys())

        while changed:
            changed = False
            # loop over all the blocks
            # in reverse order
            for block_lb in reversed(block_labels):
                # get the block
                block = func[block_lb]

                # get the actual in and
                # out before upddate
                old_in = block.lv.ins
                old_out = block.lv.out

                # update lv out following the rule:
                # out[n] = \union_{s \in success[n]} in[s]
                temp = set()
                for success in block.successors:
                    temp = temp.union(success.lv.ins)
                block.lv.out = temp

                # update lv in following the rule:
                # in[n] = use[n] \union (out[n] - def[n])
                block.lv.ins = block.lv.use.union(block.lv.out - block.lv.defs)

                # if there is no change
                # we can end the loop
                if block.lv.out != old_out or block.lv.ins != old_in:
                    changed = True

        # set globals as out to all nodes
        for block_lb in block_labels:
            block = func[block_lb]
            for global_inst in self.blocks_control.globals:
                block.lv.out = block.lv.out.union({global_inst[1]})

        if debug:
            print()
            print('== Live Variable Analysis ==')
            for block_lb in block_labels:
                bb = func[block_lb]
                print(bb.label)
                print('\tuse:  ', sorted(bb.lv.use))
                print('\tdef:  ', sorted(bb.lv.defs))
                print('\tin :  ', sorted(bb.lv.ins))
                print('\tout:  ', sorted(bb.lv.out))


    def __compute_rd_defs(self, func, blocks_label):
        """
            Live! Ta OK!
            :param func:
            :return:
        """
        defs = {}

        for block_counter, block_label in enumerate(blocks_label):
            block = func[block_label]
            for inst_counter, inst in enumerate(block.instructions):
                if inst[0].split('_')[0] in self.assignment_op:
                    target = inst[-1]
                    if target not in defs.keys():
                        defs[target] = [(block_counter, inst_counter)]
                    else:
                        defs[target].append((block_counter, inst_counter))

        return defs


    def __compute_rd_gen_kill(self, func):
        """
            Ta OK!
            :param func:
            :return:
        """
        blocks_label = list(func.keys())

        defs = self.__compute_rd_defs(func=func, blocks_label=blocks_label)

        for block_counter, block_label in enumerate(blocks_label):
            block = func[block_label]

            for inst_counter, inst in enumerate(block.instructions):
                if inst[0].split('_')[0] in self.assignment_op:
                    target = inst[-1]
                    kills = set(defs[target]) - {(block_counter, inst_counter)}
                    block.rd.kill = block.rd.kill.union(kills)
                    gen = {(block_counter, inst_counter)}
                    block.rd.gen = gen.union(block.rd.gen - kills)


    def compute_rd_in_out(self, func, debug=False):
        """
            Ta live tbm!
            :param func:
            :return:
        """
        # first compute the gen/kill
        self.__compute_rd_gen_kill(func=func)

        # get a list of blocks
        blocks_label = list(func.keys())

        # create a set of changed nodes
        changed_nodes = set(blocks_label)

        # iterate while exists nodes
        # in the changed_nodes set
        while changed_nodes:
            # get a block label from
            # the set of block labels
            block_label = changed_nodes.pop()
            # get a Block object
            block = func[block_label]

            # first we calculate the in[n]
            # by the following rule :
            # in[n] = \union_{p \in predecessors[n]}{out[p]}
            block.rd.ins = set()
            for predecessor in block.predecessors:
                block.rd.ins = block.rd.ins.union(predecessor.rd.out)

            # store the old out value
            old_out = block.rd.out

            # now we calculate the new out[n] that
            # is calculated according to the rule :
            # out[n] = gen[n] \union (in[n] - kill[n])
            block.rd.out = block.rd.gen.union(block.rd.ins - block.rd.kill)

            # if out[n] has changed, we
            # must update the changed nodes
            # with the successors of n
            if block.rd.out != old_out:
                for success in block.successors:
                    changed_nodes = changed_nodes.union({success.label})

        if debug:
            print()
            print('==Reaching Definitions==')
            for block_lb in func:
                bb = func[block_lb]
                print(bb.label)
                print('\tgen:  ', sorted(bb.rd.gen))
                print('\tkill: ', sorted(bb.rd.kill))
                print('\tin :  ', sorted(bb.rd.ins))
                print('\tout:  ', sorted(bb.rd.out))


    def deadcode_elimination(self, func, debug=False):
        """
            Parece OK!
            :param debug:
            :param func:
            :return:
        """
        for block_lb in func:
            block = func[block_lb]
            dead_code = set()
            live_variables = block.lv.defs.intersection(block.lv.out)

            for inst_pos, inst in reversed(list(enumerate(block.instructions))):

                use, defs = self.__get_full_use_def(inst)

                _is_dead = False

                for d in defs:
                    if d not in live_variables and 'alloc' not in inst[0]:
                        _is_dead = True
                if _is_dead:
                    dead_code.add(inst)
                    self.code_to_eliminate.add(inst)
                else:
                    live_variables = live_variables.union(use) - set(defs)

            updated_instructions = []
            for inst_pos, inst in enumerate(block.instructions):
                if inst not in dead_code:
                    updated_instructions.append(inst)

            block.instructions = updated_instructions


    def eliminate_unreachable_code(self, func, debug=False):
        """
            Parece ok!
            :param func:
            :param debug:
            :return:
        """
        for block_lb in func:
            block = func[block_lb]
            dead_code = set()
            live_variables = block.lv.defs.intersection(block.lv.out)

            for inst_pos, inst in enumerate(block.instructions):
                if inst[0] in ['jump', 'cbranch']:
                    if inst_pos < len(block.instructions):
                        for eliminate_pos in range(inst_pos + 1, len(block.instructions)):
                            dead_code.add(eliminate_pos)
                            self.code_to_eliminate.add(block.instructions[eliminate_pos])

            updated_instructions = []
            for inst_pos, inst in enumerate(block.instructions):
                if inst_pos not in dead_code:
                    updated_instructions.append(inst)

            block.instructions = updated_instructions


    def eliminate_unnecessary_allocs(self, func, debug=False):
        if debug:
            print()
            print('== Alloc Test ==')

        for block_lb in func:
            block = func[block_lb]
            dead_code = set()

            for inst_pos, inst in enumerate(block.instructions):
                if 'alloc' in inst[0]:
                    target = inst[-1]
                    is_dead = True
                    for block_temp in func:
                        bb_temp = func[block_temp]
                        if target in bb_temp.lv.use:
                            is_dead = False
                    if is_dead:
                        if debug:
                            print("=============")
                            print(target)
                            print("=============")
                        dead_code.add(inst_pos)
                        self.code_to_eliminate.add(block.instructions[inst_pos])

            # eliminate code
            updated_instructions = []
            for inst_pos, inst in enumerate(block.instructions):
                if inst_pos not in dead_code:
                    updated_instructions.append(inst)

            block.instructions = updated_instructions

        if debug:
            print('=' * len('== Alloc Test =='))


    def __set_constants(self, block, block_pos, blocks_list):
        constants = {}

        # rd.ins has a list of instructions
        # stored as (block_pos, inst_pos)
        for rd_pos, rd_in in sorted(block.rd.ins):
            # get instruction
            inst = blocks_list[rd_pos].instructions[rd_in]

            if 'literal' in inst[0]:
                if inst[-1] not in constants:
                    constants[inst[-1]] = inst[1]
                elif constants[inst[-1]] != inst[1]:
                    constants[inst[-1]] = False
            else:
                constants[inst[-1]] = False

        return constants


    def __constant_operation(self, operation, left_value, right_value):
        """

            :param operation:
            :param left_value:
            :param right_value:
            :return:
        """
        func_op = self.binary_ops[operation]
        result = func_op(left_value, right_value)

        if operation in self.comparison_ops:
            return int(result)
        else:
            return result


    def __constant_fold(self, inst, left_value, right_value):
        """

            :param inst:
            :param left_value:
            :param right_value:
            :return:
        """
        op_type = inst[0].split('_')[1]

        left_value, right_value = str(left_value), str(right_value)
        left, right = eval(op_type + '(' + left_value + ')'), \
                      eval(op_type + '(' + right_value + ')')

        op_value = self.__constant_operation(inst[0].split('_')[0], left, right)
        inst = (f"literal_{op_type}", op_value, inst[3])

        return inst


    def constant_propagation(self, func, debug=False):
        if debug:
            print()
            print('== Constant Propagation ==')

        blocks_label = list(func.keys())
        blocks_list = [func[block_lb] for block_lb in blocks_label]

        for block_pos, block in enumerate(blocks_list):
            constants = self.__set_constants(block, block_pos, blocks_list)

            for inst_pos, inst in enumerate(block.instructions):
                op = inst[0].split('_')
                opt_type = op[1] if len(op) > 1 else ''
                print(opt_type)

                if op[0] in ['load', 'store', 'cbranch']:
                    source = inst[1]
                    if source in constants and constants[source] is not False:
                        if op[0] == 'cbranch':
                            if debug:
                                print('Chora!')
                            pass
                        else:
                            block.instructions[inst_pos] = (f'literal_{opt_type}', constants[source], inst[2])
                            # update inst/op
                            inst = block.instructions[inst_pos]
                            op = inst[0].split('_')
                elif op[0] in self.binary_ops:
                    # get operands
                    left_op = inst[1]
                    right_op = inst[2]

                    if left_op in constants and right_op in constants and\
                            constants[left_op] is not False and constants[right_op] is not False:

                        # get constants values
                        left_value, right_value = str(constants[left_op]), str(constants[right_op])
                        left_value, right_value = eval(opt_type + '(' + left_value + ')'),\
                                                  eval(opt_type + '(' + right_value + ')')

                        op_value = self.__constant_operation(inst[0].split('_')[0],
                                                             left_value, right_value
                                                             )

                        inst = (f"literal_{opt_type}", op_value, inst[3])
                        block.instructions[inst_pos] = inst
                        op = inst[0].split('_')

        if debug:
            print('=' * len('== Constant Propagation =='))


    def optimize_code(self):
        debug = True

        for func in self.blocks_control.functions:
            self.all_blocks = self.blocks_control.create_block_list(func)
            # make the reaching definitions analysis
            self.compute_rd_in_out(self.blocks_control.functions[func], debug=False)
            self.constant_propagation(self.blocks_control.functions[func], debug=False)

            # make the liveness analysis
            self.compute_lv_in_out(self.blocks_control.functions[func], debug=False)
            self.eliminate_unreachable_code(self.blocks_control.functions[func], debug=False)
            self.deadcode_elimination(self.blocks_control.functions[func], debug=False)
            self.eliminate_unnecessary_allocs(self.blocks_control.functions[func], debug=False)

            if debug:
                cfg = CFG(f"{func}-opt")
                cfg.view(self.blocks_control.functions[func]['%entry'], self.all_blocks)
