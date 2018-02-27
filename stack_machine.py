from ast import literal_eval
from copy import copy

from contracts import contract
from contracts import new_contract
from functools import reduce

__author__ = 'Arin'
import sys
import re

STACK = "stack"
ENV = "environment"
CONTROL = "contr"
DUMP = "dump"

NON_TERM = "NT"
TERM_INT = "INT"
TERM_CHAR = "CHAR"
TERM_INS = "INS"
NIL = "NIL"

ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"
MOD = "MOD"

DEFUN = "DEFUN"
DEF = "DEF"
WRITE = "WRITE"
READI = "READI"

LDC = "LDC"
LD = "LD"

APP = "APP"
LDF = "LDF"

IF = "IF"
AND = "AND"
OR = "OR"
NOT = "NOT"

EQUAL = "EQUAL"
LT = "LT"
GT = "GT"

CONS = "CONS"
CAR = "CAR"
CDR = "CDR"
STRING = "STRING"

INSTRUCTIONS = [
    ADD, #pops one from stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    SUB, #pops one from stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    MUL, #pops one from stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    DIV, #pops one from stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    MOD, #pops one from stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    DEF, #pops one from the stack(env) => pops one from the stack(val) => pushes one to specified environment
    LD, #pops one from the control => pushes one to stack
    LDC, #pops one from control => pushes one to the stack
    DEFUN, #pops one from stack => pops one from control => pushes one to specified environment
    APP, #pops one from the control(pos in env) => pops one from the stack(amount of params) => pops the specified amount from the stack
        # => push func result on stack
    IF, #pops on from the stack(amount of control params) => pops one from the stack(val) => pops specified amount from control
        # => push unspecified amount to control
    AND, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    OR, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    NOT, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes the specified amount to the stack
    EQUAL, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    LT, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    GT, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    CONS, #pops one from the stack(amount of params) => pops the specified amount from the stack => pushes one to stack
    CAR, #pops one from the stack => pushes one to the stack
    CDR, #pops one from the stack => pushes one to the stack
    WRITE, #pops one from the stack
    READI, #pushes one to the stack
    STRING, #pops one from control => pushes one to the stack
]


def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_str(val):
    return isinstance(val, str)


def is_list(val):
    return isinstance(val, list)


def is_nil(val):
    return val == "nil"


def is_instr(val):
    return val in INSTRUCTIONS

