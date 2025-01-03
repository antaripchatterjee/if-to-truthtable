import copy

from .error import ExpressionError, GrammarError
from .grammar import G
from .token import Token
from .context import ScriptContext


class ParserError:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ParserError, cls).__new__(cls)
            cls.__instance.__error_message = None
            cls.__instance.__degree_of_error = 0
        return cls.__instance

    def update(self, degree_of_error: int, error_message: str):
        if degree_of_error > self.__degree_of_error:
            self.__degree_of_error = degree_of_error
            self.__error_message = error_message

    @property
    def message(self):
        return self.__error_message

    @staticmethod
    def reset():
        ParserError().__error_message = None
        ParserError().__degree_of_error = 0
    

class Parser(object):
    def __init__(self):
        self.__ctx = ScriptContext()
        self.__current_path = list()
        self.__checkpoints = dict()

    def __oneof_items(self, g: dict, tokens: list[Token], doe: int):
        G_copy = copy.deepcopy(g)
        self.__current_path.append('ONEOF')
        parser_error = ParserError()
        syntax_matched = False
        eos_reached = False
        path_popped = False

        if len(tokens) == 0:
            parser_error.update(100, 'incomplete statement, could not reach end of statement')
        else:
            index = 0
            G_copy_len = len(G_copy['ONEOF'])
            while index < G_copy_len:
                option = G_copy['ONEOF'][index]
                if (isinstance(option['IF'], str) and tokens[0].ruleName == option['IF']) \
                    or (isinstance(option['IF'], (tuple, list, set)) and tokens[0].ruleName in option['IF']):
                    if syntax_matched:
                        parser_error.update(doe, 'ambiguous syntax, multiple matching pattern')
                        break
                    
                    G_next = option.get('THEN')
                    if G_next is None:
                        raise GrammarError('expects THEN')
                        
                    tokens_next = tokens[1:]

                    syntax_matched = True
                    
                    self.__current_path.append(index)

                    checkpoint = option.get('CHECKPOINT')
                    if checkpoint is not None and self.__checkpoints.get(checkpoint) is None:
                        self.__checkpoints[checkpoint] = copy.deepcopy(self.__current_path)
                    
                    if 'ANYOF' in G_next.keys():
                        eos_reached = self.__anyof_items(G_next, tokens_next, doe+1)
                    elif 'ONEOF' in G_next.keys():
                        eos_reached = self.__oneof_items(G_next, tokens_next, doe+1)
                    elif 'GOTO' in G_next.keys():
                        self.__current_path.pop()
                        self.__current_path.pop()
                        path_popped = True
                        goto = G_next['GOTO']
                        if goto is not None:
                            if isinstance(goto, str) and goto in self.__checkpoints.keys():
                                G_next = copy.deepcopy(G)
                                path = self.__checkpoints[goto]
                                
                                for i in path:
                                    G_next = G_next[i]['THEN'] if isinstance(i, int) else G_next[i]
                                
                                if 'ANYOF' in G_next.keys():
                                    eos_reached = self.__anyof_items(G_next, tokens_next, doe+1)
                                elif 'ONEOF' in G_next.keys():
                                    eos_reached = self.__oneof_items(G_next, tokens_next, doe+1)
                                else:
                                    raise GrammarError('expects ANYOF or ONEOF')
                            else:
                                raise GrammarError('checkpoint should be a string which have already been recorded')
                        else:
                            if tokens[0].ruleName == "EOS":
                                eos_reached = True
                                ParserError.reset()
                            else:
                                raise GrammarError('encountering None checkpoint before EOS')
                    else:
                        raise GrammarError('encountering None checkpoint before EOS')
                    if not path_popped: self.__current_path.pop()
                if (parser_error.message is not None and index == G_copy_len - 1) or eos_reached:
                    break
                elif index < G_copy_len - 1:
                    syntax_matched = False
                index += 1
            if not syntax_matched:
                parser_error.update(doe, f'unexpected occurrence of "{tokens[0].groupValue}"')
        if not path_popped: self.__current_path.pop()
        return eos_reached

    def __anyof_items(self, g: dict, tokens: list[Token], doe):
        G_copy = copy.deepcopy(g)
        self.__current_path.append('ANYOF')
        parser_error = ParserError()
        syntax_matched = False
        eos_reached = False
        path_popped = False

        if len(tokens) == 0:
            parser_error.update(100, 'incomplete statement, could not reach end of statement')
        else:
            index = 0
            G_copy_len = len(G_copy['ANYOF'])
            while index < G_copy_len:
                option = G_copy['ANYOF'][index]
                if (isinstance(option['IF'], str) and tokens[0].ruleName == option['IF']) \
                    or (isinstance(option['IF'], (tuple, list, set)) and tokens[0].ruleName in option['IF']):
                    
                    G_next = option.get('THEN')
                    if G_next is None:
                        raise GrammarError('expects THEN')

                    syntax_matched = True
                    self.__current_path.append(index)

                    checkpoint = option.get('CHECKPOINT')
                    if checkpoint is not None and self.__checkpoints.get(checkpoint) is None:
                        self.__checkpoints[checkpoint] = copy.deepcopy(self.__current_path)

                    tokens_next = tokens[1:]
                    if 'ANYOF' in G_next.keys():
                        eos_reached = self.__anyof_items(G_next, tokens_next, doe+1)
                    elif 'ONEOF' in G_next.keys():
                        eos_reached = self.__oneof_items(G_next, tokens_next, doe+1)
                    elif 'GOTO' in G_next.keys():
                        self.__current_path.pop()
                        self.__current_path.pop()
                        path_popped = True
                        goto = G_next['GOTO']
                        if goto is not None:
                            if isinstance(goto, str) and goto in self.__checkpoints.keys():
                                G_next = copy.deepcopy(G)
                                
                                path = self.__checkpoints[goto]
                                for i in path:
                                    G_next = G_next[i]['THEN'] if isinstance(i, int) else G_next[i]
                                
                                if 'ANYOF' in G_next.keys():
                                    eos_reached = self.__anyof_items(G_next, tokens_next, doe+1)
                                elif 'ONEOF' in G_next.keys():
                                    eos_reached = self.__oneof_items(G_next, tokens_next, doe+1)
                                else:
                                    raise GrammarError('expects ANYOF or ONEOF')
                            else:
                                raise GrammarError('checkpoint should be a string which have already been recorded')
                        else:
                            if tokens[0].ruleName == "EOS":
                                eos_reached = True
                                ParserError.reset()
                            else:
                                raise GrammarError('encountering None checkpoint before EOS')
                    else:
                        raise GrammarError('expects ANYOF or ONEOF or GOTO')
                    if not path_popped: self.__current_path.pop()

                if (parser_error.message and index == G_copy_len - 1) or syntax_matched or eos_reached:
                    break
                elif index < G_copy_len - 1:
                    syntax_matched = False
                index += 1
            if not syntax_matched:
                parser_error.update(doe, f'unexpected occurrence of "{tokens[0].groupValue}"')
        if not path_popped: self.__current_path.pop()
        return eos_reached

    def generate_ast(self, tokens: list[Token]):
        self.__anyof_items(G, tokens, 1)
        parser_error = ParserError()
        if parser_error.message is not None:
            raise ExpressionError(parser_error.message)

        
        


