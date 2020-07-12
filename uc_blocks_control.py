##################################################
# uc_blocks_control.py                           #
#                                                #
# Code for create basic blocks.                  #
#                                                #
# Authors: Luiz Cartolano && Erico Faustino      #
##################################################
from uc_block import Block, ConditionBlock, CFG


class ControlBlocks():
    """
        Class to create the CFG.
    """
    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.functions = dict()
        self.basic_blocks = dict()
        self.globals = []
        self.pre_blocks = dict()
        self.cfg_list = []
        self.non_opt_blocks = None


    def split_globals(self):
        """
            Function to separate globals.

            :return: None
        """
        self.globals = [code for code in self.ir_list if 'global' in code[0]]
        self.ir_list = [code for code in self.ir_list if not 'global' in code[0]]


    def split_functions(self):
        """
            Split to separate functions from the IR.

            :return: None
        """
        # separate globals
        self.split_globals()
        # init function name
        func_name = ''

        # iterate over the ir list to get a pre-block
        for code in self.ir_list:
            # if code is a define
            # get function name
            if code[0].startswith('define'):
                func_name = code[1][1:]
                # initialize dict of functions
                self.functions[func_name] = [code]
            # append code to dict of functions
            self.functions[func_name].append(code)


    def create_pre_blocks(self):
        """
            Create a pre block instance.

            :return: None
        """
        # iterate over functions
        for key in self.functions:
            # get function IR
            function_ir = self.functions[key]
            # set new label
            label = ''
            # restart functions dict
            self.functions[key] = dict()

            # ignore blocks with only labels
            if len(function_ir) <= 1:
                continue

            # iterate over function instructions
            for code in function_ir:
                # set a new block
                if len(code) == 1 and 'return' not in code[0]:
                    label = f'%{code[0]}'
                    self.functions[key][label] = Block(label=label)
                # set an entry block
                elif code[0].startswith('define'):
                    label = '%entry'
                    self.functions[key][label] = Block(label=label)
                    self.functions[key][label].append(code)
                # append to current block
                else:
                    self.functions[key][label].append(code)


    def convert_conditional_block(self, block):
        """
            Convert a normal block to a
            conditional one.

            :param block: uc_block.Block
            :return: uc_block.ConditionBlock
        """
        # create block
        cond_block = ConditionBlock(block.label)
        # update instruction
        cond_block.instructions = block.instructions

        return cond_block


    def convert_conditional_blocks(self):
        """
            Iterate over all functions converting
            normal blocks to conditionals if needed.

            :return: None
        """
        # get pre blocks
        pre_blocks = self.functions
        # iterate over functions
        for func in pre_blocks:
            # iterate over blocks
            for labels in pre_blocks[func]:
                # get block
                block = pre_blocks[func][labels]
                # check if last instruction is
                # cbranch, if yes convert block
                if block.take_cbranch():
                    self.functions[func][labels] = \
                        self.convert_conditional_block(block)


    def print_pre_blocks(self):
        """
            Debug function.

            :return: None
        """
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
        """
            Get all jumps in a block.

            :param ir_list: list
            :param func_blocks: dict
            :return: list, list
        """
        # create empty list
        labels = []
        blocks = []
        # iterate over IR list
        for code in ir_list:
            # check if code is a jump
            if code[0] == 'jump':
                # add label and block to the list
                labels.append(code[1])
                blocks.append(func_blocks[code[1]])

        return labels, blocks


    def create_links(self, func):
        """
            Main function that create links
            between blocks on CFG.

            :param func: dict
            :return: None
        """
        # get the dict block
        func_blocks = self.functions[func]
        block_labels_names = list(func_blocks.keys())
        ignore = {}

        for counter, label in enumerate(block_labels_names):
            if label not in ignore:
                current_block = func_blocks[label]
            else:
                continue

            if isinstance(current_block, ConditionBlock):
                # check if exist any jump block
                # in the middle of the code
                jump_labels, jump_blocks =\
                    self.get_jump_labels(current_block.instructions, func_blocks)

                if len(jump_blocks) != 0:
                    # add next block predecessors
                    for next_block in jump_blocks:
                        current_block.successors.append(next_block)
                        next_block.predecessors.append(current_block)

                # deal with the true condition
                true_block = func_blocks[current_block.instructions[-1][-2]]

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

                    if len(jump_blocks) != 1:
                        remove_label = jump_labels.pop()
                        del jump_blocks[-1]
                        del self.functions[func][remove_label]
                        del current_block.instructions[-1]
                        ignore[remove_label] = True

                    # add next block predecessors
                    for next_block in jump_blocks:
                        # add current blocks successors
                        current_block.successors.append(next_block)
                        next_block.predecessors.append(current_block)

                    # add current block next block
                    current_block.next_block = jump_blocks[0]
                else:
                    # next block is the next label on list
                    # check if exist any jump
                    # in the instructions
                    jump_labels, jump_blocks =\
                        self.get_jump_labels(current_block.instructions, func_blocks)

                    if len(jump_blocks) != 0:
                        # add next block predecessors
                        for next_block in jump_blocks:
                            current_block.successors.append(next_block)
                            next_block.predecessors.append(current_block)

                    if counter + 1 < len(block_labels_names):
                        # get next block
                        next_block = func_blocks[block_labels_names[counter + 1]]
                        # add successors
                        current_block.successors.append(next_block)
                        current_block.next_block = next_block
                        # add predecessor to next block
                        next_block.predecessors.append(current_block)


    def create_block_list(self, func):
        """
            Create a list of blocks objects.

            :param func: dict
            :return: list
        """
        # empty list
        all_blocks = []

        # iterate over all blocks
        for label in self.functions[func]:
            # get block
            block = self.functions[func][label]
            # append block to list
            if len(block.instructions) > 1:
                all_blocks.append(self.functions[func][label])

        return all_blocks


    def create_basic_blocks(self):
        """
            Function that controls the CFG creation.
            :return: None
        """
        debug = False

        # split IR in functions
        self.split_functions()
        # split IR in blocks
        self.create_pre_blocks()
        # convert blocks to
        # conditional if necessary
        self.convert_conditional_blocks()

        # iterate over blocks creating
        # predecessors/sucessors/others
        for func in self.functions:
            # create links between blocks
            self.create_links(func)

            if debug:
                # create all blocks list for debug only
                all_blocks = self.create_block_list(func)
                # create CFG obj
                cfg = CFG(func)
                # make CFG pdf
                cfg.view(self.functions[func]['%entry'], all_blocks)
                self.cfg_list.append(cfg)

        self.non_opt_blocks = self.functions.copy()