class SECD:

    new_contract("STACK_not_empty", lambda secd: len(secd._stacks[STACK]) > 0)
    new_contract("ENV_not_empty", lambda secd: len(secd._stacks[ENV]) > 0)
    def __init__(self):
        self._memory_size = 2000
        self._last_filled_cell = 0
        self.out = sys.stdout
        self.input = sys.stdin

        #first location is for nil
        self._memory = [NIL, None] + [None] * self._memory_size
        self._stacks = { STACK: [],
                         ENV: [],
                         CONTROL: [],
                         DUMP: [] }

        self.inst_mapping = {
            ADD: self._add,
            SUB: self._sub,
            MUL: self._mul,
            DIV: self._div,
            MOD: self._mod,
            DEF: self._define,
            LDC: self._ldc,
            LD: self._ld,
            DEFUN: self._defun,
            APP: self._app,
            AND: self._and,
            OR: self._or,
            NOT: self._not,
            IF: self._if,
            EQUAL: self._equal,
            LT: self._lt,
            GT: self._gt,
            CONS: self._cons,
            CAR: self._car,
            CDR: self._cdr,
            WRITE: self._write,
            READI: self._readi,
            STRING: self._string,
        }

    def print_stacks(self):
        print(STACK + " => " + str(self._stacks[STACK]))
        print(ENV + " => " + str(self._stacks[ENV]))
        print(CONTROL + " => " + str(self._stacks[CONTROL]))
        print(DUMP + " => " + str(self._stacks[DUMP]))

    def print_stack(self, stack_name):
        print(stack_name + " => " + str(self._stacks[stack_name]))

    def print_memory(self):
        print("Memory:")
        for i in range(self._last_filled_cell + 1):
            print("Cell => " + str(i) + " value => " + str(self._memory[i]))

    def _get_free_address(self):
        """
        Gets the next free address in the memory of the machine
        :return: Free memory address
        """
        self._last_filled_cell += 1
        assert self._last_filled_cell <= self._memory_size, "SECD machine has run out of memory"
        return self._last_filled_cell

    def _add_cell_to_memory(self, cell):
        """
        A function for adding created cell to the memory. If you want to create cell and add it use _add_cell function
        :param cell: Well shaped terminal cell
        :return: Address of the cell
        """
        #try to find a terminal which already holds our values
        #we can do that since terminals are immutable
        for address in range(1, self._last_filled_cell + 1):
            memory_cell = self._memory[address]
            if self._cell_equal(memory_cell, cell):
                return address

        #otherwise we have to add this cell after the current last one
        address = self._get_free_address()

        #now we can fill the cell with our terminal
        self._memory[address] = cell
        return address

    def _cell_equal(self, f_cell, s_cell):
        """
        Compares two well formed cells
        :param f_cell: First provided cell
        :param s_cell: Second provided cell
        :return: True if the cells are identical, False otherwise
        """
        return len(f_cell) == len(s_cell) and all(f_cell[x] == s_cell[x] for x in range(len(f_cell)))

    def _add_cell(self, tag, value):
        """
        Function for adding all new cells to the memory. This function is a preffered way of doing it as it supports all types of cells.
        :param tag: Type tag of the cell to add.
        :param value: Value of the cell to add. This should be an integer if the cell in TERM_INT and an instruction string if TERM_INS.
                    A python list [car,cdr] if it is a NON_TERM - car should be an address of the value of the current list el,
                    cdr should be an address of the nex el (or address of nil if it is the last el)
        :return: Address of newly added cell
        """
        if tag == NIL:
            return 0 #this is the nil cell address
        elif tag != NON_TERM:
            cell = self._create_terminal_cell(tag, value)
            return self._add_cell_to_memory(cell)
        else:
            cell = self._create_non_terminal_cell(value)
            return self._add_cell_to_memory(cell)

    def _get_int_cell_val(self, address):
        """
        Gets the integer value stored at provided address. (works also for bools since they are stored as ints)
        :param address: Address of the cell to retrieve value from
        :return: The value of the cell
        """
        assert address <= self._last_filled_cell, "Trying to access unallocated memory at address {0}".format(address)
        assert self._memory[address][0] == TERM_INT, "Trying to get int value from non-int cell at address {0}".format(address)
        return self._memory[address][1]

    def _get_cell_val(self, address):
        """
        Gets value of the cell stored at provided address.
        IMPORTANT! It is preffered to use this method only if you are unsure what type of cell value you wish to retrieve.
        In other cases use more specialised methods like _get_int_cell_val
        :param address: Address of the cell to retrieve value from
        :return: The value of the cell
        """
        assert address <= self._last_filled_cell, "Trying to access unallocated memory at address {0}".format(address)
        return self._memory[address][1]

    def _is_terminal_cell(self, cell):
        #later add here other types
        return cell[0] == TERM_INT or cell[0] == TERM_CHAR or cell[0] == TERM_INS

    def is_string_list(self, head_cell):
        if head_cell[0] != NON_TERM:
            return False
        value_cell = self._memory[head_cell[1]]
        return value_cell != self._memory[0] and value_cell[0] == TERM_CHAR

    def _create_terminal_cell(self, tag, value):
        """
        Creates a terminal cell out of provided value. Created cell is NOT added to the memory
        :param tag: Type tag of the new cell. Only terminal tags are accepted
        :param value: Values to add
        :return: The newly created cell
        """
        assert tag != NON_TERM, "The tag specified is incorrect! Cannot add terminal cell"
        return [tag, value]

    def _create_non_terminal_cell(self, value):
        """
        Creates non-terminal cell out of provided value. Created cell is NOT added to the memory
        :param value: Values to add provided as pylist in a form of [car, cdr]
        :return: The newly created cell
        """
        car = value[0]
        cdr = value[1]
        return [NON_TERM, car, cdr]

    def pop(self, stack_name):
        assert len(self._stacks[stack_name]) > 0, "The stack {0} is empty! Cannot pop.".format(stack_name)
        return self._stacks[stack_name].pop()

    def push(self, stack_name, address):
        self._stacks[stack_name].append(address)

    def _pop_amount(self, stack_name, amount):
        """
        Pops certain amount of values from the stack.
        :param stack_name: The name of the stack from which to pop
        :param amount: The amount of values to pop
        :return: List of all popped values in the order at which they were lying on the stack(not the popping order)
        """
        assert len(self._stacks[stack_name]) >= amount, "Not enough elements on the " + stack_name
        end_list = list(reversed([self.pop(stack_name) for x in range(amount)]))
