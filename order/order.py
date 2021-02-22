class Order:
    pass


class SwiftMove(Order):
    def __init__(self, dxdy):
        self.dxdy = dxdy


class AttackOrder(Order):
    def __init__(self, attack_dxdy, target=None):
        self.attack_dxdy = attack_dxdy
        self.target = target
