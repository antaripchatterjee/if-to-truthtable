
class ScriptContext:
    __instance = None

    def __new__(cls, *argv, **kwargv):
        if cls.__instance is None:
            cls.__instance = super(ScriptContext, cls).__new__(cls, *argv, **kwargv)
        return cls.__instance
    