#        print("Pop list => " + str(end_list))
        return end_list

    def _pop_typed_amount(self, type_tag, amount):
        """
        Convinience method for popping particular amount from the STACK. The cells popped will be processed according to provided type.
        :param type_tag: Tag of the type of the cells
        :param amount: Amount of cells to pop
        :return: Values of popped cells
        """
        assert len(self._stacks[STACK]) >= amount, ("Not enough elements on the " + STACK)
        if type_tag == TERM_INT:
            return list(reversed([self._pop_int_val() for x in range(amount)]))
        elif type_tag == NON_TERM:
            #add support for non terms
            #nah, this can be achieved through pop_auto_typed_amount but maybe one day, when I have time...
            pass


    def _pop_auto_typed_amount(self, amount):
        """
        Convenience method for popping particular amount from the STACK. The cells popped will be processed according to their type.
        :param amount: Amount of cells to pop
        :return: Values of popped cells
        """
        assert len(self._stacks[STACK]) >= amount, "Not enough elements on the {0}".format(STACK)
        return list(reversed([self._pop_typed_val() for x in range(amount)]))

    def _push_val(self, value):
        """
        A convenience function. Adds provided value to the memory and pushes it onto stack
        :param value: A value
        """
        address = self._add_typed_cell(value)
        self.push(STACK, address)

    def _add_typed_cell(self, value):
        tag = self._get_type_tag(value)
        if tag != NON_TERM:
            return self._add_cell(tag, value)
        else:
            return self._add_list(value)

    def _car(self):
        address = self.pop(STACK)
        assert self._memory[address][0] == NON_TERM, "The cell is a terminal cell. The car instruction does not apply."
        self.push(STACK, self._memory[address][1])

    def _cdr(self):
        address = self.pop(STACK)
        assert self._memory[address][0] == NON_TERM, "The cell is a terminal cell. The cdr instruction does not apply."
        self.push(STACK, self._memory[address][2])

    def _write(self):
        cell = self._memory[self.pop(STACK)]
        tag = cell[0]
        value = cell[1]

        if tag != NON_TERM:
            self._writei(value)
        else:
            val_cell = self._memory[value]
            if val_cell[0] == TERM_CHAR:
                self._writes(cell)
            else:
                self._writel(cell)

    def _writes(self, head_cell):
        end_string = self._extract_string(head_cell)
        self.out.write(end_string + "\n")

    def _extract_string(self, head_cell):
        end_string = ""
        current_cell = head_cell

        while current_cell != self._memory[0]:
            end_string += self._get_cell_val(current_cell[1])
            current_cell = self._memory[current_cell[2]]
        return end_string

    def _writei(self, value):
        self.out.write(str(value) + "\n")

    def _writel(self, head_cell):
        """
        Prints a list
        :param head_cell: The first cell of the list
        """
        end_string = self._create_l_string(head_cell)
        self.out.write("{0} \n".format(end_string))

    def _create_l_string(self, cell):
        string = ""
        current_cell = cell

        while current_cell != self._memory[0]:
            print ("current cell => {0}".format(current_cell))
            val_cell = self._memory[current_cell[1]]
            if val_cell[0] == NON_TERM:
                string += self._create_l_string(val_cell)
            elif val_cell == NIL:
                string += val_cell
            else:
                print ("val cell => {0}".format(val_cell))
                string += "{0} ".format(val_cell[1])
            current_cell = self._memory[current_cell[2]]
        string = string[:-1] if string[-1] == " " else string
        string = "({0}) ".format(string)
        return string

    def _readi(self):
        read_data = input()
        assert is_int(read_data), "Not integer data provided!"
        self._push_val(int(read_data))

    def _add(self):
        self._math_op(lambda x, y: x + y)

    def _sub(self):
        self._math_op(lambda x, y: x - y)

    def _mul(self):
        self._math_op(lambda x, y: x * y)

    def _div(self):
        self._math_op(lambda x, y: x / y)

    def _mod(self):
        self._math_op(lambda x, y: x % y)

    def _math_op(self, math_function):
        """
        Function for generic handling of the mathematical operations.
        :param math_function: Mathematical function that is to be applied.
                The function has to take as argument two int values and return and int.
        """
        amount = self._pop_int_val()
        values = self._pop_typed_amount(TERM_INT, amount)
        self._push_val(reduce(math_function, values))

    def _if(self):
        contr_amount = self._pop_int_val()
        bool_val = self._pop_int_val()
        then = reversed(self.pop(CONTROL))
        then_else = [] if contr_amount == 1 else reversed(self.pop(CONTROL))
        self._stacks[CONTROL] += then if bool_val == 1 else then_else

    def _equal(self):
        self._log_exp(lambda values: all(values[0] == values[i] for i in range(1, len(values))))

    def _lt(self):
        self._log_exp(lambda values: all(values[0] < values[i] for i in range(1, len(values))))

    def _gt(self):
        self._log_exp(lambda values: all(values[0] > values[i] for i in range(1, len(values))))

    def _and(self):
        self._log_exp(lambda values: all(val != 0 for val in values))

    def _or(self):
        self._log_exp(lambda values: any(val != 0 for val in values))

    def _not(self):
        self._log_exp(lambda values: values[0] == 0)

    def _log_exp(self, log_func):
        """
        Function used for generic handling of logical operations
        :param result_method: Funtion used for this particular logical operation.
                Needs to take a list of values and return a bool.
        """
        amount = self._pop_int_val()
        values = self._pop_auto_typed_amount(amount)
        result = 1 if log_func(values) else 0
        self._push_val(result)

    def _cons(self):
        """
        Constructs a list out of desired elements.
        """
        amount = self._pop_int_val()
        cell_address = self._pop_amount(STACK, amount)
        cells = [self._memory[address] for address in cell_address]

        if all(self.is_string_list(cell) for cell in cells):
            head = self._cons_string(cells)
        else:
            head = self._combine_into_list(cell_address)
        self.push(STACK, head)
