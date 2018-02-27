from stack_machine import LDC, ADD, SUB, DIV, MUL, DEF, LD, DEFUN, APP, IF, AND, OR, NOT, EQUAL, LT, \
    GT, \
    CONS, CAR, CDR, MOD, NIL, WRITE, READI, STRING

__author__ = 'Arin'
import ply.lex as lex
import ply.yacc as yacc

DECLARE = "declare"

tokens = ("LPAREN", "RPAREN", "NIL", "NUM", "IF", "PLUS", "MINUS", "DIVIDE", "MOD", "MULTIPLY",
          "DEFINE", "READ", "PRINT", "STRING", "CONS", "EQUAL", "LT", "GT",
          "TRUE", "FALSE", "IDENTIFIER", "AND", "OR", "NOT", "CAR", "CDR")

t_ignore = ' \t\v\r'


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_DEFINE(t):
    r'define'
    return t


def t_NIL(t):
    r'nil'
    t.value = NIL
    return t


def t_IF(t):
    r'if'
    return t


def t_EQUAL(t):
    r'='
    t.value = EQUAL
    return t


def t_LT(t):
    r'\<'
    t.value = LT
    return t


def t_GT(t):
    r'\>'
    t.value = GT
    return t


def t_AND(t):
    r'and'
    t.value = AND
    return t


def t_CONS(t):
    r'\bcons\b'
    t.value = CONS
    return t


def t_CAR(t):
    r'\bcar\b'
    t.value = CAR
    return t


def t_CDR(t):
    r'\bcdr\b'
    t.value = CDR
    return t


def t_OR(t):
    r'\bor\b'
    t.value = OR
    return t


def t_NOT(t):
    r'\bnot\b'
    t.value = NOT
    return t


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_PLUS(t):
    r'\+'
    t.value = ADD
    return t


def t_MINUS(t):
    r'\-'
    t.value = SUB
    return t


def t_DIVIDE(t):
    r'\/'
    t.value = DIV
    return t


def t_MOD(t):
    r'\%'
    t.value = MOD
    return t


def t_MULTIPLY(t):
    r'\*'
    t.value = MUL
    return t


def t_TRUE(t):
    r'\btrue\b'
    t.value = True
    return t


def t_FALSE(t):
    r'\bfalse\b'
    t.value = False
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1: -1]
    return t


def t_PRINT(t):
    r'\bprint\b'
    t.value = WRITE
    return t


def t_READ(t):
    r'\bread\b'
    t.value = READI
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    pass


def t_error(t):
    pass


def p_program(p):
    "program : exp"
    p[0] = ("program",) + p[1]


def p_exp(p):
    '''exp : definition
            | value_exp
            | if_stmt
            | log_exp
            | print_exp'''
    p[0] = (p[1],)


def p_exp_exp(p):
    "exp : exp exp"
    p[0] = p[1] + p[2]


def p_print_exp(p):
    """print_exp : LPAREN PRINT exp RPAREN"""
    p[0] = p[2], p[3]


def p_read_exp(p):
    """read_exp : READ"""
    p[0] = p[1]


def p_number(p):
    "number : NUM"
    p[0] = "number", p[1]


def p_log_val(p):
    """log_val : TRUE
                | FALSE"""
    p[0] = p[1]


def p_identifier(p):
    "identifier : IDENTIFIER"
    p[0] = "identifier", p[1]


def p_definition(p):
    "definition : LPAREN DEFINE identifier value_exp RPAREN"
    p[0] = (DEF, p[3]) + (p[4],)


def p_defun(p):
    "definition : LPAREN DEFINE identifier LPAREN arguments RPAREN LPAREN exp RPAREN RPAREN"
    p[0] = (DEFUN, p[3], ("arguments", p[5])) + (p[8],)


def p_arguments(p):
    "arguments : declaration arguments"
    p[0] = (p[1],) + p[2]


def p_empty_arguments(p):
    "arguments : "
    p[0] = tuple()


def p_declaration(p):
    "declaration : identifier"
    p[0] = DECLARE, p[1]


def p_if_stmt(p):
    """if_stmt : LPAREN IF log_exp LPAREN exp RPAREN RPAREN"""
    p[0] = IF, p[3], p[5]


