#lang racket

(require "Lexer/lexer.rkt")
(require "Parser/parser.rkt")
(require "semantic/semantic.rkt")
(require "backend/backend.rkt")

(define test-program
"let x = 5;
let y = 10;
let z = x + y * (x - 3) / 2;

print z;

if z > 10 {
    let a = z - 1;
    print a;

    if a < 20 {
        let b = a * 2;
        print b;
    }
    else {
        let c = a / 2;
        print c;
    }
}
else {
    let d = z + 1;
    print d;
}

while x < 10 {
    x = x + 1;
    print x;
}
")

(displayln "===== SOURCE CODE =====")
(displayln test-program)

(displayln "===== LEXER =====")
(define tokens (tokenize test-program))
(for-each displayln tokens)

(displayln "===== PARSER + SEMANTIC =====")
(define ctx (parse-program tokens))

(displayln "===== INTERMEDIATE CODE (IR) =====")
(for-each displayln (semantic-get-code ctx))

(displayln "===== BACKEND =====")
(write-ir ctx "out.ir")

(displayln "Compilation finished successfully.")
(displayln "IR written to out.ir")
