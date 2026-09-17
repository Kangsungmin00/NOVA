from dataclasses import dataclass

DIRECTIONS = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0),
}

@dataclass
class SpatialEntity:
    entity_id:str
    entity_type:str

    x: int = 0
    y: int = 0

    def move(self, direction:str):
        if direction not in DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")

        dx, dy = DIRECTIONS[direction]
        self.x += dx
        self.y += dy

    def get_state(self):
        return{
            "entity_id":self.entity_id,
            "entity_type":self.entity_type,
            "x":self.x,
            "y":self.y,
        }
