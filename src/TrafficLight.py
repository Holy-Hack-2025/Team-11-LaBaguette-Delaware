import constants

class TrafficLight:
    def __init__(self, route, position, initial_state = "GREEN", ticks = constants.DEFAULT_TRAFFIC_LIGHT_DURATION*constants.TICKS_PER_SECOND):
        """"Initiates a traffic light. Route determines what route the light is on (Route class), 
        and position is its position on this route. All traffic lights face the 0-side of a route. 
        All lights start the simulation green
        """
        self.route = route
        self.position = position
        self.state = "GREEN" #can be "GREEN" or "RED"
        self.ticks_since_last_change = 0
        self.ticks_between_changes = ticks
    
    def get_position(self):
        return self.position
    
    def update(self):
        """determines the next state of the light. In basic implementation, juste based on a chronometer."""
        if self.ticks_since_last_change == self.ticks_between_changes:
            self.toggle_state()

    def toggle_state(self):
        if self.state == "GREEN":
            self.state = "RED"
        else:
            self.state = "GREEN"
        self.ticks_since_last_change = 0

    