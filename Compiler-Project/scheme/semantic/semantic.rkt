#lang racket

(provide
 make-semantic-context
 semantic-declare
 semantic-check
 semantic-emit
 semantic-new-temp
 semantic-new-label
 semantic-get-code)

(define (make-semantic-context)
  (let (
        (symbols '())
        (code '())
        (temp-counter 0)
        (label-counter 0)
       )

    (define (declare name)
      (set! symbols (cons name symbols)))

    (define (check name)
      (if (not (member name symbols))
          (error
           (string-append
            "Semantic error: variable not defined -> "
            (symbol->string name)))
          #t))

    (define (emit line)
      (set! code (append code (list line))))

    (define (new-temp)
      (set! temp-counter (+ temp-counter 1))
      (string-append "t" (number->string temp-counter)))

    (define (new-label)
      (set! label-counter (+ label-counter 1))
      (string-append "L" (number->string label-counter)))

    (define (get-code)
      code)

    (list
     (cons 'declare declare)
     (cons 'check check)
     (cons 'emit emit)
     (cons 'new-temp new-temp)
     (cons 'new-label new-label)
     (cons 'get-code get-code))))

(define (semantic-declare ctx name)
  ((cdr (assoc 'declare ctx)) name))

(define (semantic-check ctx name)
  ((cdr (assoc 'check ctx)) name))

(define (semantic-emit ctx line)
  ((cdr (assoc 'emit ctx)) line))

(define (semantic-new-temp ctx)
  ((cdr (assoc 'new-temp ctx))))

(define (semantic-new-label ctx)
  ((cdr (assoc 'new-label ctx))))

(define (semantic-get-code ctx)
  ((cdr (assoc 'get-code ctx))))
