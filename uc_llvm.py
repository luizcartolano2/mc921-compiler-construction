##################################################
# uc_llvm.py                                     #
#                                                #
# Code for the convert ucIR to LLVM              #
#                                                #
# Authors: Luiz Cartolano && Erico Faustino      #
##################################################
from ctypes import CFUNCTYPE, c_int

from llvmlite import ir, binding

bool_type = ir.IntType(1)
llvm_false = ir.Constant(bool_type, False)
llvm_true = ir.Constant(bool_type, True)
void_type = ir.VoidType()
char_type = ir.IntType(8)
int_type = ir.IntType(32)
i64_type = ir.IntType(64)
float_type = ir.DoubleType()
charptr_ty = char_type.as_pointer()
# voidptr is used in printf/scanf declarations
voidptr_ty = char_type.as_pointer()

llvm_type_dict = {
    'int': int_type,
    'float': float_type,
    'char': char_type,
    'void': void_type,
    'string': charptr_ty,
}


def extract_operation(inst):
    """
        The method that extracts the operation of an instruction

        ...

        Parameters
        ----------
            inst :
                The instruction.

    """
    # create a modifier
    # dict to store info
    # associated with array
    # or pointer
    modifier = {}
    # create var to get op type
    uc_type = None
    aux = inst.split('_')

    # get opcode
    opcode = aux[0]

    if len(aux) > 1:
        # if inst has a
        # type associated
        uc_type = aux[1]

        # if inst has info
        # associated with array
        # or pointer
        if len(aux) > 2:
            for i, val in enumerate(aux[2:]):
                if val.isdigit():
                    modifier['dim' + str(i)] = val
                elif val == '*':
                    modifier['prt' + str(i)] = val

    return opcode, uc_type, modifier