def p_if_else_stmt(p):
    """if_stmt : LPAREN IF log_exp LPAREN exp RPAREN LPAREN exp RPAREN RPAREN"""
    p[0] = IF, p[3], p[5], p[8]


def p_log_expression(p):
    """log_exp : value
                | value_exp"""
    p[0] = p[1]


def p_log_expression_op(p):
    """log_exp : LPAREN log_operator log_exp log_args RPAREN"""
    values = (p[3],) + p[4]
    p[0] = ("log_exp", (p[2] + (len(values),))) + values


def p_log_args(p):
    """log_args : log_exp log_args"""
    p[0] = (p[1],) + p[2]


def p_log_arg(p):
    """log_args : log_exp"""
    p[0] = (p[1],)


def p_opt_log_args(p):
    """log_args :"""
    p[0] = tuple()


def p_log_operator(p):
    """log_operator : AND
                    | OR
                    | NOT
                    | EQUAL
                    | GT
                    | LT"""
    p[0] = "log_operator", p[1]


def p_value_exp(p):
    "value_exp : LPAREN operator value_exp args RPAREN"
    values = (p[3],) + p[4]
    p[0] = ("val_exp", (p[2] + (len(values),))) + values


def p_value_exp_func(p):
    """value_exp : func_exp"""
    p[0] = p[1]


def p_func_exp(p):
    """func_exp : LPAREN function args RPAREN"""
    p[0] = (APP, (p[2] + (len(p[3]),)),) + p[3]


def p_function(p):
    "function : identifier"
    p[0] = "function", p[1]


def p_args(p):
    "args : value_exp args"
    p[0] = (p[1],) + p[2]


def p_arg(p):
    "args : value_exp"
    p[0] = (p[1],)


def p_opt_args(p):
    "args : "
    p[0] = tuple()


def p_val_exp(p):
    "value_exp : value"
    p[0] = p[1]


def p_value(p):
    '''value : identifier
            | NIL
            | number
            | log_val
            | list
            | list_car
            | read_exp
    '''
    p[0] = p[1]


def p_car(p):
    """list_car : LPAREN CAR identifier RPAREN
                | LPAREN CAR list RPAREN
                | LPAREN CAR list_car RPAREN"""
    p[0] = p[2], p[3]


def p_cdr(p):
    """list : LPAREN CDR identifier RPAREN
            | LPAREN CDR list RPAREN"""
    p[0] = p[2], p[3]


def p_cons_list(p):
    """list : LPAREN CONS args RPAREN"""
    p[0] = (p[2], len(p[3])) + p[3]


def p_string(p):
    """list : STRING"""
    p[0] = STRING, p[1]


def p_operator(p):
    '''operator : PLUS
                | MINUS
                | DIVIDE
                | MULTIPLY
                | MOD'''
    p[0] = "operator", p[1]


def p_error(p):
    print("Incorrect symbol %s" % p)
    pass


start = "program"
lexer = lex.lex()

parser = yacc.yacc()


def parse(input_string):
    lexer.input(input_string)
    parse_tree = parser.parse(input_string, lexer=lexer)
    return parse_tree


