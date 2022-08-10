class Handler(object):
    def __init__(self):
        self.nextHandler = None

    def handle(self, request):
        self.nextHandler.handle(request)