#        self.print_memory()

    def _cons_string(self, combination_cells):
        string = ""
        for cell in combination_cells:
            string += self._extract_string(cell)
        return self._add_char_list(string)

    def _string(self):
        """
        Constructs a list of characters out of provided string.
        """
        string = self.pop(CONTROL)
        assert is_str(string), "Value {0} is not a string. Cannot create a char list.".format(string)
        head = self._add_char_list(string)
        self.push(STACK, head)

    def _combine_into_list(self, cell_addresses):
        """
        Combines provided cell addresses into a list object
        :param cell_addresses: Addresses of the cells to put into the list, provided in a desired order
        :return: address of the first cell of the list
        """
        address = 0
        cdr = 0
        for cell_address in reversed(cell_addresses):
            car = cell_address
            address = self._add_cell(NON_TERM, [car, cdr])
            cdr = address
        return address


    def _add_char_list(self, string):
        assert is_str(string), "Not a string, cannot add"
        address = 0
        cdr = 0 #points to nil
        if string == "":
            car = self._add_cell(TERM_CHAR, "")
            address = self._add_cell(NON_TERM, [car, cdr])
            cdr = address

        for char in reversed(string):
            car = self._add_cell(TERM_CHAR, char)
            address = self._add_cell(NON_TERM, [car, cdr])
            cdr = address
        return address



    def _define(self):
        """
        Defines a variable and adds its value to the specified environment.
        :return:
        """
        env_pos = self._pop_int_val()
        value = self.pop(STACK)
        self._add_to_env(value, env_pos)

    def _defun(self):
        """
        Puts function body in the environment, so it can later be called.
        :return:
        """
        env_num = self._pop_int_val()
        code = self.pop(CONTROL)
        self._add_to_env(code, env_num)
        assert code[0] <= len(self._stacks[ENV]), "The environment is not insertable"
        self._stacks[ENV].append([])

    def _app(self):
        """
        Applies the function from the environment to the provided parameters.
        This function requiers at least one parameter to be placed on the STACK before it is called,
        as well as one value be present on the CONTROL after APP
        First a value describing amount of parameters is popped from the STACK
        Then we pop a provided amount of parameters, and apply them to the function.
        :return:
        """
#        self.print_stacks()
        env_pos = self.pop(CONTROL)
        amount = self._pop_int_val()
#        print("env_pos => " + str(env_pos))
#        self.print_stacks()
#        print("first env => " + str(self._stacks[ENV][0]))
        control = self._stacks[ENV][env_pos[0]][env_pos[1]]
        var_addresses = self._pop_amount(STACK, amount)
        self._dump(var_addresses, list(reversed(control[1:])), control[0])
#        self.print_stacks()

    def _dump(self, params, control, new_env_num):
        """
        Dumps STACK, ENV and CONTROL onto the DUMP.
        :param params: Parameters that are to be put into new environment
        :param control: The code to put into new CONTROL
        :param new_env_num: Number of the new environment.
        This value must be an integer smaller the size of environment stack.
        :return:
        """
#        self.print_stacks()
        dump = [self._stacks[STACK], copy(self._stacks[ENV]), self._stacks[CONTROL]]
        self._stacks[STACK] = []
        self._stacks[CONTROL] = control
        self._stacks[DUMP].append(dump)
        self._reinit_env(new_env_num, params)

    def _restore_stacks(self):
        """
        Restores STACK, ENV and CONTROL from the DUMP.
        There has to be at least one object on the DUMP
        """
        dump = self.pop(DUMP)
        self._stacks[STACK] = dump[0] + self._stacks[STACK]
        self._stacks[ENV] = dump[1]
        self._stacks[CONTROL] = dump[2]
