from uc_block import Block, ConditionBlock, CFG


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
        self.binary_fold = {'add',
                            'sub',
                            'mul',
                            'div',
                            'mod',
                            'and',
                            'or',
                            'not',
                            'ne',
                            'eq',
                            'lt',
                            'le',
                            'gt',
                            'ge'
                            }

    def __set_use_def(self, inst):
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


    def compute_lv_in_out(self, func):
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
                print(block_lb)
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
                    # import pdb; pdb.set_trace()
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

        print('== Live Variable Analysis ==')
        for block_lb in block_labels:
            bb = func[block_lb]
            print(bb.label)
            print('\tuse:  ', sorted(bb.lv.use))
            print('\tdef:  ', sorted(bb.lv.defs))
            print('\tin :  ', sorted(bb.lv.ins))
            print('\tout:  ', sorted(bb.lv.out))


    def __compute_rd_defs(self, func):
        """
            Live! Ta OK!
            :param func:
            :return:
        """
        defs = {}
        blocks_label = list(func.keys())

        for block_counter, block_label in enumerate(blocks_label):
            block = func[block_label]
            for inst_counter, inst in enumerate(block.instructions[1:]):
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

        defs = self.__compute_rd_defs(func=func)

        for block_counter, block_label in enumerate(blocks_label):
            block = func[block_label]
            for inst_counter, inst in enumerate(block.instructions[1:]):
                if inst[0].split('_')[0] in self.assignment_op:
                    target = inst[-1]
                    kills = set(defs[target]) - {(block_counter, inst_counter)}
                    block.rd.kill = block.rd.kill.union(kills)
                    gen = {(block_counter, inst_counter)}
                    block.rd.gen = gen.union(block.rd.gen - kills)


    def compute_rd_in_out(self, func):
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
                    if d not in live_variables:
                        _is_dead = True
                if _is_dead:
                    dead_code.add(inst_pos)
                    self.code_to_eliminate.add(inst)
                    live_variables = live_variables.union(use)

            if debug:
                updated_instructions = []
                for inst_pos, inst in enumerate(block.instructions):
                    if inst_pos not in dead_code:
                        updated_instructions.append(inst)

                block.instructions = updated_instructions


    def eliminate_unreachable_code(self, func, debug=False):
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

            if debug:
                updated_instructions = []
                for inst_pos, inst in enumerate(block.instructions):
                    if inst_pos not in dead_code:
                        updated_instructions.append(inst)

                block.instructions = updated_instructions


    def optimize_code(self):
        debug = True

        for func in self.blocks_control.functions:
            self.all_blocks = self.blocks_control.create_block_list(func)

            self.compute_rd_in_out(self.blocks_control.functions[func])
            # make the liveness analysis
            self.compute_lv_in_out(self.blocks_control.functions[func])
            self.deadcode_elimination(self.blocks_control.functions[func], debug=True)
            self.eliminate_unreachable_code(self.blocks_control.functions[func], debug=True)
            import pdb; pdb.set_trace()
            if debug:

                # import pdb; pdb.set_trace()
                cfg = CFG(f"{func}-opt")
                # import pdb; pdb.set_trace()
                cfg.view(self.blocks_control.functions[func]['%entry'], self.all_blocks)
                # import pdb; pdb.set_trace()
                # print('oi')
