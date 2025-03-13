import Car

class Route:
    def __init__(self, id, length, trafic_light = null, cars = []):
        self.id = id
        self.length = length
        self.cars = cars
        self.trafic_light = trafic_light
    
    def add_car(self, reaction_time, is_driving = True, position = 0):
        new_car = Car(route = self, reaction_time, is_driving, position)
        self.cars.append(new_car)
    
    def add_trafic_light
   
    
    