#        self.print_stacks()

    def _reinit_env(self, env_num, params):
        """
        Reinitializes desired environment with new parameters
        :param env_num: The position of the environment
        This value must be an integer smaller the size of environment stack.
        :param params: Parameters to put into environment
        Parameters must be provided as a list
        """
        assert len(self._stacks[ENV]) > env_num, "The environment doesn't exist. Reinitialisation failed!"

        self._stacks[ENV][env_num] = []
        for param in params:
           self._stacks[ENV][env_num].append(param)

    def _add_to_env(self, value, env_num):
        """
        Adds provided value to the environment at the provided position.
        The value is stored as is, which means it will not be pushed into memory.
        The value is pushed into the end of that environment.
        :param value: The value to add to environment
        :param env_num: The position of the environment.
        This value must be an integer smaller or equal the size of environment stack.
        """
#        print("Adding to env => " + str(env_num))
        env_len = len(self._stacks[ENV])
        assert env_len >= env_num, "Undefined position in environment stack"
        if env_len == env_num:
            self._stacks[ENV].append([value])
        else:
            self._stacks[ENV][env_num].append(value)

    def _ldc(self):
        """
        Loads constant onto the stack. Requires the CONTROL stack to hold one value after LDC.
        """
        value = self.pop(CONTROL)
        self._push_val(value)  # adds value to memory and pushes it's address to STACK
#        self.print_memory()

    def _ld(self):
        """
        Loads a variable onto the stack. Requires the CONTROL stack to hold one env index after LD.
        """
        env_pos = self.pop(CONTROL)
        assert is_list(env_pos), "Position in environment was not provided. Unable to load variable"
        self.push(STACK, self.get_env_val(env_pos)) #Load address of memory cell from ENV and push it to STACK
#        self.print_stack(STACK)

    def get_env_val(self, env_pos):
        """
        Finds cell at specified position in the environment
        :param env_pos: Position in the environment stack provided as a two element python list.
        The first el is the index of the environment and the second is the position in that environment.
        :return: The value that was stored in environment at provided position
        (exactly as it was stored, so if it was an address, this function will return an address)
        """
        return self._stacks[ENV][env_pos[0]][env_pos[1]]

    def _get_type_tag(self, value):
        """
        Checks the type of the provided value and provides info on that.
        :param value: Value to check
        :return: The tag that corresponds to the value
        """
        if is_int(value):
            return TERM_INT
        elif is_instr(value):
            return TERM_INS
        elif value == NIL:
            return NIL
        elif is_str(value):
            return
        elif is_list(value):
            return NON_TERM

    def _pop_int_val(self):
        """
        Convienience function for popping the STACK and getting the value of the popped cell
        :return: Value of the popped cell
        """
        address = self.pop(STACK)
        return self._get_int_cell_val(address)

    def _pop_typed_val(self):
        """
        Convienience function for popping the STACK and getting the value of the popped cell. The type of cell is determined autimatically
        IMPORTANT! Use this function only if multiple types are allowed in the operation you are performing.
        Otherwise use a strongly typed version of this function like _pop_int_val
        :return: Value of the popped cell
        """
        address = self.pop(STACK)
        return self._get_cell_val(address)

    def _can_execute(self):
        """
        Checks whether the stack machine should continue executing
        :return: True if CONTROL or DUMP are not empty, false otherwise
        """
        return len(self._stacks[CONTROL]) > 0 or len(self._stacks[DUMP]) > 0

    def exec_instr(self):
        """
        Executes top instruction on the CONTROL stack.
        """
        assert len(self._stacks[CONTROL]) > 0, "No instructions on the stack! Cannot execute"
        instr = self._stacks[CONTROL].pop()
        assert is_instr(instr), "Not an instruction! Cannot execute " + str(instr)

#        print("Executing instruction: " + instr)
        self.inst_mapping[instr]()

    def run_program(self, program):
        """
        Executes provided program.
        :param program: Well formed correctly parsed Specialization project program, provided as a pylist.
        """
#        print("Running")
#        print("Program => " + str(program))
        for i in reversed(program):
            self.push(CONTROL, i)
        while self._can_execute():
            if len(self._stacks[CONTROL]) == 0:
                self._restore_stacks()
                continue
            self.exec_instr()
#        self.print_stacks()
#        self.print_memory()

    def run_program_for_result(self, program):
        """
        Executes provided program.
        :param program: Well formed correctly parsed Specialization project program, provided as a pylist.
        :return Top memory cell of the main stack. This is the result of the program.
        """
        self.run_program(program)
        return self._memory[self.pop(STACK)]



