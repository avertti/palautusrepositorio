import pytest
from tekoaly import Tekoaly


class TestTekoaly:
    def test_tekoaly_returns_valid_move(self):
        ai = Tekoaly()
        for _ in range(20):
            move = ai.anna_siirto()
            assert move in ["k", "p", "s"]

    def test_tekoaly_aseta_siirto(self):
        ai = Tekoaly()
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("s")

    def test_tekoaly_initialization(self):
        ai = Tekoaly()
        assert ai._siirto == 0
