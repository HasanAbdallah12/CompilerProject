# backend/backend.py

def write_ir(ctx, filename="out.ir"):
    f = open(filename, "w", encoding="utf-8")
    for line in ctx.code:
        f.write(line + "\n")
    f.close()
