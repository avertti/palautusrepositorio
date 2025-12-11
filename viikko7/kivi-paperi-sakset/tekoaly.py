import random


# Simple AI that plays randomly
class Tekoaly:
    def __init__(self):
        self._siirto = 0

    def anna_siirto(self):
        siirto = random.randint(0, 2)

        if siirto == 0:
            return "k"
        elif siirto == 1:
            return "p"
        else:
            return "s"

    def aseta_siirto(self, siirto):
        # Ei tehdä mitään
        pass
