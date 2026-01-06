#lang racket

(provide tokenize)

(define (make-token kind value)
  (list kind value))

(define (token-kind tok)
  (car tok))

(define (token-value tok)
  (cadr tok))

(define keywords
  (list
   (cons "let"   'LET)
   (cons "print" 'PRINT)
   (cons "if"    'IF)
   (cons "else"  'ELSE)
   (cons "while" 'WHILE)))

(define (lookup-keyword word)
  (let ((entry (assoc word keywords)))
    (if entry
        (cdr entry)
        'ID)))

(define symbols
  (list
   (cons #\+ 'PLUS)
   (cons #\- 'MINUS)
   (cons #\* 'MUL)
   (cons #\/ 'DIV)
   (cons #\= 'ASSIGN)
   (cons #\> 'GT)
   (cons #\< 'LT)
   (cons #\( 'LPAREN)
   (cons #\) 'RPAREN)
   (cons #\{ 'LBRACE)
   (cons #\} 'RBRACE)
   (cons #\; 'SEMI)))

(define (lookup-symbol ch)
  (let ((entry (assoc ch symbols)))
    (if entry
        (cdr entry)
        #f)))

(define (whitespace? ch)
  (or (char=? ch #\space)
      (char=? ch #\tab)
      (char=? ch #\newline)
      (char=? ch #\return)))

(define (letter? ch)
  (or (char-alphabetic? ch)
      (char=? ch #\_)))

(define (read-identifier chars)
  (define (loop cs acc)
    (if (and (pair? cs)
             (or (char-alphabetic? (car cs))
                 (char-numeric? (car cs))
                 (char=? (car cs) #\_)))
        (loop (cdr cs) (cons (car cs) acc))
        (cons (list->string (reverse acc)) cs)))
  (loop chars '()))

(define (read-number chars)
  (define (loop cs acc)
    (if (and (pair? cs) (char-numeric? (car cs)))
        (loop (cdr cs) (cons (car cs) acc))
        (cons (string->number (list->string (reverse acc))) cs)))
  (loop chars '()))

(define (tokenize input)
  (define chars (string->list input))

  (define (scan cs tokens)
    (cond
      ((null? cs)
       (let ((final-tokens (append tokens (list (make-token 'EOF "$")))))
         (validate-tokens final-tokens)
         final-tokens))

      ((whitespace? (car cs))
       (scan (cdr cs) tokens))

      ((letter? (car cs))
       (let* ((result (read-identifier cs))
              (word (car result))
              (rest (cdr result))
              (kind (lookup-keyword word)))
         (scan rest
               (append tokens
                       (list (make-token kind word))))))

      ((char-numeric? (car cs))
       (let* ((result (read-number cs))
              (num (car result))
              (rest (cdr result)))
         (scan rest
               (append tokens
                       (list (make-token 'INT num))))))

      ((lookup-symbol (car cs))
       (scan (cdr cs)
             (append tokens
                     (list (make-token
                            (lookup-symbol (car cs))
                            (string (car cs)))))))

      (else
       (error
        (string-append
         "Lexical error: illegal character "
         (string (car cs)))))))

  (scan chars '()))

(define (validate-tokens tokens)
  (define (loop ts brace-count paren-count)
    (cond
      ((null? ts)
       (cond
         ((not (= brace-count 0))
          (error "Syntax error: unbalanced braces"))
         ((not (= paren-count 0))
          (error "Syntax error: unbalanced parentheses"))
         (else #t)))

      ((eq? (token-kind (car ts)) 'LBRACE)
       (loop (cdr ts) (+ brace-count 1) paren-count))

      ((eq? (token-kind (car ts)) 'RBRACE)
       (if (< (- brace-count 1) 0)
           (error "Syntax error: unmatched '}'")
           (loop (cdr ts) (- brace-count 1) paren-count)))

      ((eq? (token-kind (car ts)) 'LPAREN)
       (loop (cdr ts) brace-count (+ paren-count 1)))

      ((eq? (token-kind (car ts)) 'RPAREN)
       (if (< (- paren-count 1) 0)
           (error "Syntax error: unmatched ')'")
           (loop (cdr ts) brace-count (- paren-count 1))))

      (else
       (loop (cdr ts) brace-count paren-count))))

  (if (not (eq? (token-kind (last tokens)) 'EOF))
      (error "Internal error: missing EOF token")
      (loop tokens 0 0)))

(define test-program
"let x = 5;
let y = 10;
let z = x + y * (x - 3);

if z > 10 {
    print z;
    let k = z - 1;
    if k < 20 {
        print k;
    }
    else {
        print x;
    }
}
else {
    print y;
}

while x < 10 {
    x = x + 1;
    print x;
}
")

(displayln "=== LEXER OUTPUT START ===")

(define test-tokens (tokenize test-program))

(define (print-tokens toks)
  (cond
    ((null? toks) (displayln "=== LEXER OUTPUT END ==="))
    (else
     (displayln (car toks))
     (print-tokens (cdr toks)))))

(print-tokens test-tokens)
