
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programAND CAR CDR CONS DEFINE DIVIDE EQUAL FALSE GT IDENTIFIER IF LPAREN LT MINUS MOD MULTIPLY NIL NOT NUM OR PLUS PRINT READ RPAREN STRING TRUEprogram : expexp : definition\n            | value_exp\n            | if_stmt\n            | log_exp\n            | print_expexp : exp expprint_exp : LPAREN PRINT exp RPARENread_exp : READnumber : NUMlog_val : TRUE\n                | FALSEidentifier : IDENTIFIERdefinition : LPAREN DEFINE identifier value_exp RPARENdefinition : LPAREN DEFINE identifier LPAREN arguments RPAREN LPAREN exp RPAREN RPARENarguments : declaration argumentsarguments : declaration : identifierif_stmt : LPAREN IF log_exp LPAREN exp RPAREN RPARENif_stmt : LPAREN IF log_exp LPAREN exp RPAREN LPAREN exp RPAREN RPARENlog_exp : value\n                | value_explog_exp : LPAREN log_operator log_exp log_args RPARENlog_args : log_exp log_argslog_args : log_explog_args :log_operator : AND\n                    | OR\n                    | NOT\n                    | EQUAL\n                    | GT\n                    | LTvalue_exp : LPAREN operator value_exp args RPARENvalue_exp : func_expfunc_exp : LPAREN function args RPARENfunction : identifierargs : value_exp argsargs : value_expargs : value_exp : valuevalue : identifier\n            | NIL\n            | number\n            | log_val\n            | list\n            | list_car\n            | read_exp\n    list_car : LPAREN CAR identifier RPAREN\n                | LPAREN CAR list RPAREN\n                | LPAREN CAR list_car RPARENlist : LPAREN CDR identifier RPAREN\n            | LPAREN CDR list RPARENlist : LPAREN CONS args RPARENlist : STRINGoperator : PLUS\n                | MINUS\n                | DIVIDE\n                | MULTIPLY\n                | MOD'
    
