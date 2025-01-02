import copy

from .error import ExpressionError, GrammarError
from .grammar import G
from .token import Token
from .context import ScriptContext


class ParserError:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParserError, cls).__new__(cls)
            cls._instance._error_messages = []
        return cls._instance

    def __lshift__(self, error: str):
        if isinstance(error, str):
            self._error_messages.append(error)
        else:
            raise TypeError("Only str object is allowed")
        return self
    
    def __iter__(self):
        for e in self._error_messages:
            yield e
    
    def __str__(self):
        if self.has_errors():
            return 'one or more expression errors during parsing\n * ' \
                + '\n * '.join(self._error_messages)
        else:
            return None
    
    def messages(self):
        return self._error_messages

    def clear(self):
        self._error_messages.clear()

    def has_errors(self):
        return len(self._error_messages) > 0
    

class Parser(object):
    def __init__(self):
        self.__ctx = ScriptContext()
        self.__current_path = list()
        self.__checkpoints = dict()

    def __oneof_items(self, g: dict, tokens: list[Token], caller, x):
        # print(f'__oneof_items called by {caller} -> {x}')
        G_copy = copy.deepcopy(g)
        self.__current_path.append('ONEOF')
        error_stack = ParserError()
        syntax_matched = False
        eos_reached = False

        if len(tokens) == 0:
            error_stack << 'incomplete statement, could not reach end of statement'
        else:
            # print(tokens[0])
            index = 0
            G_copy_len = len(G_copy['ONEOF'])
            while index < G_copy_len:
                option = G_copy['ONEOF'][index]
                # print(index, option['IF'], end=' ')
                if (isinstance(option['IF'], str) and tokens[0].ruleName == option['IF']) \
                    or (isinstance(option['IF'], (tuple, list, set)) and tokens[0].ruleName in option['IF']):
                    # print('✅')
                    if syntax_matched:
                        error_stack << 'ambiguous syntax, multiple matching pattern'
                        break
                    
                    G_next = option.get('THEN')
                    if G_next is None:
                        raise GrammarError('expects THEN')
                        
                    tokens_next = tokens[1:]

                    syntax_matched = True
                    
                    self.__current_path.append(index)

                    checkpoint = option.get('CHECKPOINT')
                    if checkpoint is not None:
                        self.__checkpoints[checkpoint] = copy.deepcopy(self.__current_path)
                    
                    if 'ANYOF' in G_next.keys():
                        eos_reached = self.__anyof_items(G_next, tokens_next, '__oneof_items', x+1)
                    elif 'ONEOF' in G_next.keys():
                        eos_reached = self.__oneof_items(G_next, tokens_next, '__oneof_items', x+1)
                    elif 'GOTO' in G_next.keys():
                        goto = G_next['GOTO']
                        if goto is not None:
                            if isinstance(goto, str) and goto in self.__checkpoints.keys():
                                G_next = copy.deepcopy(G)
                                
                                path = self.__checkpoints[goto]
                                for i in path:
                                    G_next = G_next[i]['THEN'] if isinstance(i, int) else G_next[i]
                                
                                if 'ANYOF' in G_next.keys():
                                    eos_reached = self.__anyof_items(G_next, tokens_next, '__oneof_items', x+1)
                                elif 'ONEOF' in G_next.keys():
                                    eos_reached = self.__oneof_items(G_next, tokens_next, '__oneof_items', x+1)
                                else:
                                    raise GrammarError('expects ANYOF or ONEOF')
                            else:
                                raise GrammarError('checkpoint should be a string which have already been recorded')
                        else:
                            if tokens[0].ruleName == "EOS":
                                eos_reached = True
                                error_stack.clear()
                            else:
                                raise GrammarError('encountering None checkpoint before EOS')
                    else:
                        raise GrammarError('encountering None checkpoint before EOS')
                    self.__current_path.pop()
                # else:
                    # print('❌')
                    # if (option['IF'] == 'EOS'):
                        # print(error_stack.messages())
                if (error_stack.has_errors() and index == G_copy_len - 1) or eos_reached:
                    break
                elif index < G_copy_len - 1:
                    syntax_matched = False
                index += 1
            if not syntax_matched:
                error_stack << f'unexpected occurrence of "{tokens[0].groupValue}"'
        self.__current_path.pop()
        # print(f'returning from __oneof_items called by {caller} with error {error_stack} -> {x}')
        return eos_reached

    def __anyof_items(self, g: dict, tokens: list[Token], caller, x):
        # print(f'__anyof_items called by {caller} -> {x}')
        G_copy = copy.deepcopy(g)
        self.__current_path.append('ANYOF')
        error_stack = ParserError()
        syntax_matched = False
        eos_reached = False

        if len(tokens) == 0:
            error_stack << 'incomplete statement, could not reach end of statement'
        else:
            # print(tokens[0])
            index = 0
            G_copy_len = len(G_copy['ANYOF'])
            while index < G_copy_len:
                option = G_copy['ANYOF'][index]
                # print(index, option['IF'], end=' ')
                if (isinstance(option['IF'], str) and tokens[0].ruleName == option['IF']) \
                    or (isinstance(option['IF'], (tuple, list, set)) and tokens[0].ruleName in option['IF']):
                    # print('✅')
                    
                    G_next = option.get('THEN')
                    if G_next is None:
                        raise GrammarError('expects THEN')

                    syntax_matched = True
                    self.__current_path.append(index)

                    checkpoint = option.get('CHECKPOINT')
                    if checkpoint is not None:
                        self.__checkpoints[checkpoint] = copy.deepcopy(self.__current_path)

                    tokens_next = tokens[1:]
                    if 'ANYOF' in G_next.keys():
                        eos_reached = self.__anyof_items(G_next, tokens_next, '__anyof_items', x+1)
                    elif 'ONEOF' in G_next.keys():
                        eos_reached = self.__oneof_items(G_next, tokens_next, '__anyof_items', x+1)
                    elif 'GOTO' in G_next.keys():
                        goto = G_next['GOTO']
                        if goto is not None:
                            if isinstance(goto, str) and goto in self.__checkpoints.keys():
                                G_next = copy.deepcopy(G)
                                
                                path = self.__checkpoints[goto]
                                for i in path:
                                    G_next = G_next[i]['THEN'] if isinstance(i, int) else G_next[i]
                                
                                if 'ANYOF' in G_next.keys():
                                    eos_reached = self.__anyof_items(G_next, tokens_next, '__anyof_items', x+1)
                                elif 'ONEOF' in G_next.keys():
                                    eos_reached = self.__oneof_items(G_next, tokens_next, '__anyof_items', x+1)
                                else:
                                    raise GrammarError('expects ANYOF or ONEOF')
                            else:
                                raise GrammarError('checkpoint should be a string which have already been recorded')
                        else:
                            if tokens[0].ruleName == "EOS":
                                eos_reached = True
                                error_stack.clear()
                            else:
                                raise GrammarError('encountering None checkpoint before EOS')
                    else:
                        raise GrammarError('expects ANYOF or ONEOF or GOTO')
                    self.__current_path.pop()
                # else:
                    # print('❌')

                if (error_stack.has_errors() and index == G_copy_len - 1) or syntax_matched or eos_reached:
                    break
                elif index < G_copy_len - 1:
                    syntax_matched = False
                index += 1
            if not syntax_matched:
                error_stack << f'unexpected occurrence of "{tokens[0].groupValue}" p'
        self.__current_path.pop()
        # # print(f'returning from __anyof_items called by {caller} with error {error_stack} -> {x}')
        return eos_reached

    def generate_ast(self, tokens: list[Token]):
        eos_reached = self.__anyof_items(G, tokens, 'generate_ast', 0)
        if not eos_reached:
            parser_error = ParserError()
            if parser_error is not None:
                raise ExpressionError(str(parser_error))
        
        


