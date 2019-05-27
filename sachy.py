import pyglet

class Figurka:
    def __init__(self, strana, druh):
        self.strana = strana
        self.druh = druh

    def muze_tahnout(self, sachovnice, puvodni_pole, nove_pole):
        radek, sloupec = nove_pole
        if radek < 0 or sloupec < 0 or radek >= 8 or sloupec >= 8:
            print('Venku z šachovnice!')
            return False

        figurka = sachovnice.vrat_figurku(nove_pole)
        if figurka and figurka.strana == self.strana:
            print('Blokováno!')
            return False

        return True

    def tahni(self, sachovnice, puvodni_pole, nove_pole):
        sachovnice.tahni(puvodni_pole, nove_pole)


class Sachovnice:
    def __init__(self):
        self.vybrana_pozice = None

        self.figurky = {}

        self.pridej((0, 0), Figurka('bily', 'vez'))
        self.pridej((0, 1), Figurka('bily', 'kun'))
        self.pridej((0, 2), Figurka('bily', 'strelec'))
        self.pridej((0, 3), Figurka('bily', 'dama'))
        self.pridej((0, 4), Figurka('bily', 'kral'))
        self.pridej((0, 5), Figurka('bily', 'strelec'))
        self.pridej((0, 6), Figurka('bily', 'kun'))
        self.pridej((0, 7), Figurka('bily', 'vez'))

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

        self.pridej((7, 0), Figurka('cerny', 'vez'))
        self.pridej((7, 1), Figurka('cerny', 'kun'))
        self.pridej((7, 2), Figurka('cerny', 'strelec'))
        self.pridej((7, 3), Figurka('cerny', 'dama'))
        self.pridej((7, 4), Figurka('cerny', 'kral'))
        self.pridej((7, 5), Figurka('cerny', 'strelec'))
        self.pridej((7, 6), Figurka('cerny', 'kun'))
        self.pridej((7, 7), Figurka('cerny', 'vez'))

    def vrat_figurku(self, pozice):
        radek, sloupec = pozice
        return self.figurky.get((radek, sloupec))

    def vrat_vybranou_figurku(self):
        pozice = self.vybrana_pozice
        if pozice:
            return self.vrat_figurku(pozice)

    def tahni(self, z, na):
        figurka = self.figurky.pop(z)
        self.pridej(na, figurka)

    def pridej(self, pozice, figurka):
        self.figurky[pozice] = figurka

    def klik(self, pozice):
        """Zpracuje kliknutí na dané políčko"""

        if self.vybrana_pozice:
            figurka = self.vrat_figurku(self.vybrana_pozice)
            if figurka and figurka.muze_tahnout(
                self, self.vybrana_pozice, pozice
            ):
                popis_z = popis_pozici(self.vybrana_pozice)
                popis_na = popis_pozici(pozice)
                print(f'{figurka} jde z {popis_z} na {popis_na}!')
                figurka.tahni(self, self.vybrana_pozice, pozice)
            else:
                print(f'Tam {figurka} nemůže táhnout!')
            self.vybrana_pozice = None
        else:
            figurka = self.vrat_figurku(pozice)
            if figurka:
                sachovnice.vybrana_pozice = pozice

    def vykresli_se(self):
        """Vykreslí šachovnici do Pyglet okýnka"""

        # Pozadí - střídavá políčka
        for radek in range(8):
            for sloupec in range(8):
                if (radek + sloupec) % 2 == 1:
                    kresli_obrazek('pole', radek, sloupec)
                else:
                    kresli_obrazek('pole2', radek, sloupec)

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

    pyglet.gl.glColor4f(1, 1, 1, 0.5)
    figurka = sachovnice.vrat_vybranou_figurku()
    if figurka:
        radek, sloupec = pozice_mysi
        kresli_obrazek(f'{figurka.strana}_{figurka.druh}', radek, sloupec)
        kresli_obrazek('vyber', radek, sloupec)
    pyglet.gl.glColor4f(1, 1, 1, 1)


def pozice_na_souradnicich(x, y):
    velikost = min(okno.width, okno.height) / 8
    sloupec = int(x / velikost)
    radek = int(y / velikost)
    return radek, sloupec

@okno.event
def on_mouse_press(x, y, tlacitko, mod):
    """Zpracuje zmáčknutí tlačítka myši"""
    pozice = pozice_na_souradnicich(x, y)
    sachovnice.klik(pozice)
    pozice_mysi[:] = pozice_na_souradnicich(x, y)

@okno.event
def on_mouse_release(x, y, tlacitko, mod):
    """Zpracuje puštění tlačítka myši"""
    pozice = pozice_na_souradnicich(x, y)
    sachovnice.klik(pozice)

@okno.event
def on_mouse_drag(x, y, dx, dy, tlacitko, mod):
    """Zpracuje tažení myší"""
    pozice_mysi[:] = pozice_na_souradnicich(x, y)


pyglet.app.run()