_lr_action_items = {'LPAREN':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,51,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,89,92,93,94,95,96,97,100,101,],[8,8,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,8,-36,47,50,50,8,47,58,47,62,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,66,47,-40,69,-21,-22,50,8,47,8,50,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,8,-23,93,94,8,8,-19,8,8,-15,-20,]),'NIL':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,33,35,36,37,38,39,40,41,42,43,44,45,46,48,49,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,93,94,95,96,97,100,101,],[12,12,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,12,-36,12,12,12,12,12,12,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,12,12,-40,-21,-22,12,12,12,12,12,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,12,-23,12,12,-19,12,12,-15,-20,]),'IDENTIFIER':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,54,55,57,66,69,70,72,73,75,76,77,78,79,80,81,83,84,85,86,88,91,93,94,95,96,97,100,101,],[18,18,-2,-3,-4,-5,-6,18,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,18,18,-36,18,18,18,18,18,18,18,18,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,18,18,18,-40,18,-21,-22,18,18,18,18,18,18,-8,-35,-51,-52,-53,-48,-49,-50,-18,18,-14,-33,18,-23,-18,18,18,-19,18,18,-15,-20,]),'NUM':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,33,35,36,37,38,39,40,41,42,43,44,45,46,48,49,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,93,94,95,96,97,100,101,],[19,19,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,19,-36,19,19,19,19,19,19,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,19,19,-40,-21,-22,19,19,19,19,19,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,19,-23,19,19,-19,19,19,-15,-20,]),'TRUE':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,33,35,36,37,38,39,40,41,42,43,44,45,46,48,49,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,93,94,95,96,97,100,101,],[20,20,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,20,-36,20,20,20,20,20,20,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,20,20,-40,-21,-22,20,20,20,20,20,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,20,-23,20,20,-19,20,20,-15,-20,]),'FALSE':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,33,35,36,37,38,39,40,41,42,43,44,45,46,48,49,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,93,94,95,96,97,100,101,],[21,21,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,21,-36,21,21,21,21,21,21,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,21,21,-40,-21,-22,21,21,21,21,21,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,21,-23,21,21,-19,21,21,-15,-20,]),'STRING':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,93,94,95,96,97,100,101,],[22,22,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,22,-36,22,22,22,22,22,22,22,22,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,22,22,-40,-21,-22,22,22,22,22,22,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,22,-23,22,22,-19,22,22,-15,-20,]),'READ':([0,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,33,35,36,37,38,39,40,41,42,43,44,45,46,48,49,52,53,54,55,57,69,70,72,73,75,76,77,78,79,80,81,84,85,86,88,93,94,95,96,97,100,101,],[23,23,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,23,-36,23,23,23,23,23,23,-55,-56,-57,-58,-59,-27,-28,-29,-30,-31,-32,23,23,-40,-21,-22,23,23,23,23,23,-8,-35,-51,-52,-53,-48,-49,-50,-36,-14,-33,23,-23,23,23,-19,23,23,-15,-20,]),'$end':([1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,72,73,75,76,77,78,79,80,84,85,88,95,100,101,],[0,-1,-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,-7,-8,-35,-51,-52,-53,-48,-49,-50,-14,-33,-23,-19,-15,-20,]),'RPAREN':([3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,31,33,48,49,52,53,54,55,56,57,59,60,61,63,64,65,66,67,68,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,90,91,92,95,96,97,98,99,100,101,],[-2,-3,-4,-5,-6,-41,-34,-21,-42,-43,-44,-45,-46,-47,-13,-10,-11,-12,-54,-9,-7,-36,-39,-39,-39,-40,-21,-22,-26,72,73,-38,75,76,77,78,79,80,-17,84,85,-25,88,-8,-35,-37,-51,-52,-53,-48,-49,-50,-18,89,-17,-14,-33,92,-24,-23,-16,-18,95,-19,98,99,100,101,-15,-20,]),'DEFINE':([8,],[25,]),'IF':([8,],[28,]),'PRINT':([8,],[30,]),'CDR':([8,47,50,58,62,66,],[32,32,32,32,32,32,]),'CONS':([8,47,50,58,62,66,],[33,33,33,33,33,33,]),'CAR':([8,47,50,62,66,],[34,34,34,34,34,]),'PLUS':([8,47,50,66,],[35,35,35,35,]),'MINUS':([8,47,50,66,],[36,36,36,36,]),'DIVIDE':([8,47,50,66,],[37,37,37,37,]),'MULTIPLY':([8,47,50,66,],[38,38,38,38,]),'MOD':([8,47,50,66,],[39,39,39,39,]),'AND':([8,50,],[40,40,]),'OR':([8,50,],[41,41,]),'NOT':([8,50,],[42,42,]),'EQUAL':([8,50,],[43,43,]),'GT':([8,50,],[44,44,]),'LT':([8,50,],[45,45,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'exp':([0,2,24,30,55,69,86,93,94,96,97,],[2,24,24,55,24,86,24,96,97,24,24,]),'definition':([0,2,24,30,55,69,86,93,94,96,97,],[3,3,3,3,3,3,3,3,3,3,3,]),'value_exp':([0,2,24,27,28,29,30,31,33,46,48,54,55,57,69,70,86,93,94,96,97,],[4,4,4,48,53,53,4,57,57,67,57,53,4,57,4,53,4,4,4,4,4,]),'if_stmt':([0,2,24,30,55,69,86,93,94,96,97,],[5,5,5,5,5,5,5,5,5,5,5,]),'log_exp':([0,2,24,28,29,30,54,55,69,70,86,93,94,96,97,],[6,6,6,51,54,6,70,6,6,70,6,6,6,6,6,]),'print_exp':([0,2,24,30,55,69,86,93,94,96,97,],[7,7,7,7,7,7,7,7,7,7,7,]),'identifier':([0,2,8,24,25,27,28,29,30,31,32,33,34,46,47,48,50,54,55,57,66,69,70,83,86,93,94,96,97,],[9,9,26,9,46,9,9,9,9,9,59,9,63,9,26,9,26,9,9,9,81,9,9,91,9,9,9,9,9,]),'func_exp':([0,2,24,27,28,29,30,31,33,46,48,54,55,57,69,70,86,93,94,96,97,],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'value':([0,2,24,27,28,29,30,31,33,46,48,54,55,57,69,70,86,93,94,96,97,],[11,11,11,49,52,52,11,49,49,49,49,52,11,49,11,52,11,11,11,11,11,]),'number':([0,2,24,27,28,29,30,31,33,46,48,54,55,57,69,70,86,93,94,96,97,],[13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,]),'log_val':([0,2,24,27,28,29,30,31,33,46,48,54,55,57,69,70,86,93,94,96,97,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'list':([0,2,24,27,28,29,30,31,32,33,34,46,48,54,55,57,69,70,86,93,94,96,97,],[15,15,15,15,15,15,15,15,60,15,64,15,15,15,15,15,15,15,15,15,15,15,15,]),'list_car':([0,2,24,27,28,29,30,31,33,34,46,48,54,55,57,69,70,86,93,94,96,97,],[16,16,16,16,16,16,16,16,16,65,16,16,16,16,16,16,16,16,16,16,16,16,]),'read_exp':([0,2,24,27,28,29,30,31,33,46,48,54,55,57,69,70,86,93,94,96,97,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'operator':([8,47,50,66,],[27,27,27,27,]),'log_operator':([8,50,],[29,29,]),'function':([8,47,50,66,],[31,31,31,31,]),'args':([31,33,48,57,],[56,61,68,74,]),'log_args':([54,70,],[71,87,]),'arguments':([66,83,],[82,90,]),'declaration':([66,83,],[83,83,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> exp','program',1,'p_program','compiler.py',180),
  ('exp -> definition','exp',1,'p_exp','compiler.py',185),
  ('exp -> value_exp','exp',1,'p_exp','compiler.py',186),
  ('exp -> if_stmt','exp',1,'p_exp','compiler.py',187),
  ('exp -> log_exp','exp',1,'p_exp','compiler.py',188),
  ('exp -> print_exp','exp',1,'p_exp','compiler.py',189),
  ('exp -> exp exp','exp',2,'p_exp_exp','compiler.py',194),
  ('print_exp -> LPAREN PRINT exp RPAREN','print_exp',4,'p_print_exp','compiler.py',199),
  ('read_exp -> READ','read_exp',1,'p_read_exp','compiler.py',204),
  ('number -> NUM','number',1,'p_number','compiler.py',209),
  ('log_val -> TRUE','log_val',1,'p_log_val','compiler.py',214),
  ('log_val -> FALSE','log_val',1,'p_log_val','compiler.py',215),
  ('identifier -> IDENTIFIER','identifier',1,'p_identifier','compiler.py',220),
  ('definition -> LPAREN DEFINE identifier value_exp RPAREN','definition',5,'p_definition','compiler.py',225),
  ('definition -> LPAREN DEFINE identifier LPAREN arguments RPAREN LPAREN exp RPAREN RPAREN','definition',10,'p_defun','compiler.py',230),
  ('arguments -> declaration arguments','arguments',2,'p_arguments','compiler.py',235),
  ('arguments -> <empty>','arguments',0,'p_empty_arguments','compiler.py',240),
  ('declaration -> identifier','declaration',1,'p_declaration','compiler.py',245),
  ('if_stmt -> LPAREN IF log_exp LPAREN exp RPAREN RPAREN','if_stmt',7,'p_if_stmt','compiler.py',250),
  ('if_stmt -> LPAREN IF log_exp LPAREN exp RPAREN LPAREN exp RPAREN RPAREN','if_stmt',10,'p_if_else_stmt','compiler.py',255),
  ('log_exp -> value','log_exp',1,'p_log_expression','compiler.py',260),
  ('log_exp -> value_exp','log_exp',1,'p_log_expression','compiler.py',261),
  ('log_exp -> LPAREN log_operator log_exp log_args RPAREN','log_exp',5,'p_log_expression_op','compiler.py',266),
  ('log_args -> log_exp log_args','log_args',2,'p_log_args','compiler.py',272),
  ('log_args -> log_exp','log_args',1,'p_log_arg','compiler.py',277),
  ('log_args -> <empty>','log_args',0,'p_opt_log_args','compiler.py',282),
  ('log_operator -> AND','log_operator',1,'p_log_operator','compiler.py',287),
  ('log_operator -> OR','log_operator',1,'p_log_operator','compiler.py',288),
  ('log_operator -> NOT','log_operator',1,'p_log_operator','compiler.py',289),
  ('log_operator -> EQUAL','log_operator',1,'p_log_operator','compiler.py',290),
  ('log_operator -> GT','log_operator',1,'p_log_operator','compiler.py',291),
  ('log_operator -> LT','log_operator',1,'p_log_operator','compiler.py',292),
  ('value_exp -> LPAREN operator value_exp args RPAREN','value_exp',5,'p_value_exp','compiler.py',297),
  ('value_exp -> func_exp','value_exp',1,'p_value_exp_func','compiler.py',303),
  ('func_exp -> LPAREN function args RPAREN','func_exp',4,'p_func_exp','compiler.py',308),
  ('function -> identifier','function',1,'p_function','compiler.py',313),
  ('args -> value_exp args','args',2,'p_args','compiler.py',318),
  ('args -> value_exp','args',1,'p_arg','compiler.py',323),
  ('args -> <empty>','args',0,'p_opt_args','compiler.py',328),
  ('value_exp -> value','value_exp',1,'p_val_exp','compiler.py',333),
  ('value -> identifier','value',1,'p_value','compiler.py',338),
  ('value -> NIL','value',1,'p_value','compiler.py',339),
  ('value -> number','value',1,'p_value','compiler.py',340),
  ('value -> log_val','value',1,'p_value','compiler.py',341),
  ('value -> list','value',1,'p_value','compiler.py',342),
  ('value -> list_car','value',1,'p_value','compiler.py',343),
  ('value -> read_exp','value',1,'p_value','compiler.py',344),
  ('list_car -> LPAREN CAR identifier RPAREN','list_car',4,'p_car','compiler.py',350),
  ('list_car -> LPAREN CAR list RPAREN','list_car',4,'p_car','compiler.py',351),
  ('list_car -> LPAREN CAR list_car RPAREN','list_car',4,'p_car','compiler.py',352),
  ('list -> LPAREN CDR identifier RPAREN','list',4,'p_cdr','compiler.py',357),
  ('list -> LPAREN CDR list RPAREN','list',4,'p_cdr','compiler.py',358),
  ('list -> LPAREN CONS args RPAREN','list',4,'p_cons_list','compiler.py',363),
  ('list -> STRING','list',1,'p_string','compiler.py',368),
  ('operator -> PLUS','operator',1,'p_operator','compiler.py',373),
  ('operator -> MINUS','operator',1,'p_operator','compiler.py',374),
  ('operator -> DIVIDE','operator',1,'p_operator','compiler.py',375),
  ('operator -> MULTIPLY','operator',1,'p_operator','compiler.py',376),
  ('operator -> MOD','operator',1,'p_operator','compiler.py',377),
]
