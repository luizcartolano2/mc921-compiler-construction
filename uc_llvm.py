from llvmlite import ir, binding
from ctypes import CFUNCTYPE, c_int

from uc_ast import *
from uc_block import *

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


def create_byte_array(buf):
    """
        A method used to create a byte array

        ...

        Parameters
        ----------
            buf :
                The buffer.

    """
    b = bytearray(buf)
    _len = len(b)
    return ir.Constant(ir.ArrayType(char_type, _len), b)


def get_align(left_type, width):
    """
        A

        ...

        Parameters
        ----------
            left_type :
                A.
            width :
                A.

    """
    align_value = 1
    if isinstance(left_type, ir.IntType):
        align_value = left_type.width // 8
    elif isinstance(left_type, (ir.DoubleType, ir.PointerType)):
        align_value = 8
    elif isinstance(left_type, ir.ArrayType):
        _align = get_align(left_type.element, 1)
        if width < 4:
            width = 1
        else:
            width = 4
        align_value = _align * width

    return align_value


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


class LLVMFunctionVisitor:

    def __init__(self, module):
        self.builder = None
        self.code = []
        self.functions = None
        self.location = {}
        self.module = module
        self.params = []
        self.phase = None
        self.ret_register = None

    def _get_location(self, target):
        """
            The method that gets the location of a target

            ...

            Parameters
            ----------
                target :
                    A.

        """
        try:
            if target[0] == '%':
                return self.location[target]
            elif target[0] == '@':
                return self.module.get_global(target[1:])
        except KeyError:
            return None

    @staticmethod
    def _global_constant(builder_or_module, name, value, linkage='internal'):
        """
            The method that creates a global constant

            ...

            Parameters
            ----------
                builder_or_module :
                    A.
                name :
                    A.
                value :
                    A.
                linkage :
                    A.

        """
        if isinstance(builder_or_module, ir.Module):
            mod = builder_or_module
        else:
            mod = builder_or_module.module
        data = ir.GlobalVariable(mod, value.type, name=name)
        data.linkage = linkage
        data.global_constant = True
        data.initializer = value
        data.align = 1
        return data

    def _new_function(self, inst):
        """
            The method that creates a new function

            ...

            Parameters
            ----------
                inst :
                    A.

        """
        _op, _name, _args = inst
        try:
            self.functions = self.module.get_global(_name[1:])
        except KeyError:
            _ctype = _op.split('_')[1]
            _sig = [llvm_type_dict[arg] for arg in [item[0] for item in _args]]
            funty = ir.FunctionType(llvm_type_dict[_ctype], _sig)
            self.functions = ir.Function(self.module, funty, name=_name[1:])
        for _idx, _reg in enumerate([item[1] for item in _args]):
            self.location[_reg] = self.functions.args[_idx]

    def _cio(self, fname, format, *target):
        """
            A

            ...

            Parameters
            ----------
                fname :
                    A.
                format :
                    A.
                *target :
                    A.

        """
        fmt_bytes = create_byte_array((format + '\00').encode('ascii'))
        global_fmt = self._global_constant(self.builder.module,
                                           self.builder.module.get_unique_name('.fmt'),
                                           fmt_bytes)
        fn = self.builder.module.get_global(fname)
        ptr_fmt = self.builder.bitcast(global_fmt, charptr_ty)
        return self.builder.call(fn, [ptr_fmt] + list(target))

    def _build_alloc(self, ctype, target):
        """
            The method that builds an alloc

            ...

            Parameters
            ----------
                ctype :
                    A.
                target :
                    A.

        """
        _type = llvm_type_dict[ctype]
        _location = self.builder.alloca(_type, name=target[1:])
        _location.align = get_align(_type, 1)
        self.location[target] = _location

    def _build_alloc_(self, ctype, target, **kwargs):
        """
            The method that builds an alloc

            ...

            Parameters
            ----------
                ctype :
                    A.
                target :
                    A.
                **kwargs :
                    A.

        """
        _type = llvm_type_dict[ctype]
        _width = 1
        for arg in reversed(list(kwargs.values())):
            if arg.isdigit():
                _width *= int(arg)
                _type = ir.ArrayType(_type, int(arg))
            else:
                _type = ir.PointerType(_type)
        _location = self.builder.alloca(_type, name=target[1:])
        _location.align = get_align(_type, _width)
        self.location[target] = _location

    def _build_call(self, ret_type, name, target):
        """
            The method that builds a call

            ...

            Parameters
            ----------
                ret_type :
                    A.
                name :
                    A.
                target :
                    A.

        """
        if name == '%':
            _loc = self.builder.call(self._get_location(name), self.params)
        else:
            try:
                _fn = self.builder.module.get_global(name[1:])
            except KeyError:
                _type = llvm_type_dict[ret_type]
                _sig = [arg.type for arg in self.params]
                funty = ir.FunctionType(_type, _sig)
                _fn = ir.Function(self.module, funty, name=name[1:])
            _loc = self.builder.call(_fn, self.params)
        self.location[target] = _loc
        self.params = []

    def _build_elem(self, ctype, source, index, target):
        """
            The method that builds an element

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                index :
                    A.
                target :
                    A.

        """
        var_source = self._get_location(source)
        var_index = self._get_location(index)
        var_base = ir.Constant(var_index.type, 0)
        if isinstance(var_source.type.pointee.element, ir.ArrayType):
            col = var_source.type.pointee.element.count
            if isinstance(var_index, ir.Constant):
                const_i = ir.Constant(int_type, var_index.constant // col)
                _j = ir.Constant(int_type, var_index.constant % col)
            else:
                _col = ir.Constant(int_type, col)
                const_i = self.builder.sdiv(var_index, _col)
                _j = self.builder.srem(var_index, _col)
            _aux = self.builder.gep(var_source, [var_base, const_i])
            _loc = self.builder.gep(_aux, [var_base, _j])
        else:
            _loc = self.builder.gep(var_source, [var_base, var_index])
        self.location[target] = _loc

    def _build_get(self, ctype, source, target):
        """
            The method that builds a get

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                target :
                    A.

        """
        pass

    def _build_get_(self, ctype, source, target, **kwargs):
        """
            The method that builds a get

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                target :
                    A.
                **kwargs :
                    A.

        """
        _source = self._get_location(source)
        _target = self._get_location(target)
        _align = get_align(llvm_type_dict[ctype].as_pointer(), 1)
        self.builder.store(_source, _target, align=_align)

    def _build_literal(self, var_type, cte, target):
        """
            The method that builds a literal

            ...

            Parameters
            ----------
                var_type :
                    A.
                cte :
                    A.
                target :
                    A.

        """
        _val = llvm_type_dict[var_type](cte)
        _loc = self._get_location(target)
        if _loc:
            self.builder.store(_val, _loc)
        else:
            self.location[target] = _val

    def _build_load(self, ctype, source, target):
        """
            The method that builds a store

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                target :
                    A.

        """
        _source = self._get_location(source)
        if isinstance(_source, ir.Constant):
            self.location[target] = _source
        else:
            _align = get_align(llvm_type_dict[ctype], 1)
            _loc = self.builder.load(_source, align=_align)
            self.location[target] = _loc

    def _build_load_(self, ctype, source, target, **kwargs):
        """
            The method that builds a load

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                target :
                    A.
                **kwargs :
                    A.

        """
        _source = self._get_location(source)
        _type = llvm_type_dict[ctype]
        _pointee = _source.type.pointee
        if isinstance(_pointee, ir.PointerType):
            if isinstance(_pointee.pointee, ir.FunctionType):
                _loc = self.builder.load(_source, align=8)
            else:
                _type = llvm_type_dict[ctype].as_pointer()
                _align = get_align(_type, 1)
                _aux = self.builder.load(_source, align=_align)
                _type = llvm_type_dict[ctype]
                _align = get_align(_type, 1)
                _loc = self.builder.load(_aux, align=_align)
        else:
            _align = get_align(_type, 1)
            _loc = self.builder.load(_source, align=8)
        self.location[target] = _loc

    def _build_param(self, par_type, source):
        """
            The method that builds a parameter

            ...

            Parameters
            ----------
                par_type :
                    A.
                source :
                    A.

        """
        self.params.append(self._get_location(source))

    def _build_print(self, val_type, target):
        """
            The method that builds a print

            ...

            Parameters
            ----------
                val_type :
                    A.
                target :
                    A.

        """
        if target:
            value_to_print = self._get_location(target)
            if val_type == 'int':
                self._cio('printf', '%d', value_to_print)
            elif val_type == 'float':
                self._cio('printf', '%f', value_to_print)
            elif val_type == 'char':
                self._cio('printf', '%c', value_to_print)
            elif val_type == 'string':
                self._cio('printf', '%s', value_to_print)
        else:
            self._cio('printf', '\n')

    def _build_read(self, var_type, target):
        """
            The method that builds a read

            ...

            Parameters
            ----------
                var_type :
                    A.
                target :
                    A.

        """
        read_target = self._get_location(target)
        if var_type == 'int':
            self._cio('scanf', '%d', read_target)
        elif var_type == 'float':
            self._cio('scanf', '%lf', read_target)
        elif var_type == 'char':
            self._cio('scanf', '%c', read_target)

    def _build_read_(self, ctype, target, **kwargs):
        """
            The method that builds a read

            ...

            Parameters
            ----------
                ctype :
                    A.
                target :
                    A.
                **kwargs :
                    A.

        """
        self._build_read_(ctype, target) #Isso faz sentido?

    def _build_store(self, ctype, source, target):
        """
            The method that builds a store

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                target :
                    A.

        """
        _source = self._get_location(source)
        _target = self._get_location(target)
        if _target:
            _align = get_align(llvm_type_dict[ctype], 1)
            self.builder.store(_source, _target, _align)
        else:
            self.location[target] = _source

    def _build_store_(self, ctype, source, target, **kwargs):
        """
            The method that builds a store

            ...

            Parameters
            ----------
                ctype :
                    A.
                source :
                    A.
                target :
                    A.
                **kwargs :
                    A.

        """
        var_source = self._get_location(source)
        var_target = self._get_location(target)

        if isinstance(var_target.type.pointee, ir.ArrayType):
            var_size = 1
            for arg in kwargs.values():
                var_size *= int(arg)
            if ctype == 'float':
                var_size = var_size * 8
            elif ctype == 'int':
                var_size = var_size * int_type.width // 8
            memcpy = self.module.declare_intrinsic('llvm.memcpy', [charptr_ty, charptr_ty, i64_type])
            _srcptr = self.builder.bitcast(var_source, charptr_ty)
            _tgtptr = self.builder.bitcast(var_target, charptr_ty)
            self.builder.call(memcpy, [_tgtptr, _srcptr, ir.Constant(i64_type, var_size), llvm_false])
        elif isinstance(var_target.type.pointee, ir.PointerType):
            _align = get_align(ir.PointerType, 1)
            _temp = self.builder.load(var_target, align=_align)
            self.builder.store(var_source, _temp, _align)
        else:
            _align = get_align(llvm_type_dict[ctype], 1)
            self.builder.store(var_source, var_target, _align)

    def _build_add(self, expr_type, left, right, target):
        """
            The method that builds a sum

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fadd(_left, _right)
        else:
            _loc = self.builder.add(_left, _right)
        self.location[target] = _loc

    def _build_sub(self, expr_type, left, right, target):
        """
            The method that builds a subtraction

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fsub(_left, _right)
        else:
            _loc = self.builder.sub(_left, _right)
        self.location[target] = _loc

    def _build_mul(self, expr_type, left, right, target):
        """
            The method that builds a multiplication

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fmul(_left, _right)
        else:
            _loc = self.builder.mul(_left, _right)
        self.location[target] = _loc

    def _build_div(self, expr_type, left, right, target):
        """
            The method that builds a division

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fdiv(_left, _right)
        else:
            _loc = self.builder.sdiv(_left, _right)
        self.location[target] = _loc

    def _build_mod(self, expr_type, left, right, target):
        """
            The method that builds a mod

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.frem(_left, _right)
        else:
            _loc = self.builder.srem(_left, _right)
        self.location[target] = _loc

    def _build_and(self, expr_type, left, right, target):
        left_loc = self._get_location(left)
        right_loc = self._get_location(right)
        target_loc = self.builder.and_(left_loc, right_loc)

        self.location[target] = target_loc

    def _build_or(self, expr_type, left, right, target):
        left_loc = self._get_location(left)
        right_loc = self._get_location(right)
        target_loc = self.builder.or_(left_loc, right_loc)

        self.location[target] = target_loc

    def _build_ge(self, expr_type, left, right, target):
        """
            The method that builds a greather or equal than

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fcmp_ordered('>=', _left, _right)
        else:
            _loc = self.builder.icmp_signed('>=', _left, _right)
        self.location[target] = _loc

    def _build_le(self, expr_type, left, right, target):
        """
            The method that builds a less or equal than

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fcmp_ordered('<=', _left, _right)
        else:
            _loc = self.builder.icmp_signed('<=', _left, _right)
        self.location[target] = _loc

    def _build_gt(self, expr_type, left, right, target):
        """
            The method that builds a greater than

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fcmp_ordered('>', _left, _right)
        else:
            _loc = self.builder.icmp_signed('>', _left, _right)
        self.location[target] = _loc

    def _build_lt(self, expr_type, left, right, target):
        """
            The method that builds a less than

            ...

            Parameters
            ----------
                expr_type :
                    A.
                left :
                    A.
                right :
                    A.
                target :
                    A.

        """
        _left = self._get_location(left)
        _right = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fcmp_ordered('<', _left, _right)
        else:
            _loc = self.builder.icmp_signed('<', _left, _right)
        self.location[target] = _loc

    def _build_eq(self, expr_type, left, right, target):
        left_loc = self._get_location(left)
        right_loc = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fcmp_ordered('==', left_loc, right_loc)
        else:
            _loc = self.builder.icmp_signed('==', left_loc, right_loc)
        self.location[target] = _loc

    def _build_ne(self, expr_type, left, right, target):
        left_loc = self._get_location(left)
        right_loc = self._get_location(right)
        if expr_type == 'float':
            _loc = self.builder.fcmp_ordered('!=', left_loc, right_loc)
        elif expr_type == 'char': # or expr_type == 'string':
            _loc = self.builder.fcmp_ordered('!=', left_loc, right_loc)
        else:
            _loc = self.builder.icmp_signed('!=', left_loc, right_loc)
        self.location[target] = _loc

    def _build_sitofp(self, expr_type, source, target):
        source_loc = self._get_location(source)
        target_loc = self.builder.sitofp(source_loc, float_type)

        self.location[target] = target_loc

    def _build_fptosi(self, expr_type, source, target):
        source_loc = self._get_location(source)
        target_loc = self.builder.fptosi(source_loc, int_type)

        self.location[target] = target_loc

    def _build_return(self, expr_type, target):
        """
            The method that builds a return

            ...

            Parameters
            ----------
                expr_type :
                    A.
                target :
                    A.

        """
        if expr_type == 'void':
            self.builder.ret_void()
        else:
            _target = self._get_location(target)
            self.builder.ret(_target)

    def _build_jump(self, expr_type, target):
        """
            The method that builds a jump

            ...

            Parameters
            ----------
                expr_type :
                    A.
                target :
                    A.

        """
        _target = self._get_location(target)
        self.builder.branch(_target)

    def _build_cbranch(self, expr_type, expr_test, target, fall_through):
        """
            The method that builds a conditional branch

            ...

            Parameters
            ----------
                expr_type :
                    A.
                expr_test :
                    A.
                target :
                    A.
                fall_through :
                    A.

        """
        _expr_test = self._get_location(expr_test)
        _target = self._get_location(target)
        _fall_through = self._get_location(fall_through)
        self.builder.cbranch(_expr_test, _target, _fall_through)

    def build(self, inst):
        """
            A

            ...

            Parameters
            ----------
                inst :
                    A.

        """
        opcode, ctype, modifier = extract_operation(inst[0])
        if hasattr(self, "_build_" + opcode):
            args = inst[1:] if len(inst) > 1 else (None,)
            if not modifier:
                getattr(self, "_build_" + opcode)(ctype, *args)
            else:
                getattr(self, "_build_" + opcode + "_")(ctype, *inst[1:], **modifier)
        else:
            print("Warning: No _build_" + opcode + "() method", flush=True)

    def create_blocks(self, func_blocks_dict):
        for block_label in func_blocks_dict:
            block = func_blocks_dict[block_label]
            if block_label == '%entry':
                self._new_function(block.instructions[1])
            ir_block_loc = self.functions.append_basic_block(block_label)
            self.location[block.label] = ir_block_loc

    def build_blocks(self, func_blocks_dict):
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

    def compile_ir(self):
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
        mod = self.compile_ir()

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
            fn_sig = isinstance(var_value, list)

            if fn_sig:
                for _el in var_value:
                    if _el not in list(llvm_type_dict.keys()):
                        fn_sig = False
            if uc_type in ['string']:
                ir_constant = create_byte_array((var_value + "\00").encode('utf-8'))
                ir_global_var = ir.GlobalVariable(self.module, ir_constant.type, var_name)
                ir_global_var.initializer = ir_constant
                ir_global_var.align = 1
                ir_global_var.global_constant = True
            elif modifier and not fn_sig:
                _width = 1
                for arg in reversed(list(modifier.values())):
                    _width = int(arg)
                    llvm_type = ir.ArrayType(llvm_type, int(arg))

                ir_global_var = ir.GlobalVariable(self.module, llvm_type, var_name)
                ir_global_var.initializer = ir.Constant(llvm_type, var_value)
                ir_global_var.align = get_align(llvm_type, _width)
                if var_name.startswith('.const'):
                    ir_global_var.global_constant = True
            elif fn_sig:
                # ptr to function
                _sig = [llvm_type_dict[arg] for arg in var_value]
                ir_func_type = ir.FunctionType(llvm_type_dict[uc_type], _sig)
            else:
                # normal global var like int x = 2
                ir_global_var = ir.GlobalVariable(self.module, llvm_type, var_name)
                ir_global_var.align = get_align(llvm_type, 1)
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
            llvm_block = LLVMFunctionVisitor(self.module)
            llvm_block.create_blocks(func_dict)
            llvm_block.build_blocks(func_dict)

        # for _decl in node.gdecls:
        #     if isinstance(_decl, FuncDef):
        #         bb = LLVMFunctionVisitor(self.module)
        #         bb.phase = 'create_bb'
        #         bb.visit(_decl.cfg)
        #         bb.phase = 'build_bb'
        #         bb.visit(_decl.cfg)
