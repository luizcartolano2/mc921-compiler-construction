##################################################
# uc_analysis.py                                 #
#                                                #
# Code for the DataFlow analysis                 #
#                                                #
# Authors: Luiz Cartolano && Erico Faustino      #
##################################################
from uc_block import Block, ConditionBlock, CFG


class DataFlow():
    """
        Class to implement DataFlow analysis.
    """
    def __init__(self, blocks_control):
        self.all_blocks = []
        self.before_opt_blocks = None
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

        self.binary_fold = {'add': lambda l, r: l + r,
                            'sub': lambda l, r: l - r,
                            'mul': lambda l, r: l * r,
                            'div': lambda l, r: l // r,
                            'mod': lambda l, r: l % r,
                            'and': lambda l, r: l & r,
                            'or': lambda l, r: l | r,
                            'ne': lambda l, r: l != r,
                            'eq': lambda l, r: l == r,
                            'lt': lambda l, r: l < r,
                            'le': lambda l, r: l <= r,
                            'gt': lambda l, r: l > r,
                            'ge': lambda l, r: l >= r,
                            }


    def __get_use_def(self, inst):
        """
            Function to return instructions
            uses and definitions.

            :param inst: tuple
            :return: set, set
        """
        # get operation
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
        """
            Compute LV use and def for
            all blocks.

            :param func: dict
            :return: None
        """
        # for each block in function
        for block_lb in func:
            # get block obj
            block = func[block_lb]
            # for each instruction in block
            for inst in block.instructions:
                # get use and defs
                use, defs = self.__get_use_def(inst=inst)
                # make the union of all uses
                block.lv.use = block.lv.use.union(use)
                # make the union of all defs
                block.lv.defs = block.lv.defs.union(defs)


    def compute_lv_in_out(self, func, debug=False):
        """
            Compute the LV in and out for all
            blocks following the algorithm given by
            https://www.cs.colostate.edu/~mstrout/CS553/slides/lecture03.pdf

            :param func: dict
            :param debug: bool
            :return: None
        """
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

        while changed:
            # set changed to false
            changed = False

            # loop over all the blocks
            # in reverse order
            for block_lb in reversed(block_labels):

                # get the block
                block = func[block_lb]

                # get the actual in and
                # out before update
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
        # according to professor spec since we
        # are not optimizing globals
        for block_lb in block_labels:
            block = func[block_lb]
            for global_inst in self.blocks_control.globals:
                block.lv.out = block.lv.out.union({global_inst[1]})

        # print LV in/out for all
        # blocks if in debug mode
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
            Func to compute RD definitions
            for all blocks.

            :param func: dict
            :param blocks_label: list
            :return: dict
        """
        # create an empty
        # dict of definitions
        defs = {}

        # iterate over all blocks of a function
        for block_counter, block_label in enumerate(blocks_label):
            # get the block obj
            block = func[block_label]
            # iterate over all instructions
            for inst_counter, inst in enumerate(block.instructions[1:]):
                # an assignment instruction is any
                # operation that defines a new var
                # such as a load/store/add/etc ...
                if inst[0].split('_')[0] in self.assignment_op:
                    # tuple last element
                    # is the target
                    target = inst[-1]
                    # if target do not exist
                    # in keys add it to the dict
                    # else append it to the previous
                    # we add a tuple with (block_pos, inst_pos)
                    if target not in defs.keys():
                        defs[target] = [(block_counter, inst_counter + 1)]
                    else:
                        defs[target].append((block_counter, inst_counter + 1))

        return defs


    def __compute_rd_gen_kill(self, func):
        """
            Compute the gen kill of all blocks.

            :param func: dict
            :return: None
        """
        # get the blocks labels as a list
        blocks_label = list(func.keys())

        # get all definitions for all blocks
        defs = self.__compute_rd_defs(func=func,
                                      blocks_label=blocks_label
                                      )

        # iterate over all blocks
        for block_counter, block_label in enumerate(blocks_label):
            # get block obj
            block = func[block_label]
            # iterate over all block instructions
            for inst_counter, inst in enumerate(block.instructions[1:]):
                # an assignment instruction is any
                # operation that defines a new var
                # such as a load/store/add/etc ...
                if inst[0].split('_')[0] in self.assignment_op:
                    # tuple last element
                    # is the target
                    target = inst[-1]
                    # following Appel algorithm
                    # kill = defs[target] - inst
                    kills = set(defs[target]) - {(block_counter, inst_counter + 1)}
                    # block kill is the union of all kills
                    block.rd.kill = block.rd.kill.union(kills)
                    # gen is the instruction by itself
                    gen = {(block_counter, inst_counter + 1)}
                    # block gen is the union of previous
                    # gens minus the actual kills
                    block.rd.gen = gen.union(block.rd.gen - kills)


    def compute_rd_in_out(self, func, debug=False):
        """
            Compute the RD in and out for all
            blocks following the algorithm given by
            https://www.cs.colostate.edu/~mstrout/CS553Fall07/Slides/lecture11-dataflow.pdf

            :param func: dict
            :param debug: bool
            :return: None
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

        # print LV in/out for all
        # blocks if in debug mode
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


    def dead_code_elimination(self, func, debug=False):
        """
            Function that implements a dead code
            elimination for the function being analysed
            following the algorithm described at
            https://www.cs.colostate.edu/~cs553/ClassNotes/lecture05-dataflow-CSE.ppt.pdf

            :param func: dict
            :param debug: bool
            :return: None
        """
        # iterate over all blocks
        for block_lb in func:
            # get block obj
            block = func[block_lb]
            # for each block create an
            # empty set of dead code
            dead_code = set()
            # get all live variables at a block
            # given by the \intersect{defs, block.lv.out}
            live_variables = block.lv.defs.intersection(block.lv.out)

            # iterate over each instruction in block at reverse order
            for inst_pos, inst in reversed(list(enumerate(block.instructions))):
                # get inst use and definitions
                use, defs = self.__get_use_def(inst)
                # if the defs set
                # contains only one temporary
                if len(defs) == 1:
                    # if the temporary being defined
                    # is not in the live out set
                    if defs.intersection(live_variables) == set():
                        # check if not deals with globals
                        # because it causes bugs
                        if 'elem' in inst[0] or 'alloc' in inst[0] or '*' in inst[0]:
                            pass
                        else:
                            # remove the node from the CFG
                            dead_code.add(inst)
                            self.code_to_eliminate.add(inst)
                # update the live variables
                # adding the uses and eliminating
                # the definitions
                live_variables = live_variables.union(use) - set(defs)

            # update block instructions
            # by eliminate the dead codes
            updated_instructions = []
            for inst_pos, inst in enumerate(block.instructions):
                if inst[0].startswith('define'):
                    updated_instructions.append(inst)
                elif inst not in dead_code:
                    updated_instructions.append(inst)
            block.instructions = updated_instructions


    def eliminate_unreachable_code(self, func, debug=False):
        """
            Function to eliminate instructions
            that are presented after jumps.

            :param func: dict
            :param debug: bool
            :return: None
        """
        # iterate over all blocks
        for block_lb in func:
            # get block obj
            block = func[block_lb]
            # for each block create an
            # empty set of dead code
            dead_code = set()

            # iterate over each instruction in block
            for inst_pos, inst in enumerate(block.instructions):
                # check if instruction is a jump
                if inst[0] in ['jump', 'cbranch']:
                    # check if not last instruction
                    if inst_pos < len(block.instructions):
                        # if not, iterate over the next instructions
                        # appending them to the dead code list
                        for eliminate_pos in range(inst_pos + 1, len(block.instructions)):
                            dead_code.add(eliminate_pos)
                            self.code_to_eliminate.add(block.instructions[eliminate_pos])

            # update block instructions
            # by eliminate the dead codes
            updated_instructions = []
            for inst_pos, inst in enumerate(block.instructions):
                if inst_pos not in dead_code:
                    updated_instructions.append(inst)
            block.instructions = updated_instructions


    def eliminate_unnecessary_alloc(self, func, debug=False):
        """
            Function to eliminate allocations of
            unused variables.

            :param func: dict
            :param debug: bool
            :return: None
        """
        # print if in debug mode
        if debug:
            print()
            print('== Alloc Test ==')

        # iterate over all blocks
        for block_lb in func:
            # get block obj
            block = func[block_lb]
            # for each block create an
            # empty set of dead code
            dead_code = set()

            # iterate over each instruction in block
            for inst_pos, inst in enumerate(block.instructions):
                # check if alloc operation
                if 'alloc' in inst[0]:
                    # get operation target
                    target = inst[-1]
                    # set a dead flag as True
                    is_dead = True
                    # iterate over all blocks
                    # checking if the target is
                    # any block.lv.use
                    for block_temp in func:
                        # get block
                        bb_temp = func[block_temp]
                        # if target in a block.lv.use
                        # we cant eliminate it so
                        # flag is False
                        if target in bb_temp.lv.use:
                            is_dead = False
                    if is_dead:
                        # print if in debug mode
                        if debug:
                            print("=============")
                            print(target)
                            print("=============")
                        # appending them to the dead code list
                        dead_code.add(inst_pos)
                        self.code_to_eliminate.add(block.instructions[inst_pos])

            # update block instructions
            # by eliminate the dead codes
            updated_instructions = []
            for inst_pos, inst in enumerate(block.instructions):
                if inst_pos not in dead_code:
                    updated_instructions.append(inst)
            block.instructions = updated_instructions

        # print if in debug mode
        if debug:
            print('=' * len('== Alloc Test =='))


    def __set_constants(self, block, blocks_list):
        """
            Create a dict of constants to the block.

            :param block: uc_block.Block
            :param blocks_list: list
            :return: dict
        """
        # create an empty
        # dict of constants
        constants = {}

        # rd.out has a list of instructions
        # stored as (block_pos, inst_pos)
        # iterate over it
        for block_pos, inst_pos in sorted(block.rd.out):
            # get instruction
            inst = blocks_list[block_pos].instructions[inst_pos]

            # if dealing with a literal instruction
            # if target not yet on dict, add it with the
            # value, else, check if not sets a new value to
            # target, if yes, cannot be a constant
            if 'literal' in inst[0]:
                if inst[-1] not in constants:
                    constants[inst[-1]] = inst[1]
                elif constants[inst[-1]] != inst[1]:
                    constants[inst[-1]] = False
            # if deals with a load, check if
            # the source is a constant, if yes
            # make the target a constant too
            elif 'load' in inst[0]:
                if inst[1] in constants and constants[inst[1]] is not False:
                    constants[inst[-1]] = inst[1]
            # if print ignore
            elif 'print' in inst[0]:
                pass
            # if any other instruction
            # target cannot be a constant
            else:
                constants[inst[-1]] = False

        return constants


    def constant_propagation(self, func, func_name, debug=False):
        """
            Function that implements a constant
            optimization for the function being analysed
            following the algorithm described at
            https://www.cs.colostate.edu/~mstrout/CS553/slides/lecture01.pdf

            :param func: dict
            :param func_name: str
            :param debug: bool
            :return: None
        """
        # print if in debug mode
        if debug:
            print()
            print('== Constant Propagation ==')

        # get a list of blocks labels
        blocks_label = list(func.keys())
        # get a list of block objects
        blocks_list = [func[block_lb] for block_lb in blocks_label]

        # iterate over all blocks
        for block_pos, block in enumerate(blocks_list):
            # set blocks constants
            constants = self.__set_constants(block, blocks_list)
            # iterate over all instructions at a block
            for inst_pos, inst in enumerate(block.instructions):
                # get the instruction operation
                op = inst[0].split('_')
                # get the operation type
                opt_type = op[1] if len(op) > 1 else ''

                # deals if operation is a load/store or cbranch
                if op[0] in ['load', 'store', 'cbranch']:
                    # get the source
                    # for instruction
                    source = inst[1]

                    # check if source is a constant
                    if source in constants and constants[source] is not False:
                        # optimize a cbranch when
                        # the source, comparison value,
                        # is a constant, so we can eliminate
                        # one of the branches
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

                            # check which branch is taken
                            # the True or False block
                            if comp_value == 0:
                                # update new block successors
                                new_block.next_block = temp_block.fall_through
                                new_block.successors = [temp_block.fall_through]

                                # eliminate old blocks references
                                temp_block.taken.predecessors = []
                                for successor in temp_block.taken.successors:
                                    successor.predecessors.remove(temp_block.taken)

                                # delete the unused branch (taken)
                                # from the list of blocks
                                del func[temp_block.taken.label]

                                # update the taken block references
                                temp_block.fall_through.predecessors.remove(temp_block)
                                temp_block.fall_through.predecessors.append(new_block)
                            else:
                                # update new block successors
                                new_block.next_block = temp_block.taken
                                new_block.successors = [temp_block.taken]

                                # eliminate old blocks references
                                temp_block.fall_through.predecessors = []
                                for successor in temp_block.fall_through.successors:
                                    successor.predecessors.remove(temp_block.fall_through)

                                # delete the unused branch (fall
                                # through) from the list of blocks
                                del func[temp_block.fall_through.label]

                                # update the taken block references
                                temp_block.taken.predecessors.remove(temp_block)
                                temp_block.taken.predecessors.append(new_block)

                            # update the block list references
                            blocks_list[block_pos] = new_block
                            func[temp_block.label] = new_block
                            self.blocks_control.functions[func_name][new_block.label] = new_block

                            # add a new instruction to replace the cbranch
                            new_block.instructions[-1] = ('jump', new_block.next_block.label)
                        else:
                            # if a load or store and
                            # does not involve globals
                            # change instruction by a literal
                            if '*' not in inst[0]:
                                block.instructions[inst_pos] = (f'literal_{opt_type}', constants[source], inst[2])
                                constants[inst[-1]] = constants[source]
                    else:
                        # if source is not a constant
                        # set target as not a constant too
                        constants[inst[-1]] = False
                # deals with binary operation
                elif op[0] in self.binary_ops:
                    # get operands
                    left_op = inst[1]
                    right_op = inst[2]

                    # check if constant value of operand
                    # is a reference to another constant
                    # happens when load %3 %4 do the check
                    # for both left and right
                    if left_op in constants:
                        if isinstance(constants[left_op], str):
                            if constants[left_op] in constants and constants[constants[left_op]] is not False:
                                left_op = constants[constants[left_op]]
                            elif left_op in constants:
                                constants[left_op] = False
                    else:
                        constants[inst[-1]] = False

                    if right_op in constants:
                        if isinstance(constants[right_op], str):
                            if constants[right_op] in constants and constants[constants[right_op]] is not False:
                                right_op = constants[constants[right_op]]
                            elif right_op in constants:
                                constants[right_op] = False
                    else:
                        constants[inst[-1]] = False

                    # make sure both left and right operators are constants
                    if left_op in constants and right_op in constants and\
                            constants[left_op] is not False and constants[right_op] is not False:

                        # get constants values and convert them to operation type
                        left_value, right_value = str(constants[left_op]), str(constants[right_op])
                        left_value, right_value = eval(opt_type + '(' + left_value + ')'),\
                                                  eval(opt_type + '(' + right_value + ')')

                        # create a binary operation
                        # function instance
                        func_op = self.binary_fold[op[0]]
                        # make the operation
                        result = func_op(left_value, right_value)
                        # if result is a bool cast to int
                        result = int(result) if op[0] in self.comparison_ops else result

                        # convert binary operation to a literal
                        block.instructions[inst_pos] = (f"literal_{opt_type}", result, inst[3])
                        constants[inst[3]] = result
                    else:
                        constants[inst[-1]] = False

        # print if in debug mode
        if debug:
            print('=' * len('== Constant Propagation =='))


    def eliminate_single_jumps(self, func, func_name, debug=False):
        """
            Function that merges two blocks the previous one
            and the next one if the current block has only a
            jump instruction.

            :param func: dict
            :param func_name: str
            :param debug: bool
            :return: None
        """
        # print if in debug mode
        if debug:
            print()
            print("== Eliminate Single Jumps ==")

        # get a list of blocks labels
        blocks_label = list(func.keys())
        # get a list of block objects
        blocks_list = [func[block_lb] for block_lb in blocks_label]
        # create an empty set
        # of function to remove
        remove_from_func = set()

        # iterate over all blocks
        for block_pos, block in enumerate(blocks_list):
            # check if block has only two
            # instructions a label and a jump
            if len(block.instructions) == 2:
                # check if last block
                # instruction is a jump
                if block.instructions[-1][0] == 'jump':
                    # print if in debug mode
                    if debug:
                        print(f"    Block: {block.label}")
                        print(f"    Target: {block.instructions[-1][1]}")

                    # get the next block label
                    jump_target = block.instructions[-1][1]

                    # iterate over all predecessors of the
                    # current block updating the references
                    for predecessor in block.predecessors:
                        # print if in debug mode
                        if debug:
                            print(f"    Predecessor: {predecessor}")

                        # if block is uc_block.ConditionBlock
                        # has a special treatment
                        if isinstance(predecessor, ConditionBlock):
                            # get the cbranch operation, expression to test
                            # taken and fall through block
                            op, expr_test, lbl_taken, lbl_fall = predecessor.instructions[-1]

                            # print if in debug mode
                            if debug:
                                print(f"        Predecessor {predecessor.label} is a Condition.")

                            # if the taken is the previous
                            # block from the current one
                            if predecessor.taken.label == block.label:
                                # print if in debug mode
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

                                # print if in debug mode
                                if debug:
                                    print(f"            Next block {block.next_block.label} predecessor: {block.next_block.predecessors}")
                                remove_from_func.add(block.label)
                            # if the fall_through is the previous
                            # block from the current one
                            else:
                                # print if in debug mode
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

                                # add current block to remove set
                                remove_from_func.add(block.label)

                            # update cbranch instruction
                            predecessor.instructions[-1] = (op, expr_test, lbl_taken, lbl_fall)
                        # if block is uc_block.Block
                        # has a special treatment
                        elif isinstance(predecessor, Block):
                            # print if in debug mode
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

                            # update the jump instruction
                            predecessor.instructions[-1] = ('jump', jump_target)

                            # add current block to the remove set
                            remove_from_func.add(block.label)

        # print if in debug mode
        if debug:
            print(f"    Remove from func: {remove_from_func}")

        # remove block references
        for key in remove_from_func:
            del self.blocks_control.functions[func_name][key]

        # print if in debug mode
        if debug:
            print('=' * len("== Eliminate Single Jumps =="))


    def generate_opt_code(self):
        """
            Generate optimized code
            from the optimized blocks.

            :return: None
        """
        # create an empty
        # list of codes
        code = []

        # iterate over all functions
        for func in self.blocks_control.functions:
            # iterate over all blocks
            for block_lb in self.blocks_control.functions[func]:
                # get block
                block = self.blocks_control.functions[func][block_lb]
                # iterate over all instructions
                for inst in block.instructions:
                    # 'entry' is a special label
                    # we must ignore
                    if 'entry' not in inst[0]:
                        code.append(inst)

        # update the code attribute
        self.code = self.blocks_control.globals + code


    def optimize_code(self):
        """
            Function that controls the optimization flow.

            :return: None
        """
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
            self.dead_code_elimination(self.blocks_control.functions[func], debug=False)
            self.eliminate_unnecessary_alloc(self.blocks_control.functions[func], debug=False)

            # circuit single jumps
            self.eliminate_single_jumps(self.blocks_control.functions[func], func, debug=False)
            self.all_blocks = self.blocks_control.create_block_list(func)

            # print if in debug mode
            if debug:
                # update list of blocks
                self.all_blocks = self.blocks_control.create_block_list(func)

                cfg = CFG(f"{func}-opt")
                cfg.view(self.blocks_control.functions[func]['%entry'], self.all_blocks)

        # generate optimized code
        self.generate_opt_code()
        print(self.blocks_control.functions)
