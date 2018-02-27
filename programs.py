from compiler import generate_stack_line
from stack_machine import SECD

__author__ = 'Arin'


def run_program(syntax):
    code = generate_stack_line(syntax)
    s = SECD()
    s.run_program(code)



#run_program("""
#(define change_opt (amount coins)
#  ((if (= amount 0)
#      (1)
#      ((if (< amount 0)
#          (0)
#          ((if (= (cdr coins) nil)
#              ((if (= (% amount (car coins)) 0)
#                  (1)
#                  (0)))
#              ((+ (change_opt (- amount (car coins)) coins)
#                  (change_opt amount (cdr coins)))))))))))
#(define change_options (change_opt 20 (cons 1 2 5 10 20)))
#(print change_options)
#""")
#
#run_program("""
#(define less_equal (x y)
#    ((or (< x y) (= x y))))
#(define factorial (x)
#    ((if (less_equal x 1)
#        (1)
#        ((* x (factorial (- x 1)))))))
#(print (factorial 10))
#""")
#
#run_program("""
#(define print_even (x)
#(
#    (if (= (% x 2) 0)
#    (
#        (print x)
#    ))
#    (if (> x 0)
#    (
#        (print_even (- x 1))
#    ))
#))
#(print_even 12)
#""")
#
#
#run_program("""
#(define factorial (x) ((if (= x 1) (1) ((* x (factorial (- x 1)))))))
#
#(define factorial_read () ((print (factorial read))))
#
#(factorial_read)
#
#""")


#run_program("""
#(if (= 1 1)
#    ((print "text")
#    (print "text2")))
#""")
#
#
#run_program("""
#(define print_times (x)
#    ((if (> x 0)
#        ((print x)
#        (print_times (- x 1))))))
#(print_times read)
#""")




#run_program("""
#(print "xxx")
#""")
#
#run_program("""
#(print (cons "x" (cons "y" "z" "xxx")))
#""")
#
#run_program("""
#(print (cons 1 (cons 1 1) 2 3 4 5))
#""")

#run_program("""
#(define x 5)
#(define foo ()
#(
#    (print (+ x 5))
#))
#(define bar ()
#(
#    (define x 2)
#    (foo)
#))
#
#(foo)
#(bar)
#""")
#
#
run_program("""

(define x 22)

(define function ()
    (x)
)

(function)

""")


run_program("""
(define add_space (string)
    ((cons string " ")))

(define add_underscore (string)
    ((cons string "_")))

(define add_left_pine (string)
    ((cons string "/")))

(define add_right_pine (string)
    ((cons string "\\")))

(define add_middle_pine (string)
    ((cons string "|")))

(define add_spaces (string amount)
(
    (if (> amount 0)
    (
        (add_space (add_spaces string (- amount 1)))
    )
    (
        string
    ))
))

(define add_underscores (string amount)
(
    (if (> amount 0)
    (
        (add_underscore (add_underscores string (- amount 1)))
    )
    (
        string
    ))
))

(define print_pine_line (height cur_height)
(
    (if (< (- height cur_height) 3)
    (
        (add_middle_pine (add_spaces (add_middle_pine (add_spaces "" (- height 3))) 6))
    )
    (
        (if (= (- height cur_height) 3)
        (
            (add_right_pine (add_underscores (add_left_pine (add_spaces "" (- height cur_height))) (+ cur_height (- height (- height cur_height)))))
        )
        (
            (add_right_pine (add_spaces (add_left_pine (add_spaces "" (- height cur_height))) (+ cur_height (- height (- height cur_height)))))
        ))
    ))
))

(define print_pine (height cur_height)
(
    (if (not (> cur_height height))
    (
        (print (print_pine_line height cur_height))
        (print_pine height (+ cur_height 1))
    ))
))

(define ask_for_pine ()
(
    (print "Christmas come early! Please state how high your Christmas tree should be.")
    (define x read)

    (if (< x 12)
    (
        (print "Come on, don't be a cheapskate, buy a bigger one")
        (ask_for_pine)
    )
    (
        (if (> x 22)
        (
            (print "Come on, no Christmas tree grows that high! Buy a smaller one.")
            (ask_for_pine)
        )
        (
            (print_pine x 0)
        ))
    ))
))

(ask_for_pine)
""")



