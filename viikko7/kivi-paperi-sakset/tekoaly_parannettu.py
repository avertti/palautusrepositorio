# Improved AI that remembers player moves
class TekoalyParannettu:
    def __init__(self, muistin_koko):
        self._muisti = [None] * muistin_koko
        self._vapaa_muisti_indeksi = 0

    def aseta_siirto(self, siirto):
        if self._vapaa_muisti_indeksi < len(self._muisti):
            self._muisti[self._vapaa_muisti_indeksi] = siirto
            self._vapaa_muisti_indeksi += 1
        else:
            # Muisti täynnä, unohdetaan vanhin
            for i in range(0, len(self._muisti) - 1):
                self._muisti[i] = self._muisti[i + 1]
            self._muisti[len(self._muisti) - 1] = siirto

    def anna_siirto(self):
        if self._vapaa_muisti_indeksi == 0 or self._vapaa_muisti_indeksi == 1:
            return "k"

        viimeisin_siirto = self._muisti[self._vapaa_muisti_indeksi - 1]

        k = 0
        p = 0
        s = 0

        for i in range(0, self._vapaa_muisti_indeksi - 1):
            if self._muisti[i] == "k":
                k += 1
            elif self._muisti[i] == "p":
                p += 1
            else:
                s += 1

        # Tehdään siirto historiaan perustuen
        # - jos kiviä eniten, annetaan aina paperi
        # - jos papereita eniten, annetaan aina sakset
        # muulloin annetaan aina kivi
        if k > p and k > s:
            return "p"
        elif p > k and p > s:
            return "s"
        else:
            return "k"
