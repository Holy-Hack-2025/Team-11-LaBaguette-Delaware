import Car
import TrafficLight
 
class Route:
    def __init__(self, id, length, cars = []):
        self.id = id
        self.length = length
        self.cars = cars
        self.traffic_light = None
    
    def add_car(self, reaction_time, is_driving = True, position = 0):
        new_car = Car(self, reaction_time, is_driving, position)
        self.cars.append(new_car)
    
    def add_traffic_light(self, position):
        self.traffic_light = TrafficLight(self, position)
     
    def update(self):
        """Updates positions of all cars and states of all traffic lights"""
        for car in self.cars:
            car.update()
        if self.traffic_light != None:
            self.traffic_light.update()