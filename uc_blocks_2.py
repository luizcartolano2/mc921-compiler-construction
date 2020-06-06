from uc_block import Block, BasicBlock, ConditionBlock


class ControlBlocks():
    def __init__(self, ir_list):
        self.ir_list = ir_list
        self.functions = dict()
        self.basic_blocks = dict()
        self.globals = []


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
                    self.functions[key][label] = []
                elif code[0] == 'define':
                    label = '%entry'
                    self.functions[key][label] = []
                else:
                    self.functions[key][label].append(code)


    def print_pre_blocks(self):
        for key in self.functions:
            print(f"FUNCTION: {key}")
            blocks = self.functions[key]
            for label in blocks:
                print(f"\tBLOCK: {label}")
                ir = blocks[label]
                for code in ir:
                    print(f"\t\t{code}")


    def create_basic_blocks(self):
        self.split_functions()
        self.create_pre_blocks()

        self.print_pre_blocks()
