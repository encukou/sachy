import pyglet

class Figurka:
    def __init__(self, strana, druh):
        self.strana = strana
        self.druh = druh

    def __str__(self):
        """Textový popis figurky"""
        return f'"{self.strana} {self.druh}"'

    def over_tah(self, sachovnice, puvodni_pozice, nova_pozice):
        """Zkontroluje, že se tato figurka může daným způsobem pohnout

        Když tah nejde provést, tahle metoda způsobí ValueError.

        sachovnice: Šachovnice, na které se figurka hýbe
        puvodni_pozice: Pozice (radek, sloupec), na kterém figurka právě je
        nova_pozice: Pozice (radek, sloupec), na které figurka má jít
        """

        # Pokud se figurka nehýbe, nejde o tah
        if puvodni_pozice == nova_pozice:
            raise ValueError('Nehýbe se')

        # Ven z šachovnice se nedá táhnout
        radek, sloupec = nova_pozice
        if radek < 0 or sloupec < 0 or radek >= 8 or sloupec >= 8:
            raise ValueError('Venku z šachovnice')

        # Taky se nedá táhnout na figurku stejné barvy
        figurka = sachovnice.figurka_na(nova_pozice)
        if figurka != None and figurka.strana == self.strana:
            raise ValueError(f'Blokuje {figurka} stejné barvy')

    def tahni(self, sachovnice, puvodni_pozice, nova_pozice):
        sachovnice.tahni(puvodni_pozice, nova_pozice)


class Vez(Figurka):
    def __init__(self, strana):
        super().__init__(strana, 'vez')

    def over_tah(self, sachovnice, puvodni_pozice, nova_pozice):
        super().over_tah(sachovnice, puvodni_pozice, nova_pozice)

        # Rozložení pozic (radek, sloupec) na čísla
        puvodni_radek, puvodni_sloupec = puvodni_pozice
        novy_radek, novy_sloupec = nova_pozice

        if puvodni_radek == novy_radek:
            # Věž se pohybuje "horizontálně", po řádku.
            # Potřebujeme `range` s čísly sloupců, které tím věž přeskočí.
            if puvodni_sloupec < novy_sloupec:
                # věž jde doprava
                preskocene_sloupce = range(puvodni_sloupec+1, novy_sloupec)
            else:
                # věž jde doleva
                preskocene_sloupce = range(novy_sloupec+1, puvodni_sloupec)
            # Na žádném z přeskočených políček nesmí být figurka:
            for sloupec in preskocene_sloupce:
                testovana_pozice = puvodni_radek, sloupec
                blokujici = sachovnice.figurka_na(testovana_pozice)
                if blokujici != None:
                    raise ValueError(f'V cestě je {blokujici}')
        elif puvodni_sloupec == novy_sloupec:
            # Podobně pohyb "vertikálně"
            if puvodni_radek < novy_radek:
                preskocene_radky = range(puvodni_radek+1, novy_radek)
            else:
                preskocene_radky = range(novy_radek+1, puvodni_radek)
            for radek in preskocene_radky:
                testovana_pozice = radek, puvodni_sloupec
                blokujici = sachovnice.figurka_na(testovana_pozice)
                if blokujici != None:
                    raise ValueError(f'V cestě je {blokujici}')
        else:
            raise ValueError(f'Musí se hýbat po řádku nebo sloupci')


