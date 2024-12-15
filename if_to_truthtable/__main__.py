import sys
import argparse

from . import ExpressionBuilder
from . import Lexer
from . import ExpressionError

def read_exprs_from_cmdline(args):
    # Read value from '-e' argument
    if args.expression:
        return args.expression

    # Read value from standard input (file redirection)
    if not sys.stdin.isatty():
        return sys.stdin.read()

    # If no arguments are provided, return None to enter interactive mode
    return None

def interactive_mode():
    print("Entering interactive mode. Press Ctrl+C to quit.")
    try:
        msg = '>  '
        code = ''
        while True:
            line = input(msg)
            code += line + '\n'
            if line.endswith('\\'):
                msg = '.. '
                code = code[:-2] + '\n'
            else:
                try:
                    for expr, expr_id in ExpressionBuilder(code).cleanComments().expressions():
                        tokens = Lexer(expr=expr, expr_id=expr_id).tokenize()
                        for token in tokens:
                            print(token)
                except ExpressionError as e:
                    print(e, file=sys.stderr)
                finally:
                    msg = '>  '
                    code = ''
    except KeyboardInterrupt:
        print("\nExiting interactive mode.")

def main():
    parser = argparse.ArgumentParser(description="Read value from arguments or enter interactive mode.")
    parser.add_argument('-e', '--expression', type=str, help="Expression to read as value")
    args = parser.parse_args()

    code = read_exprs_from_cmdline(args)
    if code is not None:
        try:
            for expr, expr_id in ExpressionBuilder(code).cleanComments().expressions():
                tokens = Lexer(expr=expr, expr_id=expr_id).tokenize()
                for token in tokens:
                    print(token)
        except ExpressionError as e:
            print(e, file=sys.stderr)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
