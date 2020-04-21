class Controller:

    class __Controller:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        if not Controller.instance:
            Controller.instance = Controller.__Controller(arg)
        else:
            Controller.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)
   