import sys
import argparse

from . import ExpressionBuilder
from . import Lexer
from . import ExpressionError, GrammarError
from . import Parser

def read_exprs_from_cmdline(args):
    # Read value from '-e' argument
    if args.expression:
        return args.expression
    elif args.filename:
        return open(args.filename).read()
    # Read value from standard input (file redirection)
    # if not sys.stdin.isatty():
    #     return sys.stdin.read()

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
                    for expr in ExpressionBuilder(code).cleanComments().expressions():
                        tokens = Lexer(expr=expr).tokenize()
                        if len(tokens) > 1:
                            parser = Parser()
                            parser.generate_ast(tokens)
                except (ExpressionError, GrammarError) as e:
                    print(f'{expr}\n{e}', file=sys.stderr)
                finally:
                    msg = '>  '
                    code = ''
    except KeyboardInterrupt:
        print("\nExiting interactive mode.")

def main():
    parser = argparse.ArgumentParser(description="Read value from arguments or enter interactive mode.")
    parser = argparse.ArgumentParser(description="Process a filename or an expression.")
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-e', '--expression', type=str, help='Provide an expression as input')
    group.add_argument('filename', nargs='?', help='Provide a filename as input')
    
    # Parse the arguments
    args = parser.parse_args()
    try:
        code = read_exprs_from_cmdline(args)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return
    
    if code is not None:
        try:
            for expr in ExpressionBuilder(code).cleanComments().expressions():
                tokens = Lexer(expr=expr).tokenize()
                if len(tokens) > 1:
                    parser = Parser()
                    parser.generate_ast(tokens)
        except (ExpressionError, GrammarError) as e:
            print(f'{expr}\n{e}', file=sys.stderr)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
