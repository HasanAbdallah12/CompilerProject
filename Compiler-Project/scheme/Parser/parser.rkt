#lang racket

(require "../semantic/semantic.rkt")
(provide parse-program)

(define (parse-error msg)
  (error (string-append "Parse error: " msg)))

(define tokens '())
(define pos 0)
(define ctx #f)

(define val-stack '())
(define assign-target #f)

(define (current)
  (list-ref tokens pos))

(define (kind)
  (car (current)))

(define (value)
  (cadr (current)))

(define (eat k)
  (if (eq? (kind) k)
      (set! pos (+ pos 1))
      (parse-error
       (format "Expected ~a, got ~a" k (kind)))))

(define (push-id)
  (semantic-check ctx (string->symbol (value)))
  (set! val-stack (cons (value) val-stack)))

(define (push-int)
  (set! val-stack (cons (number->string (value)) val-stack)))

(define (emit-bin op)
  (let* ((b (car val-stack))
         (a (cadr val-stack))
         (t (semantic-new-temp ctx)))
    (set! val-stack (cddr val-stack))
    (semantic-emit ctx
      (string-append t " = " a " " op " " b))
    (set! val-stack (cons t val-stack))))

(define (parse-program-internal)
  (parse-stmlist)
  (eat 'EOF)
  ctx)

(define (parse-stmlist)
  (cond
    ((member (kind) '(LET ID PRINT IF WHILE))
     (parse-stmt)
     (parse-stmlist))
    (else '())))

(define (parse-stmt)
  (cond
    ((eq? (kind) 'LET)
     (eat 'LET)
     (let ((name (value)))
       (eat 'ID)
       (semantic-declare ctx (string->symbol name))
       (set! assign-target name)
       (eat 'ASSIGN)
       (parse-expr)
       (semantic-emit ctx
         (string-append assign-target " = " (car val-stack)))
       (set! val-stack (cdr val-stack))
       (eat 'SEMI)))

    ((eq? (kind) 'ID)
     (let ((name (value)))
       (eat 'ID)
       (semantic-check ctx (string->symbol name))
       (set! assign-target name)
       (eat 'ASSIGN)
       (parse-expr)
       (semantic-emit ctx
         (string-append assign-target " = " (car val-stack)))
       (set! val-stack (cdr val-stack))
       (eat 'SEMI)))

    ((eq? (kind) 'PRINT)
     (eat 'PRINT)
     (parse-expr)
     (semantic-emit ctx
       (string-append "print " (car val-stack)))
     (set! val-stack (cdr val-stack))
     (eat 'SEMI))

    ((eq? (kind) 'IF)
     (eat 'IF)
     (parse-rel)
     (eat 'LBRACE)
     (parse-stmlist)
     (eat 'RBRACE)
     (eat 'ELSE)
     (eat 'LBRACE)
     (parse-stmlist)
     (eat 'RBRACE))

    ((eq? (kind) 'WHILE)
     (eat 'WHILE)
     (parse-rel)
     (eat 'LBRACE)
     (parse-stmlist)
     (eat 'RBRACE))

    (else
     (parse-error "Invalid statement"))))

(define (parse-rel)
  (parse-expr)
  (cond
    ((eq? (kind) 'GT)
     (eat 'GT)
     (parse-expr)
     (set! val-stack (cddr val-stack)))
    ((eq? (kind) 'LT)
     (eat 'LT)
     (parse-expr)
     (set! val-stack (cddr val-stack)))
    (else '())))

(define (parse-expr)
  (parse-term)
  (parse-expr-tail))

(define (parse-expr-tail)
  (cond
    ((eq? (kind) 'PLUS)
     (eat 'PLUS)
     (parse-term)
     (emit-bin "+")
     (parse-expr-tail))
    ((eq? (kind) 'MINUS)
     (eat 'MINUS)
     (parse-term)
     (emit-bin "-")
     (parse-expr-tail))
    (else '())))

(define (parse-term)
  (parse-factor)
  (parse-term-tail))

(define (parse-term-tail)
  (cond
    ((eq? (kind) 'MUL)
     (eat 'MUL)
     (parse-factor)
     (emit-bin "*")
     (parse-term-tail))
    ((eq? (kind) 'DIV)
     (eat 'DIV)
     (parse-factor)
     (emit-bin "/")
     (parse-term-tail))
    (else '())))

(define (parse-factor)
  (cond
    ((eq? (kind) 'INT)
     (push-int)
     (eat 'INT))
    ((eq? (kind) 'ID)
     (push-id)
     (eat 'ID))
    ((eq? (kind) 'LPAREN)
     (eat 'LPAREN)
     (parse-expr)
     (eat 'RPAREN))
    (else
     (parse-error "Invalid factor"))))

(define (parse-program token-list)
  (set! tokens token-list)
  (set! pos 0)
  (set! val-stack '())
  (set! assign-target #f)
  (set! ctx (make-semantic-context))
  (parse-program-internal))
