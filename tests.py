from compiler import generate_stack_line
from stack_machine import SECD, LDC, SUB, MUL, ADD, DEF, LD, DEFUN, APP, IF, AND, EQUAL, NOT, CONS, CAR, CDR, TERM_INT, \
    WRITE, NIL, STRING, TERM_CHAR, OR, LT

__author__ = 'Arin'


def test_syntax(syntax, answer, debug=False):
    result = generate_stack_line(syntax, debug)
    if debug:
        print("\n")
        print("Test result => " + str(result))
        print("\n")
    return answer == result


def test_semantics(syntax, answer, debug=False):
    program = generate_stack_line(syntax, debug)
    s = SECD()
    if debug:
        print("Semantic Specialization project:")
        print("Program => " + str(program))
    result = s.run_program_for_result(program)
    if debug:
        print("Result => " + str(result))
    return answer == result


tests_syn = []


def add_syn_test(syntax, answer, debug = False):
    tests_syn.append(test_syntax(syntax, answer, debug))


def add_sem_test(syntax, answer, debug = False):
    tests_sem.append(test_semantics(syntax, answer, debug))


add_syn_test("(* 2 5 (- 2 2)) (+ 3 2)",
             [LDC, 2, LDC, 5, LDC, 2, LDC, 2, LDC, 2, SUB, LDC, 3, MUL, LDC, 3, LDC, 2, LDC, 2, ADD],
             False)

add_syn_test("(define x (* 2 3 12 83))",
             [LDC, 2, LDC, 3, LDC, 12, LDC, 83, LDC, 4, MUL, LDC, 0, DEF],
             False)

add_syn_test("(define x (* 2 7)) (define z (+ 1 3)) (- x z)",
             [LDC, 2, LDC, 7, LDC, 2, MUL, LDC, 0, DEF, LDC, 1, LDC, 3, LDC, 2, ADD, LDC, 0, DEF, LD, [0, 0], LD, [0, 1], LDC, 2, SUB],
             False)

add_syn_test("(define function (x y) ((+ x y)))",
             [LDC, 0, DEFUN, [1, LD, [1, 0], LD, [1, 1], LDC, 2, ADD]],
             False)

add_syn_test("(define function (x y) ((+ x y))) (function 3 7)",
             [LDC, 0, DEFUN, [1, LD, [1, 0], LD, [1, 1], LDC, 2, ADD], LDC, 3, LDC, 7, LDC, 2, APP, [0, 0]],
             False)

add_syn_test("(define p 4) (define fun1 (x y) ((+ x y))) (define fun2 (x z) ((fun1 x (+ z p))))",
             [LDC, 4, LDC, 0, DEF, LDC, 0, DEFUN, [1, LD, [1, 0], LD, [1, 1], LDC, 2, ADD], LDC, 0, DEFUN, [2, LD, [2, 0], LD, [2, 1], LD, [0, 0], LDC, 2, ADD, LDC, 2, APP, [0, 1]]],
             False)

add_syn_test("(define p 4) (define fun1 (x y) ((+ x y))) (define fun2 (x z) ((fun1 x (+ z p)))) (fun2 1 7)",
             [LDC, 4, LDC, 0, DEF, LDC, 0, DEFUN, [1, LD, [1, 0], LD, [1, 1], LDC, 2, ADD], LDC, 0, DEFUN, [2, LD, [2, 0], LD, [2, 1], LD, [0, 0], LDC, 2, ADD, LDC, 2, APP, [0, 1]], LDC, 1, LDC, 7, LDC, 2, APP, [0, 2]],
             False)

add_syn_test("(if (and true false) ((+ 2 2 2)) ((- 2 2)))",
             [LDC, 1, LDC, 0, LDC, 2, AND, LDC, 2, IF, [LDC, 2, LDC, 2, LDC, 2, LDC, 3, ADD], [LDC, 2, LDC, 2, LDC, 2, SUB]],
             False)

add_syn_test("(= 4 5)",
             [LDC, 4, LDC, 5, LDC, 2, EQUAL],
             False)

add_syn_test("(define are_equal (x y) ((if (not (= x y)) (false) (true))))",
             [LDC, 0, DEFUN, [1, LD, [1, 0], LD, [1, 1], LDC, 2, EQUAL, LDC, 1, NOT, LDC, 2, IF, [LDC, 0], [LDC, 1]]],
             False)

add_syn_test("(define x (cons (+ 7 10) 8))",
             [LDC, 7, LDC, 10, LDC, 2, ADD, LDC, 8, LDC, 2, CONS, LDC, 0, DEF],
             False)

add_syn_test("(define x (cons (+ 7 10) 8)) (car x)",
             [LDC, 7, LDC, 10, LDC, 2, ADD, LDC, 8, LDC, 2, CONS, LDC, 0, DEF, LD, [0, 0], CAR],
             False)

add_syn_test("(define x (cons  23 75 69 100)) (car (cdr x))",
             [LDC, 23, LDC, 75, LDC, 69, LDC, 100, LDC, 4, CONS, LDC, 0, DEF, LD, [0, 0], CDR, CAR],
             False)

add_syn_test("(print 54)",
             [LDC, 54, WRITE],
             False)