class Sachovnice:
    def __init__(self):
        self.vybrana_pozice = None

        self.figurky = {}

        self.pridej((0, 0), Vez('bily'))
        self.pridej((0, 1), Figurka('bily', 'kun'))
        self.pridej((0, 2), Figurka('bily', 'strelec'))
        self.pridej((0, 3), Figurka('bily', 'dama'))
        self.pridej((0, 4), Figurka('bily', 'kral'))
        self.pridej((0, 5), Figurka('bily', 'strelec'))
        self.pridej((0, 6), Figurka('bily', 'kun'))
        self.pridej((0, 7), Vez('bily'))

        self.pridej((1, 0), Figurka('bily', 'pesec'))
        self.pridej((1, 1), Figurka('bily', 'pesec'))
        self.pridej((1, 2), Figurka('bily', 'pesec'))
        self.pridej((1, 3), Figurka('bily', 'pesec'))
        self.pridej((1, 4), Figurka('bily', 'pesec'))
        self.pridej((1, 5), Figurka('bily', 'pesec'))
        self.pridej((1, 6), Figurka('bily', 'pesec'))
        self.pridej((1, 7), Figurka('bily', 'pesec'))

        self.pridej((6, 0), Figurka('cerny', 'pesec'))
        self.pridej((6, 1), Figurka('cerny', 'pesec'))
        self.pridej((6, 2), Figurka('cerny', 'pesec'))
        self.pridej((6, 3), Figurka('cerny', 'pesec'))
        self.pridej((6, 4), Figurka('cerny', 'pesec'))
        self.pridej((6, 5), Figurka('cerny', 'pesec'))
        self.pridej((6, 6), Figurka('cerny', 'pesec'))
        self.pridej((6, 7), Figurka('cerny', 'pesec'))

        self.pridej((7, 0), Vez('cerny'))
        self.pridej((7, 1), Figurka('cerny', 'kun'))
        self.pridej((7, 2), Figurka('cerny', 'strelec'))
        self.pridej((7, 3), Figurka('cerny', 'dama'))
        self.pridej((7, 4), Figurka('cerny', 'kral'))
        self.pridej((7, 5), Figurka('cerny', 'strelec'))
        self.pridej((7, 6), Figurka('cerny', 'kun'))
        self.pridej((7, 7), Vez('cerny'))

    def figurka_na(self, pozice):
        """Vrátí figurku na daných souřadnicích, nebo None"""
        radek, sloupec = pozice
        return self.figurky.get((radek, sloupec))

    def vrat_vybranou_figurku(self):
        """Vrátí figurku, která je právě vybraná (bude se hýbat)"""
        pozice = self.vybrana_pozice
        if pozice:
            return self.figurka_na(pozice)

    def pridej(self, pozice, figurka):
        """Přidá danou figurku na danou pozici

        Pokud je na cílové pozici jiná figurka, vyhodí ji.
        """
        self.figurky[pozice] = figurka

    def tahni(self, z, na):
        """Přemístí figurku z jedné pozice na druhou.

        Pokud je na cílové pozici jiná figurka, vyhodí ji.
        """
        figurka = self.figurky.pop(z)
        self.pridej(na, figurka)

    def muze_tahnout(self, nova_pozice):
        """Vrátí true, pokud právě vybraná figurka může táhnout na danou pozici
        """
        figurka = self.vrat_vybranou_figurku()
        if figurka == None:
            return False
        else:
            try:
                figurka.over_tah(self, self.vybrana_pozice, nova_pozice)
            except ValueError:
                return False
            else:
                return True

    def vyber_pozici(self, pozice):
        """Vybere figurku na dané pozici"""

        figurka = self.figurka_na(pozice)
        if figurka:
            self.vybrana_pozice = pozice
        else:
            self.vybrana_pozice = None

    def tahni_na_pozici(self, pozice):
        """Táhne vybranou figurkou na danou pozici"""

        if self.vybrana_pozice == None:
            return

        popis_z = popis_pozici(self.vybrana_pozice)
        popis_na = popis_pozici(pozice)

        figurka = self.figurka_na(self.vybrana_pozice)
        try:
            figurka.over_tah(self, self.vybrana_pozice, pozice)
        except ValueError as chyba:
            print(f'{figurka} nemůže na z {popis_z} na {popis_na}: {chyba}!')
        else:
            print(f'{figurka} jde z {popis_z} na {popis_na}!')
            figurka.tahni(self, self.vybrana_pozice, pozice)
        self.vybrana_pozice = None

    def vykresli_se(self):
        """Vykreslí šachovnici do Pyglet okýnka"""

        # Pozadí - střídavá políčka
        for radek in range(8):
            for sloupec in range(8):
                if (radek + sloupec) % 2 == 1:
                    kresli_obrazek('pole', radek, sloupec)
                else:
                    kresli_obrazek('pole2', radek, sloupec)

                # Označení možných tahů
                if self.vybrana_pozice:
                    kreslena_pozice = (radek, sloupec)
                    figurka = self.figurka_na(self.vybrana_pozice)
                    try:
                        figurka.over_tah(
                            self,
                            self.vybrana_pozice,
                            kreslena_pozice,
                        )
                    except ValueError as chyba:
                        pass
                    else:
                        kresli_obrazek('muze', radek, sloupec)

        # Figurky
        for (radek, sloupec), figurka in self.figurky.items():
            kresli_obrazek(f'{figurka.strana}_{figurka.druh}', radek, sloupec)

        # Výběr
        if self.vybrana_pozice:
            radek, sloupec = self.vybrana_pozice
            kresli_obrazek('vyber', radek, sloupec)


