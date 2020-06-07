from uc_block import Block, ConditionBlock, CFG


class ControlBlocks():
    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.functions = dict()
        self.basic_blocks = dict()
        self.globals = []
        self.pre_blocks = dict()


    def split_globals(self):
        self.globals = [code for code in self.ir_list if 'global' in code[0]]
        self.ir_list = [code for code in self.ir_list if not 'global' in code[0]]


    def split_functions(self):
        self.split_globals()
        func_name = ''

        # iterate over the ir list to get a pre-block
        for code in self.ir_list:
            if code[0] == 'define':
                func_name = code[1][1:]
                self.functions[func_name] = []
            self.functions[func_name].append(code)


    def create_pre_blocks(self):
        for key in self.functions:
            function_ir = self.functions[key]
            label = ''
            self.functions[key] = dict()
            for code in function_ir:
                if len(code) == 1 and 'return' not in code[0]:
                    label = f'%{code[0]}'
                    self.functions[key][label] = Block(label=label)
                elif code[0] == 'define':
                    label = '%entry'
                    self.functions[key][label] = Block(label=label)
                else:
                    self.functions[key][label].append(code)


    def convert_conditional_block(self, block):
        cond_block = ConditionBlock(block.label)
        cond_block.instructions = block.instructions

        return cond_block


    def convert_conditional_blocks(self):
        pre_blocks = self.functions
        for func in pre_blocks:
            for lable in pre_blocks[func]:
                block = pre_blocks[func][lable]

                if block.take_cbranch():
                    self.functions[func][lable] = \
                        self.convert_conditional_block(block)


    def print_pre_blocks(self):
        for key in self.functions:
            print(f"FUNCTION: {key}")
            blocks = self.functions[key]
            # iterate over labels
            for label in blocks:
                print(f"\tBLOCK: {label}")
                ir = blocks[label].instructions
                for code in ir:
                    print(f"\t\t{code}")


    def get_jump_labels(self, ir_list, func_blocks):
        labels = []
        blocks = []
        for code in ir_list:
            if code[0] == 'jump':
                labels.append(code[1])
                blocks.append(func_blocks[code[1]])

        return labels, blocks


    def create_links(self, func):
        # get the dict block
        func_blocks = self.functions[func]
        block_labels_names = list(func_blocks.keys())

        for counter, label in enumerate(block_labels_names):
            current_block = func_blocks[label]
            if isinstance(current_block, ConditionBlock):
                # check if exist any jump block
                # in the middle of the code
                jump_labels, jump_blocks =\
                    self.get_jump_labels(current_block.instructions, func_blocks)

                if len(jump_blocks) != 0:
                    current_block.successors.append(jump_blocks)
                    # add next block predecessors
                    for next_block in jump_blocks:
                        next_block.predecessors.append(current_block)

                # deal with the true condition
                true_block = func_blocks[current_block.instructions[-1][-2]]
                current_block.next_block = true_block
                
                # add current block successor
                current_block.successors.append(true_block)
                current_block.taken = true_block
                # add next block predecessor
                true_block.predecessors.append(current_block)

                # deal with the false condition
                false_label = func_blocks[current_block.instructions[-1][-1]]
                # add current block successor
                current_block.successors.append(false_label)
                current_block.fall_through = false_label
                # add next block predecessor
                false_label.predecessors.append(current_block)

                # add next block
                current_block.next_block = false_label
            else:
                if current_block.instructions[-1][0] == 'jump':
                    # block has a jump so next
                    # block is going to be the jump
                    # label
                    jump_labels, jump_blocks =\
                        self.get_jump_labels(current_block.instructions, func_blocks)

                    # add current blocks successors
                    current_block.successors.append(jump_blocks)
                    # add next block predecessors
                    for next_block in jump_blocks:
                        next_block.predecessors.append(current_block)

                    # add current block next block
                    current_block.next_block = jump_blocks[-1]
                else:
                    # next block is the next label on list
                    # check if exist any jump
                    # in the instructionsttr
                    jump_labels, jump_blocks =\
                        self.get_jump_labels(current_block.instructions, func_blocks)

                    if len(jump_blocks) != 0:
                        current_block.successors.append(jump_blocks)
                        # add next block predecessors
                        for next_block in jump_blocks:
                            next_block.predecessors.append(current_block)

                    if counter + 1 < len(block_labels_names):
                        # get next block
                        next_block = func_blocks[block_labels_names[counter + 1]]
                        # add successors
                        current_block.successors.append(next_block)
                        current_block.next_block = next_block
                        # add predecessor to next block
                        next_block.predecessors.append(current_block)


    def create_basic_blocks(self):
        self.split_functions()
        self.create_pre_blocks()

        self.convert_conditional_blocks()

        # iterate over blocks creating
        # predecessors/sucessors/others
        for func in self.functions:
            self.create_links(func)
            cfg = CFG(func)
            cfg.view(self.functions[func]['%entry'])
            import pdb; pdb.set_trace()

        self.print_pre_blocks()

