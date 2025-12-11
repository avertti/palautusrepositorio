import pytest
from tuomari import Tuomari


class TestTuomari:
    def test_initial_scores(self):
        tuomari = Tuomari()
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0

    def test_tasapeli_detection(self):
        tuomari = Tuomari()
        assert tuomari._tasapeli("k", "k") == True
        assert tuomari._tasapeli("p", "p") == True
        assert tuomari._tasapeli("s", "s") == True
        assert tuomari._tasapeli("k", "p") == False

    def test_eka_voittaa_rock_beats_scissors(self):
        tuomari = Tuomari()
        assert tuomari._eka_voittaa("k", "s") == True
        assert tuomari._eka_voittaa("s", "k") == False

    def test_eka_voittaa_scissors_beats_paper(self):
        tuomari = Tuomari()
        assert tuomari._eka_voittaa("s", "p") == True
        assert tuomari._eka_voittaa("p", "s") == False

    def test_eka_voittaa_paper_beats_rock(self):
        tuomari = Tuomari()
        assert tuomari._eka_voittaa("p", "k") == True
        assert tuomari._eka_voittaa("k", "p") == False

    def test_kirjaa_siirto_tasapeli(self):
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "k")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 1

    def test_kirjaa_siirto_eka_voittaa(self):
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0

    def test_kirjaa_siirto_toka_voittaa(self):
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("s", "k")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
        assert tuomari.tasapelit == 0

    def test_multiple_rounds(self):
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        tuomari.kirjaa_siirto("p", "s")
        tuomari.kirjaa_siirto("k", "k")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 1
        assert tuomari.tasapelit == 1

    def test_str_representation(self):
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        result = str(tuomari)
        assert "Pelaaja 1: 1" in result
        assert "Pelaaja 2: 0" in result
        assert "Tasapelit: 0" in result
