# Welke inputs en methoden moet dit hebben?
class Car:

    def __init__(self, route, positie=0):
        self.route = route
        self.positie = positie

    # Wat moet dit kunnen?
    def update(self):
        return 0

    # De geplande weg die de auto zal volgen
    # Dit kan een lijst van coordinaten of richtingen zijn
    # bijvoorbeeld ["rechtdoor", "links", "rechts"]
    # input: list van posities of richtingen
    def route (richtingen):
        return 0

    # De huidige positie op de weg, bijvoorbeeld als een coordinaat (x, y)
    def get_positie():
        return 0

    # De snelheid waarmee de auto zich voortbeweegt
    # Dit kan variabel zijn, afhankelijk van verkeerslichten en andere auto's
    def snelheid(snelheid):
        return 0
    
    # Hoe lang de auto stilstaat bij een rood licht of verkeersopstopping
    def wachttijd(tijd):
        return 0

    # Waar de auto uiteindelijk naartoe moet
    def bestemming(tuple of string)