class LLVMBuilder:

    def __init__(self, module):
        self.builder = None
        self.functions = None
        self.location = {}
        self.module = module
        self.params = []

    def get_location(self, target):
        """
            The method that gets the location of a target

            ...

            Parameters
            ----------
                target :
                    The instruction target.

        """
        location = None

        if target[0] == '%' and target in self.location:
            location = self.location[target]
        elif target[0] == '@' and target[1:] in self.module.globals:
            location = self.module.get_global(target[1:])

        return location

    def new_function(self, inst):
        """
            The method that creates a new function

            ...

            Parameters
            ----------
                inst :
                    The instruction.

        """
        operand, func_name, func_args = inst

        if func_name[1:] in self.module.globals:
            self.functions = self.module.get_global(func_name[1:])
        else:
            uc_type = operand.split('_')[1]
            args_types = [llvm_type_dict[arg] for arg in [item[0] for item in func_args]]
            func_type = ir.FunctionType(llvm_type_dict[uc_type], args_types)
            self.functions = ir.Function(self.module, func_type, name=func_name[1:])

        for arg_id, arg_target in enumerate([item[1] for item in func_args]):
            self.location[arg_target] = self.functions.args[arg_id]

    def cio(self, func_name, string_format, *target):
        """
            The method cio

            ...

            Parameters
            ----------
                func_name :
                    The function name.
                string_format :
                    The string format.
                *target :
                    The instruction type.

        """
        byte_array = bytearray((string_format + "\00").encode('ascii'))
        len_byte_array = len(byte_array)
        fmt_bytes = ir.Constant(ir.ArrayType(char_type, len_byte_array), byte_array)

        mod = self.builder.module

        data = ir.GlobalVariable(mod, fmt_bytes.type, name=mod.get_unique_name('.fmt'))
        data.linkage = 'internal'
        data.global_constant = True
        data.initializer = fmt_bytes
        global_fmt = data

        fn = self.builder.module.get_global(func_name)
        ptr_fmt = self.builder.bitcast(global_fmt, charptr_ty)
        return self.builder.call(fn, [ptr_fmt] + list(target))

    def build_alloc(self, uc_type, target, **kwargs):
        """
            The method that builds an alloc

            ...

            Parameters
            ----------
                uc_type :
                    The instruction type.
                target :
                    The instruction target.
                **kwargs :
                    Possible extra arguments.

        """
        llvm_type = llvm_type_dict[uc_type]

        for arg in list(kwargs.values()):
            llvm_type = ir.ArrayType(llvm_type, int(arg))

        target_location = self.builder.alloca(llvm_type, name=target[1:])
        self.location[target] = target_location

    def build_call(self, return_type, name, target):
        """
            The method that builds a call

            ...

            Parameters
            ----------
                return_type :
                    The return type.
                name :
                    The called instruction name.
                target :
                    The instruction target.

        """
        if name == '%':
            func_call_loc = self.builder.call(self.get_location(name), self.params)
        elif name[1:] in self.builder.module.globals:
            func_name = self.builder.module.get_global(name[1:])
            func_call_loc = self.builder.call(func_name, self.params)
        else:
            llvm_type = llvm_type_dict[return_type]
            arg_type = [arg.type for arg in self.params]
            func_type = ir.FunctionType(llvm_type, arg_type)
            func_name = ir.Function(self.module, func_type, name=name[1:])

            func_call_loc = self.builder.call(func_name, self.params)

        self.location[target] = func_call_loc
        self.params = []

    def build_elem(self, uc_type, source, index, target):
        """
            The method that builds an element

            ...

            Parameters
            ----------
                uc_type :
                    The instruction type.
                source :
                    The instruction source.
                index :
                    The instruction index.
                target :
                    The instruction target.

        """
        var_source = self.get_location(source)
        var_index = self.get_location(index)
        var_base = ir.Constant(var_index.type, 0)

        if not isinstance(var_source.type.pointee.element, ir.ArrayType):
            var_location = self.builder.gep(var_source, [var_base, var_index])
        else:
            col = ir.Constant(int_type, var_source.type.pointee.element.count)
            const_i = self.builder.sdiv(var_index, col)
            const_j = self.builder.srem(var_index, col)
            var_aux = self.builder.gep(var_source, [var_base, const_i])
            var_location = self.builder.gep(var_aux, [var_base, const_j])

        self.location[target] = var_location

    def build_get(self, source, target, **kwargs):
        """
            The method that builds a get

            ...

            Parameters
            ----------
                source :
                    The instruction source.
                target :
                    The instruction target.
                **kwargs :
                    Possible extra arguments.

        """
        self.builder.store(self.get_location(source),
                           self.get_location(target))

    def build_literal(self, var_type, constant, target):
        """
            The method that builds a literal

            ...

            Parameters
            ----------
                var_type :
                    The variable type.
                constant :
                    The constant value.
                target :
                    The instruction target.

        """
        if var_type == 'char':
            literal_val = llvm_type_dict[var_type](ord(constant))
        else:
            literal_val = llvm_type_dict[var_type](constant)
        literal_location = self.get_location(target)
        if literal_location:
            self.builder.store(literal_val, literal_location)
        else:
            self.location[target] = literal_val

    def build_load(self, uc_type, source, target, **kwargs):
        """
            The method that builds a load

            ...

            Parameters
            ----------
                uc_type :
                    The instruction type.
                source :
                    The instruction source.
                target :
                    The instruction target.
                **kwargs :
                    Possible extra arguments.

        """
        target_location = self.builder.load(self.get_location(source))

        self.location[target] = target_location

    def build_param(self, param_type, param_source):
        """
            The method that builds a parameter

            ...

            Parameters
            ----------
                param_type :
                    The parameter type.
                param_source :
                    The parameter source.

        """
        self.params.append(self.get_location(param_source))

    def build_print(self, val_type, target):
        """
            The method that builds a print

            ...

            Parameters
            ----------
                val_type :
                    The value type.
                target :
                    The instruction target.

        """
        if target:
            value_to_print = self.get_location(target)
            if val_type == 'int':
                self.cio('printf', '%d', value_to_print)
            elif val_type == 'float':
                self.cio('printf', '%f', value_to_print)
            elif val_type == 'char':
                self.cio('printf', '%c', value_to_print)
            elif val_type == 'string':
                self.cio('printf', '%s', value_to_print)
        else:
            self.cio('printf', '\n')

    def build_read(self, var_type, target):
        """
            The method that builds a read

            ...

            Parameters
            ----------
                var_type :
                    The variable type.
                target :
                    The instruction target.

        """
        read_target = self.get_location(target)
        if var_type == 'int':
            self.cio('scanf', '%d', read_target)
        elif var_type == 'float':
            self.cio('scanf', '%lf', read_target)
        elif var_type == 'char':
            self.cio('scanf', '%c', read_target)

    def build_store(self, uc_type, source, target, **kwargs):
        """
            The method that builds a store

            ...

            Parameters
            ----------
                uc_type :
                    The type.
                source :
                    The instruction source.
                target :
                    The instruction target.
                **kwargs :
                    Possible extra arguments.

        """
        location_source = self.get_location(source)
        location_target = self.get_location(target)

        if isinstance(location_target.type.pointee, ir.ArrayType):
            var_size = 1
            for arg in kwargs.values():
                var_size *= int(arg)

            if uc_type == 'float':
                var_size *= 8
            elif uc_type == 'int':
                var_size *= int_type.width // 8

            memory_copy = self.module.declare_intrinsic('llvm.memcpy', [charptr_ty, charptr_ty, i64_type])
            source_pointer = self.builder.bitcast(location_source, charptr_ty)
            target_pointer = self.builder.bitcast(location_target, charptr_ty)

            self.builder.call(memory_copy, [target_pointer, source_pointer, ir.Constant(i64_type, var_size), llvm_false])
        else:
            self.builder.store(location_source, location_target)

    def build_add(self, expr_type, left, right, target):
        """
            The method that builds a sum

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.add(self.get_location(left),
                                                self.get_location(right))
        else:
            result_location = self.builder.fadd(self.get_location(left),
                                               self.get_location(right))

        self.location[target] = result_location

    def build_sub(self, expr_type, left, right, target):
        """
            The method that builds a subtraction

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.sub(self.get_location(left),
                                               self.get_location(right))
        else:
            result_location = self.builder.fsub(self.get_location(left),
                                               self.get_location(right))

        self.location[target] = result_location

    def build_mul(self, expr_type, left, right, target):
        """
            The method that builds a multiplication

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.mul(self.get_location(left),
                                                self.get_location(right))
        else:
            result_location = self.builder.fmul(self.get_location(left),
                                               self.get_location(right))
        self.location[target] = result_location

    def build_div(self, expr_type, left, right, target):
        """
            The method that builds a division

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.sdiv(self.get_location(left),
                                                self.get_location(right))
        else:
            result_location = self.builder.fdiv(self.get_location(left),
                                                self.get_location(right))

        self.location[target] = result_location

    def build_mod(self, expr_type, left, right, target):
        """
            The method that builds a mod expression

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.srem(self.get_location(left),
                                                self.get_location(right))
        else:
            result_location = self.builder.frem(self.get_location(left),
                                                self.get_location(right))

        self.location[target] = result_location

    def build_and(self, expr_type, left, right, target):
        """
            The method that builds an and expression

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        target_loc = self.builder.and_(self.get_location(left),
                                       self.get_location(right))

        self.location[target] = target_loc

    def build_or(self, expr_type, left, right, target):
        """
            The method that builds an or expression

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        target_loc = self.builder.or_(self.get_location(left),
                                      self.get_location(right))

        self.location[target] = target_loc

    def build_ge(self, expr_type, left, right, target):
        """
            The method that builds a greater of equals than

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.icmp_signed('>=',
                                                        self.get_location(left),
                                                        self.get_location(right))
        else:
            result_location = self.builder.fcmp_ordered('>=',
                                                       self.get_location(left),
                                                       self.get_location(right))

        self.location[target] = result_location

    def build_le(self, expr_type, left, right, target):
        """
            The method that builds a less of equals than

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.icmp_signed('<=',
                                                        self.get_location(left),
                                                        self.get_location(right))
        else:
            result_location = self.builder.fcmp_ordered('<=',
                                                       self.get_location(left),
                                                       self.get_location(right))

        self.location[target] = result_location

    def build_gt(self, expr_type, left, right, target):
        """
            The method that builds a greater than

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.icmp_signed('>',
                                                        self.get_location(left),
                                                        self.get_location(right))
        else:
            result_location = self.builder.fcmp_ordered('>',
                                                       self.get_location(left),
                                                       self.get_location(right))

        self.location[target] = result_location

    def build_lt(self, expr_type, left, right, target):
        """
            The method that builds a less than

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.icmp_signed('<',
                                                        self.get_location(left),
                                                        self.get_location(right))
        else:
            result_location = self.builder.fcmp_ordered('<',
                                                       self.get_location(left),
                                                       self.get_location(right))

        self.location[target] = result_location

    def build_eq(self, expr_type, left, right, target):
        """
            The method that builds an equals expression

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """

        if expr_type in ['int', 'char']:
            result_location = self.builder.icmp_signed('==',
                                                       self.get_location(left),
                                                       self.get_location(right))
        else:
            result_location = self.builder.fcmp_ordered('==',
                                                       self.get_location(left),
                                                       self.get_location(right))

        self.location[target] = result_location

    def build_ne(self, expr_type, left, right, target):
        """
            The method that builds a not equals expression

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                left :
                    The left value.
                right :
                    The right value.
                target :
                    The result target.

        """
        if expr_type in ['int', 'char']:
            result_location = self.builder.icmp_signed('!=',
                                                       self.get_location(left),
                                                       self.get_location(right))
        else:
            result_location = self.builder.fcmp_ordered('!=',
                                                        self.get_location(left),
                                                        self.get_location(right))

        self.location[target] = result_location

    def build_sitofp(self, expr_type, source, target):
        """
            The method that builds sitofp

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                source :
                    The instruction source.
                target :
                    The instruction target.

        """
        target_loc = self.builder.sitofp(self.get_location(source),
                                         float_type)

        self.location[target] = target_loc

    def build_fptosi(self, expr_type, source, target):
        """
            The method that builds fptosi

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                source :
                    The instruction source.
                target :
                    The instruction target.

        """
        target_loc = self.builder.fptosi(self.get_location(source),
                                         int_type)

        self.location[target] = target_loc

    def build_return(self, expr_type, target=None):
        """
            The method that builds a return

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                target :
                    The return target.

        """
        if target:
            self.builder.ret(self.get_location(target))
        else:
            self.builder.ret_void()

    def build_jump(self, expr_type, target):
        """
            The method that builds a jump

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                target :
                    The jump target.

        """
        self.builder.branch(self.get_location(target))

    def build_cbranch(self, expr_type, expr_test, target, fall_through):
        """
            The method that builds a conditional branch

            ...

            Parameters
            ----------
                expr_type :
                    The expression type.
                expr_test :
                    The expression test.
                target :
                    The branch target.
                fall_through :
                    The branch fall through.

        """
        self.builder.cbranch(self.get_location(expr_test),
                             self.get_location(target),
                             self.get_location(fall_through)
                             )

    def build(self, inst):
        """
            The method to build a instruction

            ...

            Parameters
            ----------
                inst :
                    The instruction.

        """
        opcode, uc_type, modifier = extract_operation(inst[0])

        args = inst[1:] if len(inst) > 1 else (None,)

        getattr(self, f"build_{opcode}")(uc_type, *inst[1:], **modifier)

    def create_blocks(self, func_blocks_dict):
        """
            The method to create the blocks for LLVM

            ...

            Parameters
            ----------
                func_blocks_dict :
                    The dictionary of function blocks.

        """
        for block_label in func_blocks_dict:
            block = func_blocks_dict[block_label]
            if block_label == '%entry':
                self.new_function(block.instructions[1])
            ir_block_loc = self.functions.append_basic_block(block_label)
            self.location[block.label] = ir_block_loc

    def build_blocks(self, func_blocks_dict):
        """
            The method to build the blocks for LLVM

            ...

            Parameters
            ----------
                func_blocks_dict :
                    The dictionary of function blocks.

        """
        for block_label in func_blocks_dict:
            block = func_blocks_dict[block_label]
            ir_block_loc = self.location[block.label]
            self.builder = ir.IRBuilder(ir_block_loc)

            if block_label == '%entry':
                for inst in block.instructions[2:]:
                    self.build(inst)
            else:
                for inst in block.instructions[1:]:
                    self.build(inst)


class LLVMCodeGenerator:
    def __init__(self, control_blocks, opt):
        # get dict with IR functions and blocks
        if opt:
            self.functions = control_blocks.functions
        else:
            self.functions = control_blocks.non_opt_blocks
        # get IR globals
        self.global_codes = control_blocks.globals
        # import binding from llvmlite
        # and initialize it
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()

        # create a ir module on llvmlite
        self.module = ir.Module(name=__file__)
        self.module.triple = self.binding.get_default_triple()

        # create an execution engine
        self.engine = self.__create_execution_engine()

        # declare printf / scanf functions
        self.__declare_printf_function()
        self.__declare_scanf_function()

    def __create_execution_engine(self):
        """
            The method that creates the execution engine

            ...

            Parameters
            ----------
                None

        """
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)

        return engine

    def __declare_printf_function(self):
        """
            The method that declares the printf functions

            ...

            Parameters
            ----------
                None

        """
        printf_ty = ir.FunctionType(int_type, [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

    def __declare_scanf_function(self):
        """
            The method that declares the scanf functions

            ...

            Parameters
            ----------
                None

        """
        scanf_ty = ir.FunctionType(int_type, [voidptr_ty], var_arg=True)
        scanf = ir.Function(self.module, scanf_ty, name="scanf")
        self.scanf = scanf

    def __compile_ir(self):
        """
            The method that compiles the IR

            ...

            Parameters
            ----------
                None

        """
        llvm_ir = str(self.module)
        mod = self.binding.parse_assembly(llvm_ir)
        mod.verify()

        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()

        return mod

    def save_ir(self, output_file):
        """
            The method that saves the IR on an output file

            ...

            Parameters
            ----------
                output_file :
                    The output file.

        """
        try:
            output_file.write(str(self.module))
        except AttributeError:
            for key, value in self.module.globals.items():
                print(key, value)

    def execute_ir(self, opt, opt_file):
        """
            The method that executes the IR

            ...

            Parameters
            ----------
                None
                :param opt_file: arg q o marzio tirou do cu dele
                :param opt: arg q o marzio tirou do cu dele

        """
        mod = self.__compile_ir()

        if opt:
            # apply some optimization passes on module
            pmb = self.binding.create_pass_manager_builder()
            pm = self.binding.create_module_pass_manager()

            pmb.opt_level = 0
            if opt == 'ctm' or opt == 'all':
                # Sparse conditional constant propagation and merging
                pm.add_sccp_pass()
                # Merges duplicate global constants together
                pm.add_constant_merge_pass()
                # Combine inst to form fewer, simple inst
                # This pass also does algebraic simplification
                pm.add_instruction_combining_pass()
            if opt == 'dce' or opt == 'all':
                pm.add_dead_code_elimination_pass()
            if opt == 'cfg' or opt == 'all':
                # Performs dead code elimination and basic block merging
                pm.add_cfg_simplification_pass()

            pmb.populate(pm)
            pm.run(mod)
            opt_file.write(str(mod))

        # Obtain a pointer to the compiled 'main' - it's the address of its JITed code in memory.
        main_ptr = self.engine.get_function_address('main')
        # To convert an address to an actual callable thing we have to use
        # CFUNCTYPE, and specify the arguments & return type.
        main_function = CFUNCTYPE(c_int)(main_ptr)
        # Now 'main_function' is an actual callable we can invoke
        res = main_function()

    def __generate_global_instructions(self, global_inst):
        """
            The method to generate the global instructions

            ...

            Parameters
            ----------
                global_inst :
                    The global instructions.

        """
        for inst in global_inst:
            _, uc_type, modifier = extract_operation(inst[0])
            llvm_type = llvm_type_dict[uc_type]
            var_name = inst[1][1:]
            var_value = inst[2]
            func_signature = isinstance(var_value, list)

            if func_signature and isinstance(var_value[0], list):
                func_signature = False
            elif func_signature and var_value[0] not in llvm_type_dict:
                func_signature = False

            if uc_type in ['string']:
                # create a byte array in order to store the string
                byte_array = bytearray((var_value + "\00").encode('utf-8'))
                len_byte_array = len(byte_array)
                ir_constant = ir.Constant(ir.ArrayType(char_type, len_byte_array), byte_array)
                # create a global variable to refer the string
                ir_global_var = ir.GlobalVariable(self.module, ir_constant.type, var_name)
                # initialize global var
                ir_global_var.initializer = ir_constant
                # set var as constant
                ir_global_var.global_constant = True
            elif modifier and not func_signature:
                for arg in reversed(list(modifier.values())):
                    llvm_type = ir.ArrayType(llvm_type, int(arg))
                ir_global_var = ir.GlobalVariable(self.module, llvm_type, var_name)
                ir_global_var.initializer = ir.Constant(llvm_type, var_value)
            elif func_signature:
                # ptr to function
                _sig = [llvm_type_dict[arg] for arg in var_value]
                ir_func_type = ir.FunctionType(llvm_type_dict[uc_type], _sig)
            else:
                # normal global var like int x = 2
                ir_global_var = ir.GlobalVariable(self.module, llvm_type, var_name)
                if var_value:
                    ir_global_var.initializer = ir.Constant(llvm_type, var_value)

    def build(self):
        """
            The method to visit the program

            ...

            Parameters
            ----------
                node :
                    The Node.

        """
        self.__generate_global_instructions(self.global_codes)

        for func in self.functions:
            func_dict = self.functions[func]
            llvm_block = LLVMBuilder(self.module)
            llvm_block.create_blocks(func_dict)
            llvm_block.build_blocks(func_dict)
