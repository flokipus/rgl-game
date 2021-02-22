class BaseState:
    def update(self, gobj):
        pass

    def handle_order(self, gobj, order):
        pass

    def enter(self, gobj):
        pass

    def exit(self, gobj):
        pass