add_syn_test('(define x "string")',
             [STRING, "string", LDC, 0, DEF],
             False)

add_syn_test('(define x (cdr "sstring")) (print x) (print "string 2")',
             [STRING, "sstring", CDR, LDC, 0, DEF, LD, [0, 0], WRITE, STRING, "string 2", WRITE],
             False)

add_syn_test("""
(define less_equal (x y)
(
    (or (= x y) (< x y))
))""",
             [LDC, 0, DEFUN, [1, LD, [1, 0], LD, [1, 1], LDC, 2, EQUAL, LD, [1, 0], LD, [1, 1], LDC, 2, LT, LDC, 2, OR]],
             False)

for i in range(len(tests_syn)):
    print("Syntactical test nr {0} => {1}".format(i, tests_syn[i]))

print("")

tests_sem = []

add_sem_test("(define p 12) (define fun (x y) ((+ x y))) (define fun2 (x z) ((+ x (fun p z) 7))) (+ (fun (fun2 12 5) (fun2 3 2)) 17)",
             [TERM_INT, 77], False)

add_sem_test("(define a 100) (define b 20) (define fun1 (a b) ((- a b))) (define fun2 (x y) ((fun1 (fun1 a x) (fun1 y b)))) (+ a (fun2 10 15))",
             [TERM_INT, 195], False)

add_sem_test("(define fun1 (z y) ((define fun2 (z) ((+ z y))) (+ (fun2 z) y))) (fun1 4 (fun1 1 6))",
             [TERM_INT, 30], False)

add_sem_test("(if false (666) (42))",
             [TERM_INT, 42], False)

add_sem_test("(if (or false false true false false) ((+ 2 2 2)) ((- 2 2)))",
             [TERM_INT, 6], False)

add_sem_test("(if (not (or (and true false) (or false false) false (not false))) ((+ 4 9)) ((- 100 50)))",
             [TERM_INT, 50], False)

add_sem_test("(define x 2) (= x 2)",
             [TERM_INT, 1], False)

add_sem_test("(define are_equal (x y) ((if (not (= x y)) (false) (true)))) (are_equal 2 2)",
             [TERM_INT, 1], False)

add_sem_test("(define greater (x y) ((> x y))) (if (greater 6 2) ((greater 20 100)) ((+ 5 5)))",
             [TERM_INT, 0], False)

add_sem_test("(define equal (x y) ((= x y))) "
             "(define greater_equal (x y) ((define greater (x y) ((> x y))) (or (equal x y) (greater x y)))) "
             "(and (greater_equal 5 5) (greater_equal 66 8) (not (greater_equal 800 2000)))",
             [TERM_INT, 1], False)

add_sem_test("(define factorial (x) ((if (= x 1) (1) ((* x (factorial (- x 1))))))) (factorial 6)",
             [TERM_INT, 720], False)

add_sem_test("(define fibbonacci (x) ((if (or (< x 2) (= x 2)) (1) ((+ (fibbonacci (- x 1)) (fibbonacci (- x 2))))))) (define fun1 (x y) ((if (> x y) ((fun1 (- x 1) y)) ((fibbonacci x))))) (define fun2 (z p) ((fun1 (+ z p) p))) (fun2 5 15)",
             [TERM_INT, 610], False)

add_sem_test("(define fun (x y) ((+ x y))) (define x (fun 12 54)) x",
             [TERM_INT, 66], False)

add_sem_test("(define x (cons 32 65 23 29)) (car (cdr (cdr x)))",
             [TERM_INT, 23], False)

add_sem_test("""(define caadr (list) ((car (car (cdr list)))))
                                    (define cddr (list) ((cdr (cdr list))))
                                    (define x (cddr (cons 54 43 100 (cons 42 69 13) 65)))
                                    (caadr x)""",
             [TERM_INT, 42], False)

add_sem_test("""
(define fun (val1 val2)
    ((if (= (% val1 val2) 0)
        (1)
        (2))))
(fun 20 5)
""", [TERM_INT, 1], False)

add_sem_test("(define x nil) (= x nil)", [TERM_INT, 1], False)

add_sem_test("""
(define change_opt (amount coins)
  ((if (= amount 0)
      (1)
      ((if (< amount 0)
          (0)
          ((if (= (cdr coins) nil)
              ((if (= (% amount (car coins)) 0)
                  (1)
                  (0)))
              ((+ (change_opt (- amount (car coins)) coins)
                  (change_opt amount (cdr coins)))))))))))
(change_opt 20 (cons 1 2 5 10 20))
""", [TERM_INT, 41], False)

add_sem_test("""
(define x "xstring") (car (cdr x))
""", [TERM_CHAR, 's'], False)



for i in range(len(tests_sem)):
    print("Semantical test nr {0} => {1}".format(i, tests_sem[i]))


success = all(tests_syn) and all(tests_sem)
print("\nAll tests succeded => {0}".format(success))

if not success:
    for i in range(len(tests_syn)):
        if not tests_syn[i]:
            print("Failure in syntactical test number => {0}".format(i))
    for i in range(len(tests_sem)):
        if not tests_sem[i]:
            print("Failure in semantical test number => {0}".format(i))

