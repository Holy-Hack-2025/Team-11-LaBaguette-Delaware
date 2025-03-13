import constants.py

class TraficLight:
    def __init__(self, route, position, ticks = ):
        """"Initiates a trafic light. Route determines what route the light is on (it between 1 and 6), 
        and position is its position on this route. All trafic lights face the 0-side of a route. 
        All lights start the simulation green
        """
        self.route = route
        self.position = position
        self.state = "GREEN" #can be "GREEN" or "RED"
        self.ticks_since_last_change = 0
        self.ticks_between_changes = ticks
    
    def update(self):
        """determines the next state of the light. In basic implementation, juste based on a chronometer."""
        