def evaluate(tree, envs, cur_env):
    """
    Evaluates the whole parse tree
    :param tree: Tree to evaluate
    :param envs: All environments that were created during evaluation
    :param cur_env: The environment currently considered
    :return: Parsed tree represented as a pylist of instructions
    """
    #    print(tree)
    result = []
    if tree is None:
        pass
    elif type(tree) == int or tree == NIL:
        result = [LDC, tree]
    elif type(tree) == bool:
        result = [LDC, 1] if tree else [LDC, 0]
    elif type(tree) == str:
        # instructions and strings (the latter not implemented yet
        result = [tree]
    elif tree[0] == DEF:
        # Here we define a variable, first we put the value of the variable, then the index of the environment to push to
        result += evaluate(tree[2], envs, cur_env)
        env_pos = add_to_env(tree[1][1], envs,
                             cur_env)  # grab the name of the identifier, not the tag
        result += evaluate(env_pos, envs, cur_env)
        result.append(tree[0])
    elif tree[0] == DECLARE:
        # just add to the environments, but since there is no value don't add anything to the result
        add_to_env(tree[1][1], envs, cur_env)  # grab the name of the identifier, not the tag
    elif tree[0] == DEFUN:
        # Here we define a function
        index = env_index(envs, cur_env)
        #        print("adding function => " + tree[1][1])
        add_to_env(tree[1][1], envs, cur_env)  # grab the name of the identifier, not the tag
        cur_env = create_new_env(envs, cur_env)
        result += [LDC, index, DEFUN]
        result += evaluate(tree[2], envs, cur_env)
        result += [[env_index(envs, cur_env)]]
        for i in range(len(tree[3])):
            result[-1] += evaluate(tree[3][i], envs, cur_env)
    elif tree[0] == APP:
        for i in range(2, len(tree)):
            result += evaluate(tree[i], envs, cur_env)
        function_tree = tree[1]
        #        print("function name => " + function_tree[1][1])
        function_index = indexize(function_tree[1][1], envs,
                                  cur_env)  # get the name of the function and find it in environment
        result += evaluate(function_tree[2], envs, cur_env)
        result.append(APP)
        result.append(function_index)
    elif tree[0] == IF:
        # if then [LDC, 1, log_block, IF block1]
        # if then else [LDC, 2, log_block, IF, block1, block2]
        result += evaluate(tree[1], envs, cur_env)
        result += [LDC, 2] if len(tree) == 4 else [LDC, 1]
        result += [tree[0]]
        for i in range(2, len(tree)):
            result += [evaluate(tree[i], envs, cur_env)]
    elif tree[0] == CONS:
        for i in range(2, len(tree)):
            result += evaluate(tree[i], envs, cur_env)
        result += evaluate(tree[1], envs, cur_env)
        result += evaluate(tree[0], envs, cur_env)
    elif tree[0] == STRING:
        result += evaluate(tree[0], envs, cur_env)
        result += evaluate(tree[1], envs, cur_env)
    elif tree[0] == CAR or tree[0] == CDR:
        result += evaluate(tree[1], envs, cur_env)
        result += evaluate(tree[0], envs, cur_env)
    elif tree[0] == WRITE:
        result += evaluate(tree[1], envs, cur_env)
        result += evaluate(tree[0], envs, cur_env)
    elif tree[0] == "arguments":
        for i in range(len(tree[1])):
            result += evaluate(tree[1][i], envs, cur_env)
    elif tree[0] == "number":
        return evaluate(tree[1], envs, cur_env)
    elif tree[0] == "identifier":
        return [LD, indexize(tree[1], envs, cur_env)]
    elif tree[0] == "operator" or tree[0] == "log_operator" or tree[0] == "function":
        result += evaluate(tree[2], envs, cur_env)
        result += evaluate(tree[1], envs, cur_env)
    elif tree[0] == "val_exp" or tree[0] == "log_exp":
        for x in range(2, len(tree)):
            result += evaluate(tree[x], envs, cur_env)
        result += evaluate(tree[1], envs, cur_env)
    elif tree[0] == "exp":
        return evaluate(tree[0], envs, cur_env)
    elif tree[0] == "program":
        for i in range(1, len(tree)):
            result += evaluate(tree[i], envs, cur_env)
    elif isinstance(tree, tuple):
        for i in range(len(tree)):
            result += evaluate(tree[i], envs, cur_env)

    return result


def evaluate_parse_tree(tree):
    environments = [[0, None]]
    cur_env = environments[0]
    return evaluate(tree, environments, cur_env)


def env_index(envs, environment):
    assert environment in envs, "Environment doesn't exist"
    return envs.index(environment)


def indexize(var_name, envs, cur_env):
    if var_name in cur_env:
        return [envs.index(cur_env), cur_env.index(var_name)]
    assert cur_env[-1] in envs, "Variable {0} doesn't exist".format(var_name)
    return indexize(var_name, envs, cur_env[-1])


def add_to_env(var_name, envs, cur_env):
    assert var_name not in cur_env, "Variable already declared!"
    cur_env.insert(-2, var_name)
    return envs.index(cur_env)


def create_new_env(envs, parent_env):
    new_env = [parent_env]
    envs.append(new_env)
    new_env.insert(-1, len(envs) - 1)
    return new_env


def generate_stack_line(syntax, debug=False):
    parse_tree = parse(syntax)
    if debug:
        print("Parse => " + str(parse_tree))
    stack_line = evaluate_parse_tree(parse_tree)
    while stack_line[-1] == " ":
        stack_line = stack_line[0: -1]
    return stack_line
