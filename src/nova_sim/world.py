from datetime import datetime, timedelta
from nova_sim.entity import DIRECTIONS, SpatialEntity


class World:
    def __init__(
            self,
            world_id:str,
            start_time:datetime,
            seed:int,
            grid_width: int = 5,
            grid_height: int = 5,
            ):
        self.world_id = world_id
        self.current_time = start_time
        self.seed = seed
        self.tick = 0

        self.entities = {}

        self.grid_width = grid_width
        self.grid_height = grid_height

    def step(
            self,
            entity_id: str | None = None,
            direction: str | None = None,
            ) -> None:
        if (entity_id is None) != (direction is None):
            raise ValueError("entity_id and direction must be provided together")

        if entity_id is not None:
            target_entity = self.entities[entity_id]
            dx, dy = DIRECTIONS[direction]
            next_x = target_entity.x + dx
            next_y = target_entity.y + dy
            if not (0 <= next_x < self.grid_width and 0 <= next_y < self.grid_height):
                raise ValueError("Cannot move outside the simulation grid")
            target_entity.move(direction)

        self.tick += 1
        self.current_time += timedelta(minutes=1)

    def get_state(self):
        return{
            "world_id":self.world_id,
            "current_time":self.current_time,
            "tick":self.tick,
            "seed":self.seed,
            "grid_width": self.grid_width,
            "grid_height": self.grid_height,
            "entities":[
                entity.get_state()
                for entity in self.entities.values()
            ],
        }

    def add_entity(self, entity:SpatialEntity):
        self.entities[entity.entity_id] = entity
