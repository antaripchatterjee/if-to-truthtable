import copy
from enum import Enum
from typing import Union

from .error import ExpressionError
from .grammer import G
from .token import Token
from .context import ScriptContext


class Parser(object):
    def __init__(self):
        self.__ctx = ScriptContext()
        self.__current_path = list()
        self.__checkpoints = dict()

    def __oneof_items(self, g: dict, tokens: list[Token]):
        G_copy = copy.deepcopy(g)
        self.__current_path.append('ONEOF')
        error_message = None
        syntax_matched = False
        eos_reached = False

        if len(tokens) == 0:
            error_message = 'Incomplete statement, could not reach end of statement'
        else:
            index = 0
            G_copy_len = len(G_copy['ONEOF'])
            while index < G_copy_len:
                option = G_copy['ONEOF'][index]
                if (isinstance(option['IF'], str) and tokens[0].ruleName == option['IF']) \
                    or (isinstance(option['IF'], (tuple, list, set)) and tokens[0].ruleName in option['IF']):
                    
                    if syntax_matched:
                        error_message = 'Ambiguous syntax, multiple matching pattern'
                        break

                    syntax_matched = True
                    
                    self.__current_path.append(index)

                    checkpoint = option.get('CHECKPOINT')
                    if checkpoint is not None:
                        self.__checkpoints[checkpoint] = copy.deepcopy(self.__current_path)
                    
                    G_next = option['THEN'] # not having 'THEN' is grammer error
                    tokens_next = tokens[1:]

                    if 'ANYOF' in G_next.keys():
                        error_message, eos_reached = self.__anyof_items(G_next, tokens_next)
                    elif 'ONEOF' in G_next.keys():
                        error_message, eos_reached = self.__oneof_items(G_next, tokens_next)
                    elif 'GOTO' in G_next.keys():
                        goto = G_next['GOTO']
                        if goto is not None:
                            if isinstance(goto, str) and goto in self.__checkpoints.keys():
                                G_next = copy.deepcopy(G)
                                
                                path = self.__checkpoints[goto]
                                for i in path:
                                    G_next = G_next[i]['THEN'] if isinstance(i, int) else G_next[i]
                                
                                if 'ANYOF' in G_next.keys():
                                    error_message, eos_reached = self.__anyof_items(G_next, tokens_next)
                                elif 'ONEOF' in G_next.keys():
                                    error_message, eos_reached = self.__oneof_items(G_next, tokens_next)
                                else:
                                    error_message = 'GrammerError, checkpoint lacks ANYOF or ONEOF'
                            else:
                                error_message = 'GrammerError, checkpoint should be a string which have been recorded'
                        else:
                            if tokens[0].ruleName == "EOS":
                                eos_reached = True
                                error_message = None
                            else:
                                error_message = 'GrammerError, incomplete grammer'
                    else:
                        error_message = 'GrammerError, invalid grammer, expects ANYOF or ONEOF or GOTO'
                    self.__current_path.pop()

                if (error_message is not None and index == G_copy_len - 1) or eos_reached:
                    break
                elif index < G_copy_len - 1:
                    syntax_matched = False
                index += 1
            print(86, error_message, tokens[0])
            if not syntax_matched and error_message is None:
                error_message = f'syntax error found "{tokens[0].groupValue}" 8'
        self.__current_path.pop()
        return error_message, eos_reached

    def __anyof_items(self, g: dict, tokens: list[Token]):
        G_copy = copy.deepcopy(g)
        self.__current_path.append('ANYOF')
        error_message = None
        syntax_matched = False
        eos_reached = False

        if len(tokens) == 0:
            error_message = 'Incomplete statement, could not reach end of statement'
        else:
            index = 0
            G_copy_len = len(G_copy['ANYOF'])
            while index < G_copy_len:
                option = G_copy['ANYOF'][index]
                if (isinstance(option['IF'], str) and tokens[0].ruleName == option['IF']) \
                    or (isinstance(option['IF'], (tuple, list, set)) and tokens[0].ruleName in option['IF']):
                    
                    syntax_matched = True
                    self.__current_path.append(index)

                    checkpoint = option.get('CHECKPOINT')
                    if checkpoint is not None:
                        self.__checkpoints[checkpoint] = copy.deepcopy(self.__current_path)
                    
                    G_next = option['THEN'] # not having 'THEN' is grammer error
                    tokens_next = tokens[1:]

                    if 'ANYOF' in G_next.keys():
                        error_message, eos_reached = self.__anyof_items(G_next, tokens_next)
                    elif 'ONEOF' in G_next.keys():
                        error_message, eos_reached = self.__oneof_items(G_next, tokens_next)
                    elif 'GOTO' in G_next.keys():
                        goto = G_next['GOTO']
                        if goto is not None:
                            if isinstance(goto, str) and goto in self.__checkpoints.keys():
                                G_next = copy.deepcopy(G)
                                
                                path = self.__checkpoints[goto]
                                for i in path:
                                    G_next = G_next[i]['THEN'] if isinstance(i, int) else G_next[i]
                                
                                if 'ANYOF' in G_next.keys():
                                    error_message, eos_reached = self.__anyof_items(G_next, tokens_next)
                                elif 'ONEOF' in G_next.keys():
                                    error_message, eos_reached = self.__oneof_items(G_next, tokens_next)
                                else:
                                    error_message = 'GrammerError, checkpoint lacks ANYOF or ONEOF'
                            else:
                                error_message = 'GrammerError, checkpoint should be a string which have been recorded'
                        else:
                            if tokens[0].ruleName == "EOS":
                                eos_reached = True
                                error_message = None
                            else:
                                error_message = 'GrammerError, incomplete grammer'
                    else:
                        error_message = 'GrammerError, invalid grammer, expects ANYOF or ONEOF or GOTO'
                    self.__current_path.pop()

                if (error_message is not None and index == G_copy_len - 1) or syntax_matched or eos_reached:
                    break
                elif index < G_copy_len - 1:
                    syntax_matched = False
                index += 1
            print(156, error_message, tokens[0])
            if not syntax_matched and error_message is None:
                error_message = f'syntax error found "{tokens[0].groupValue}" 7'
        self.__current_path.pop()
        return error_message, eos_reached

    def generate_ast(self, tokens: list[Token]):
        error_message, _ = self.__anyof_items(G, tokens)
        if error_message is not None:
            raise ExpressionError(error_message)
        


