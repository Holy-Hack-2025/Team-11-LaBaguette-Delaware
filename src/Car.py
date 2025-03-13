import constants.py



class Car:

    def __init__(self, route, reaction_time, is_driving = True, position=0):
        """"Initiates a car. Will be on one of the routes(Route object from intersection's routes), 
        and position is its position on this route. Reaction_time is the number of ticks 
        it takes the car to start.
        """
        self.route = route #Route object
        self.position = position
        self.reaction_time = reaction_time
        self.is_driving = is_driving
        self.waiting_time = 0
        self.reaction_time_countdown  = 0
        self.is_done_driving = False

    # Traffic Light State can be "GREEN" or "RED"
    def update(self, traffic_light_state, andere_autos):
        if stopped_car_in_front() or red_light_ahead(): # if obstacle ahead 
            self.isdriving = False
        else:
            if self.isdriving: pass #if car is already driving, do nothing
            else: # if car was stopped and can start, start a reaction time countdown, and when it reaches self.reaction_time, start the car
                if self.reaction_time_countdown == self.reaction_time:
                    self.is_driving = True
                    self.reaction_time = 0
                else: 
                    self.reaction_time_countdown += 1
        if self.isdriving: #update positie, check als einde van de route bereikt is
            if self.position + CAR_SPEED > self.route.length:
                self.is_done_driving = True
            else: 
                self.position += CAR_SPEED
    
    def red_light_ahead(self):
        red_light_position = self.route.trafic_light.position
        if self.position <= 1.5*CAR_LENGTH:
            if self.route.trafic_light.state == "RED":
                return True
        return False
        
    
    
    
    def stopped_car_in_front(self):
        cars = self.route.cars
        for car in cars:
            if car.position != self.position:
                if car.positie <= self.position + 1.5*CAR_LENGTH:
                    if not car.is_driving:
                        return True
        return False