import Route

class Intersection:
    def __init__(self, routes = []):
        """Initiates the intersection with the chosen layout"""
        self.routes = routes
        
    def add_route(self, id, length, traffic_light_position, cars_on_start):
        route = Route(id, length, cars_on_start)
        route.add_traffic_light(traffic_light_position)
        self.routes.append(route)
    
    def add_car_to_route(self, route, reaction_time, is_driving = True, position = 0):
        route.add_car(reaction_time, is_driving, position)
    
    
    def update_intersection_state(self):
        """Updates positions of all cars and states of all traffic lights"""
        for route in self.routes:
            route.update()
