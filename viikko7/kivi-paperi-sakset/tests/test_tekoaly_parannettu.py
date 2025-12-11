import pytest
from tekoaly_parannettu import TekoalyParannettu


class TestTekoalyParannettu:
    def test_initialization(self):
        ai = TekoalyParannettu(10)
        assert len(ai._muisti) == 10
        assert ai._vapaa_muisti_indeksi == 0

    def test_first_move_is_rock(self):
        ai = TekoalyParannettu(10)
        assert ai.anna_siirto() == "k"

    def test_second_move_is_rock(self):
        ai = TekoalyParannettu(10)
        ai.aseta_siirto("k")
        assert ai.anna_siirto() == "k"

    def test_aseta_siirto_stores_move(self):
        ai = TekoalyParannettu(3)
        ai.aseta_siirto("k")
        assert ai._muisti[0] == "k"
        assert ai._vapaa_muisti_indeksi == 1
        ai.aseta_siirto("p")
        assert ai._muisti[1] == "p"
        assert ai._vapaa_muisti_indeksi == 2

    def test_memory_overflow(self):
        ai = TekoalyParannettu(3)
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")
        assert ai._muisti[0] == "p"
        assert ai._muisti[1] == "s"
        assert ai._muisti[2] == "k"

    def test_returns_paper_when_rock_most_common(self):
        ai = TekoalyParannettu(10)
        ai.aseta_siirto("k")
        ai.aseta_siirto("k")
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        move = ai.anna_siirto()
        assert move == "p"

    def test_returns_scissors_when_paper_most_common(self):
        ai = TekoalyParannettu(10)
        ai.aseta_siirto("p")
        ai.aseta_siirto("p")
        ai.aseta_siirto("p")
        ai.aseta_siirto("k")
        move = ai.anna_siirto()
        assert move == "s"

    def test_returns_rock_when_scissors_most_common(self):
        ai = TekoalyParannettu(10)
        ai.aseta_siirto("s")
        ai.aseta_siirto("s")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")
        move = ai.anna_siirto()
        assert move == "k"

    def test_returns_valid_move(self):
        ai = TekoalyParannettu(5)
        for move in ["k", "p", "s", "k", "p", "s"]:
            ai.aseta_siirto(move)
            result = ai.anna_siirto()
            assert result in ["k", "p", "s"]
