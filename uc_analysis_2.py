from uc_block import Block, ConditionBlock, CFG
import numpy as np


class DataFlow():
    def __init__(self, blocks_control):
        self.all_blocks = []
        self.blocks_control = blocks_control
        self.code_to_eliminate = set()
        self.code = []
        self.variable_ops = ['load', 'store', 'get']
        self.binary_ops = ['add', 'sub', 'mul', 'div', 'mod', 'and', 'or',
                           'not', 'ne', 'eq', 'lt', 'le', 'gt', 'ge']
        self.values_ops = ['fptosi', 'sitofp', 'param', 'print', 'return']
        self.assignment_op = ('load', 'store', 'literal', 'elem', 'get',
                              'add', 'sub', 'mul', 'div', 'mod', 'lt',
                              'le', 'ge', 'gt', 'eq', 'ne', 'and', 'or',
                              'not', 'call', 'read')
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


    def __get_use_def(self, inst):
        """

            :param inst:
            :return:
        """
        op = inst[0].split('_')[0]

        if op in self.variable_ops:
            return {inst[1]}, {inst[2]}
        elif op in self.binary_ops or op == 'elem':
            return {inst[1], inst[2]}, {inst[3]}
        elif op == 'literal':
            return set(), {inst[2]}
        elif (op in self.values_ops and inst[0] != 'return_void') or op == 'cbranch':
            return {inst[1]}, set()
        elif op == 'call':
            return set(), {inst[2]}
        elif op in ['read', 'alloc']:
            return set(), {inst[1]}
        else:
            return set(), set()


    def __compute_lv_use_def(self, func):
        for block_lb in func:
            block = func[block_lb]
            for inst in block.instructions:
                use, defs = self.__get_use_def(inst=inst)
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
            for inst_counter, inst in enumerate(block.instructions[1:]):
                if inst[0].split('_')[0] in self.assignment_op:
                    target = inst[-1]
                    if target not in defs.keys():
                        defs[target] = [(block_counter, inst_counter + 1)]
                    else:
                        defs[target].append((block_counter, inst_counter + 1))

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

            for inst_counter, inst in enumerate(block.instructions[1:]):
                if inst[0].split('_')[0] in self.assignment_op:
                    target = inst[-1]
                    kills = set(defs[target]) - {(block_counter, inst_counter + 1)}
                    block.rd.kill = block.rd.kill.union(kills)
                    gen = {(block_counter, inst_counter + 1)}
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

                use, defs = self.__get_use_def(inst)

                if len(defs) == 1:
                    if (defs.intersection(live_variables) == set()) and 'alloc' not in inst[0]:
                        dead_code.add(inst)
                        self.code_to_eliminate.add(inst)

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


    def __set_constants(self, block, blocks_list):
        """

            :param block:
            :param blocks_list:
            :return:
        """
        constants = {}

        # rd.ins has a list of instructions
        # stored as (block_pos, inst_pos)
        for block_pos, inst_pos in sorted(block.rd.out):
            # get instruction
            inst = blocks_list[block_pos].instructions[inst_pos]

            if 'literal' in inst[0]:
                if inst[-1] not in constants:
                    constants[inst[-1]] = inst[1]
                elif constants[inst[-1]] != inst[1]:
                    constants[inst[-1]] = False
            elif 'load' in inst[0]:
                if inst[1] in constants and constants[inst[1]] is not False:
                    constants[inst[-1]] = inst[1]
            elif 'print' in inst[0]:
                pass
            else:
                constants[inst[-1]] = False

        return constants


    def constant_propagation(self, func, func_name, debug=False):
        if debug:
            print()
            print('== Constant Propagation ==')

        blocks_label = list(func.keys())
        blocks_list = [func[block_lb] for block_lb in blocks_label]

        for block_pos, block in enumerate(blocks_list):
            constants = self.__set_constants(block, blocks_list)

            for inst_pos, inst in enumerate(block.instructions):
                op = inst[0].split('_')
                opt_type = op[1] if len(op) > 1 else ''

                if op[0] in ['load', 'store', 'cbranch']:
                    source = inst[1]

                    if source in constants and constants[source] is not False:
                        if op[0] == 'cbranch':
                            # get comparison value
                            comp_value = constants[source]
                            # get actual block
                            temp_block = blocks_list[block_pos]

                            # create new Block
                            new_block = Block('novo')
                            new_block.label = temp_block.label
                            new_block.instructions = temp_block.instructions
                            new_block.predecessors = temp_block.predecessors
                            new_block.rd = temp_block.rd
                            if comp_value == 0:
                                new_block.next_block = temp_block.fall_through
                                new_block.successors = [temp_block.fall_through]

                                temp_block.taken.predecessors = []
                                for successor in temp_block.taken.successors:
                                    successor.predecessors.remove(temp_block.taken)

                                del func[temp_block.taken.label]

                                temp_block.fall_through.predecessors.remove(temp_block)
                                temp_block.fall_through.predecessors.append(new_block)
                            else:
                                new_block.next_block = temp_block.taken
                                new_block.successors = [temp_block.taken]

                                temp_block.fall_through.predecessors = []
                                for successor in temp_block.fall_through.successors:
                                    successor.predecessors.remove(temp_block.fall_through)

                                del func[temp_block.fall_through.label]

                                temp_block.taken.predecessors.remove(temp_block)
                                temp_block.taken.predecessors.append(new_block)

                            blocks_list[block_pos] = new_block
                            func[temp_block.label] = new_block
                            self.blocks_control.functions[func_name][new_block.label] = new_block
                            new_block.instructions[-1] = ('jump', new_block.next_block.label)

                        else:
                            block.instructions[inst_pos] = (f'literal_{opt_type}', constants[source], inst[2])
                            constants[inst[2]] = constants[source]

                elif op[0] in self.binary_ops:
                    # get operands
                    left_op = inst[1]
                    right_op = inst[2]

                    if left_op in constants:
                        if isinstance(constants[left_op], str):
                            if constants[left_op] in constants and constants[constants[left_op]] is not False:
                                left_op = constants[constants[left_op]]
                            elif left_op in constants:
                                constants[left_op] = False
                    if right_op in constants:
                        if isinstance(constants[right_op], str):
                            if constants[right_op] in constants and constants[constants[right_op]] is not False:
                                right_op = constants[constants[right_op]]
                            elif right_op in constants:
                                constants[right_op] = False


                    if left_op in constants and right_op in constants and\
                            constants[left_op] is not False and constants[right_op] is not False:

                        # get constants values
                        left_value, right_value = str(constants[left_op]), str(constants[right_op])
                        left_value, right_value = eval(opt_type + '(' + left_value + ')'),\
                                                  eval(opt_type + '(' + right_value + ')')

                        func_op = self.binary_fold[op[0]]
                        result = func_op(left_value, right_value)
                        result = int(result) if op[0] in self.comparison_ops else result

                        block.instructions[inst_pos] = (f"literal_{opt_type}", result, inst[3])
                        constants[inst[3]] = result

        if debug:
            print('=' * len('== Constant Propagation =='))


    def eliminate_single_jumps(self, func, func_name, debug=False):
        """

            :param func:
            :param func_name:
            :param debug:
            :return:
        """
        if debug:
            print()
            print("== Eliminate Single Jumps ==")

        blocks_label = list(func.keys())
        blocks_list = [func[block_lb] for block_lb in blocks_label]
        remove_from_func = set()

        for block_pos, block in enumerate(blocks_list):
            if len(block.instructions) == 2:
                if block.instructions[-1][0] == 'jump':
                    if debug:
                        print(f"    Block: {block.label}")
                        print(f"    Target: {block.instructions[-1][1]}")
                    jump_target = block.instructions[-1][1]

                    for predecessor in block.predecessors:
                        if debug:
                            print(f"    Predecessor: {predecessor}")
                        if isinstance(predecessor, ConditionBlock):
                            op, expr_test, lbl_taken, lbl_fall = predecessor.instructions[-1]

                            if debug:
                                print(f"        Predecessor {predecessor.label} is a Condition.")

                            if predecessor.taken.label == block.label:
                                if debug:
                                    print(f"            Predecessor {predecessor.label} taken is the path!")
                                # get label taken
                                lbl_taken = jump_target

                                # update the taken for predecessor block
                                old_taken = predecessor.taken
                                predecessor.taken = block.next_block

                                # update next block predecessor
                                block.next_block.predecessors.remove(old_taken)
                                block.next_block.predecessors.insert(0, predecessor)

                                # update predecessors sucessors
                                predecessor.successors.remove(old_taken)
                                predecessor.successors.insert(0, predecessor.taken)

                                if debug:
                                    print(f"            Next block {block.next_block.label} predecessor: {block.next_block.predecessors}")
                                remove_from_func.add(block.label)
                            else:
                                if debug:
                                    print(f"            Predecessor {predecessor.label} fall through is the path!")
                                # get label fall
                                lbl_fall = jump_target

                                # update fall for predecessor
                                old_fall = predecessor.fall_through
                                predecessor.fall_through = block.next_block

                                # update next block predecessor
                                block.next_block.predecessors.remove(old_fall)
                                block.next_block.predecessors.append(predecessor)

                                # update predecessors sucessors
                                predecessor.successors.remove(old_fall)
                                predecessor.successors.append(predecessor.fall_through)

                                remove_from_func.add(block.label)
                            predecessor.instructions[-1] = (op, expr_test, lbl_taken, lbl_fall)

                        elif isinstance(predecessor, Block):
                            if debug:
                                print(f"        Predecessor {predecessor.label} is a Block.")

                            # update predecessor for next block
                            block.next_block.predecessors.remove(block)
                            block.next_block.predecessors.append(predecessor)

                            # update sucessor
                            predecessor.successors.remove(block)
                            predecessor.successors.append(block.next_block)

                            # update next block
                            predecessor.next_block = block.next_block

                            predecessor.instructions[-1] = ('jump', jump_target)

                            remove_from_func.add(block.label)

        if debug:
            print(f"    Remove from func: {remove_from_func}")

        for key in remove_from_func:
            del self.blocks_control.functions[func_name][key]

        if debug:
            print('=' * len("== Eliminate Single Jumps =="))


    def generate_opt_code(self):
        code = []
        for func in self.blocks_control.functions:
            for block_lb in self.blocks_control.functions[func]:
                block = self.blocks_control.functions[func][block_lb]
                for inst in block.instructions:
                    if 'entry' not in inst[0]:
                        code.append(inst)

        self.code = self.blocks_control.globals + code


    def optimize_code(self):
        debug = False

        for func in self.blocks_control.functions:
            self.all_blocks = self.blocks_control.create_block_list(func)
            # make the reaching definitions analysis
            self.compute_rd_in_out(self.blocks_control.functions[func], debug=False)
            self.constant_propagation(self.blocks_control.functions[func], func,debug=False)
            self.all_blocks = self.blocks_control.create_block_list(func)

            # make the liveness analysis
            self.compute_lv_in_out(self.blocks_control.functions[func], debug=False)
            self.eliminate_unreachable_code(self.blocks_control.functions[func], debug=False)
            self.deadcode_elimination(self.blocks_control.functions[func], debug=False)
            self.eliminate_unnecessary_allocs(self.blocks_control.functions[func], debug=False)

            # circuit single jumps
            self.eliminate_single_jumps(self.blocks_control.functions[func], func, debug=False)
            self.all_blocks = self.blocks_control.create_block_list(func)

            self.generate_opt_code()

            if debug:
                # update list of blocks
                self.all_blocks = self.blocks_control.create_block_list(func)

                cfg = CFG(f"{func}-opt")
                cfg.view(self.blocks_control.functions[func]['%entry'], self.all_blocks)