def popis_pozici(pozice):
    """Popíše pozici pro lidi

    např:

    >>> popis_pozici(0, 0)
    'a1'

    """
    radek, sloupec = pozice
    return "abcdefgh"[sloupec] + "12345678"[radek]


okno = pyglet.window.Window(width=360, height=360, resizable=True)
sachovnice = Sachovnice()
pozice_mysi = [0, 0]

obrazky = {}

def kresli_obrazek(jmeno, radek, sloupec):
    """Nakreslí obrázek na danou pozici"""

    # Načtené obrázky ukládáme ve slovníku "obrazky",
    # aby se nemusely načítat víckrát
    try:
        obrazek = obrazky[jmeno]
    except KeyError:
        # Když ještě obrázek ve slovníku není, načíst a uložit
        obrazek = pyglet.image.load(f"{jmeno}.png")
        obrazky[jmeno] = obrazek

    # Vykreslení obrázku
    velikost = min(okno.width, okno.height) / 8
    obrazek.blit(
        sloupec * velikost, radek * velikost,
        width=velikost, height=velikost,
    )

@okno.event
def on_draw():
    """Vykreslí obsah okna"""

    okno.clear()
    # Lepší vykreslování (pro nás zatím kouzelné zaříkadlo)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(
        pyglet.gl.GL_SRC_ALPHA,
        pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
    )

    sachovnice.vykresli_se()

    # Vykreslení "stínu" figurky, která se hýbe
    radek, sloupec = pozice_mysi
    figurka = sachovnice.vrat_vybranou_figurku()
    if figurka:
        pyglet.gl.glColor4f(1, 1, 1, 0.5)
        kresli_obrazek(f'{figurka.strana}_{figurka.druh}', radek, sloupec)
        pyglet.gl.glColor4f(1, 1, 1, 1)
        if sachovnice.muze_tahnout(pozice_mysi):
            kresli_obrazek('muze', radek, sloupec)
        else:
            kresli_obrazek('nemuze', radek, sloupec)


def pozice_na_souradnicich(x, y):
    """Vrátí pozici (radek, sloupec) na pixelových souřadnicích (x, y)"""
    velikost = min(okno.width, okno.height) / 8
    sloupec = int(x / velikost)
    radek = int(y / velikost)
    return radek, sloupec

@okno.event
def on_mouse_press(x, y, tlacitko, mod):
    """Zpracuje zmáčknutí tlačítka myši"""
    pozice = pozice_na_souradnicich(x, y)
    sachovnice.vyber_pozici(pozice)
    pozice_mysi[:] = pozice_na_souradnicich(x, y)

@okno.event
def on_mouse_release(x, y, tlacitko, mod):
    """Zpracuje puštění tlačítka myši"""
    pozice = pozice_na_souradnicich(x, y)
    sachovnice.tahni_na_pozici(pozice)

@okno.event
def on_mouse_drag(x, y, dx, dy, tlacitko, mod):
    """Zpracuje tažení myší"""
    pozice_mysi[:] = pozice_na_souradnicich(x, y)


pyglet.app.run()
