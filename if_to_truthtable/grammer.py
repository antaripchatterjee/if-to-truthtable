G = {
    'IF': 'BOS',
    'CHECKPOINT': 'BOS_CP',
    'THEN': {
        'ANYOF': [
            {
                'IF': 'STMT_ALIAS',
                'THEN': {
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'SYM_CMDARG',
                                        'CHECKPOINT': 'STMT_ALIAS_CP',
                                        'THEN': {
                                            'ANYOF': [
                                                {
                                                    'IF': 'SIGN_OPERATOR',
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': ['BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL'],
                                                                'THEN': {
                                                                    'ONEOF': [
                                                                        {
                                                                            'IF' : 'SYM_COMMA',
                                                                            'THEN': {
                                                                                'GOTO': 'STMT_ALIAS_CP',
                                                                            }
                                                                        },
                                                                        {
                                                                            'IF': 'EOS',
                                                                            'THEN': {
                                                                                'GOTO': 'BOS_CP'
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    'IF': ['BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL', 'STRING_LITERAL', 'RESERVED_LITERAL'],
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF' : 'SYMBOL_COMMA',
                                                                'THEN': {
                                                                    'GOTO': 'STMT_ALIAS_CP',
                                                                }
                                                            },
                                                            {
                                                                'IF': 'EOS',
                                                                'THEN': {
                                                                    'GOTO': 'BOS_CP'
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'IF': 'STMT_BEGIN',
                'THEN': {
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'EOS',
                                        'THEN': {
                                            'GOTO': 'BOS_CP'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'IF': 'STMT_END',
                'THEN': {
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'EOS',
                                        'THEN': {
                                            'GOTO': 'BOS_CP'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'IF': 'STMT_MUT',
                'THEN': {
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'SYM_CMDARG',
                                        'CHECKPOINT': 'STMT_MUT_CP',
                                        'THEN': {
                                            'ANYOF': [
                                                {
                                                    'IF': 'SIGN_OPERATOR',
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': ['BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL'],
                                                                'THEN': {
                                                                    'ONEOF': [
                                                                        {
                                                                            'IF' : 'SYM_COMMA',
                                                                            'THEN': {
                                                                                'GOTO': 'STMT_MUT_CP',
                                                                            }
                                                                        },
                                                                        {
                                                                            'IF': 'EOS',
                                                                            'THEN': {
                                                                                'GOTO': 'BOS_CP'
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    'IF': ['BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL', 'STRING_LITERAL', 'RESERVED_LITERAL'],
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF' : 'SYMBOL_COMMA',
                                                                'THEN': {
                                                                    'GOTO': 'STMT_MUT_CP',
                                                                }
                                                            },
                                                            {
                                                                'IF': 'EOS',
                                                                'THEN': {
                                                                    'GOTO': 'BOS_CP'
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'IF': 'SYM_CMDARG',
                                        'THEN': {
                                            'ANYOF': [
                                                {
                                                    'IF': 'SCRIPT_NOUN',
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': 'EOS',
                                                                'THEN': {
                                                                    'GOTO': 'BOS_CP'
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'IF': 'STMT_CONST',
                'THEN': {
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'SYM_CMDARG',
                                        'THEN': {
                                            'ANYOF': [
                                                {
                                                    'IF': 'SIGN_OPERATOR',
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': ['BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL'],
                                                                'THEN': {
                                                                    'ONEOF': [
                                                                        {
                                                                            'IF': 'EOS',
                                                                            'THEN': {
                                                                                'GOTO': 'BOS_CP'
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    'IF': ['BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL', 'STRING_LITERAL', 'RESERVED_LITERAL'],
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': 'EOS',
                                                                'THEN': {
                                                                    'GOTO': 'BOS_CP'
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'IF': 'STMT_EVAL',
                'THEN': {
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'SYM_CMDARG',
                                        'THEN': {
                                            'ONEOF': [
                                                {
                                                    'IF': 'STRING_LITERAL',
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': 'EOS',
                                                                'THEN': {
                                                                    'GOTO': 'BOS_CP'
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                'IF': 'STMT_EXPR',
                'THEN': {
                    'CONTEXT': {
                        'PARAN_DEPTH': [
                            {
                                'FUNC': 'INIT',
                                'VAL': 0
                            }
                        ]
                    },
                    'ONEOF': [
                        {
                            'IF': 'SCRIPT_NOUN',
                            'THEN': {
                                'ONEOF': [
                                    {
                                        'IF': 'SYM_CMDARG',
                                        'THEN': {
                                            'ONEOF': [
                                                {
                                                    'IF': 'SCRIPT_NOUN',
                                                    'THEN': {
                                                        'ONEOF': [
                                                            {
                                                                'IF': 'SYM_ARROW',
                                                                'CHECKPOINT': 'STMT_EXPR_CP1',
                                                                'THEN': {
                                                                    'ONEOF': [
                                                                        {
                                                                            'IF': ['SIGN_OPERATOR', 'UNARY_OPERATOR'], 
                                                                            'THEN': {
                                                                                'GOTO': 'STMT_EXPR_CP1'
                                                                            }
                                                                        },
                                                                        {
                                                                            'IF': ['IDENTIFIER', 'BINARY_LITERAL', 'OCTAL_LITERAL', 'HEX_LITERAL', 'DECIMAL_LITERAL', 'STRING_LITERAL', 'RESERVED_LITERAL'],
                                                                            'CHECKPOINT': 'STMT_EXPR_CP2',
                                                                            'THEN': {
                                                                                'ONEOF': [
                                                                                    {
                                                                                        'IF': 'BINARY_OPERATOR',
                                                                                        'THEN': {
                                                                                            'GOTO': 'STMT_EXPR_CP1'
                                                                                        }
                                                                                    },
                                                                                    {
                                                                                        'IF': 'CLOSE_PARAN',
                                                                                        'THEN': {
                                                                                            'CONTEXT': {
                                                                                                'PARAN_DEPTH': [
                                                                                                    {
                                                                                                        'FUNC': 'DEC',
                                                                                                        'BY': 1,
                                                                                                    },
                                                                                                    {
                                                                                                        'FUNC': 'VALIDATE',
                                                                                                        'COND': [
                                                                                                            {
                                                                                                                'GE': 0
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            'GOTO': 'STMT_EXPR_CP2'
                                                                                        }
                                                                                    },
                                                                                    {
                                                                                        'IF': 'EOS',
                                                                                        'THEN': {
                                                                                            'CONTEXT': {
                                                                                                'PARAN_DEPTH': [
                                                                                                    {
                                                                                                        'FUNC': 'VALIDATE',
                                                                                                        'COND': [
                                                                                                            {
                                                                                                                'EQ': 0
                                                                                                            }
                                                                                                        ]
                                                                                                    }
                                                                                                ]
                                                                                            },
                                                                                            'GOTO': 'BOS_CP'
                                                                                        }
                                                                                    }
                                                                                ]
                                                                            }
                                                                        },
                                                                        {
                                                                            'IF': 'OPEN_PARAN',
                                                                            'THEN': {
                                                                                'CONTEXT': {
                                                                                    'PARAN_DEPTH': [
                                                                                        {
                                                                                            'FUNC': 'INC',
                                                                                            'BY': 1
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                'GOTO': 'STMT_EXPR_CP1'
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
        ]
    }
}