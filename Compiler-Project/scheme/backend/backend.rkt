#lang racket

(require "../semantic/semantic.rkt")

(provide write-ir)

(define (write-ir ctx filename)
  (let ((out (open-output-file filename #:exists 'replace)))
    (define (write-lines lines)
      (cond
        ((null? lines) 'done)
        (else
         (displayln (car lines) out)
         (write-lines (cdr lines)))))
    (write-lines (semantic-get-code ctx))
    (close-output-port out)))
