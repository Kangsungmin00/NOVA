from datetime import datetime, timedelta
from nova_sim.entity import SpatialEntity

class World:
    def __init__(
            self,
            world_id:str,
            start_time:datetime,
            seed:int,
            center_latitude:float,
            center_longitude:float,
            ):
        self.world_id = world_id
        self.current_time = start_time
        self.seed = seed
        self.tick = 0

        self.entities = {}

        self.center_latitude = center_latitude
        self.center_longitude = center_longitude

    def step(self):
        self.tick += 1
        self.current_time += timedelta(minutes=1)

    def get_state(self):
        return{
            "world_center":{
                "latitude":self.center_latitude,
                "longitude":self.center_longitude,
            },
            "world_id":self.world_id,
            "current_time":self.current_time,
            "tick":self.tick,
            "seed":self.seed,
            "entities":[
                entity.get_state()
                for entity in self.entities.values()
            ],
        }

    def add_entity(self, entity:SpatialEntity):
        self.entities[entity.entity_id] = entity
