from dataclasses import dataclass

@dataclass
class SpatialEntity:
    entity_id:str
    entity_type:str
    latitude: float
    longitude: float

    def get_state(self):
        return{
            "entity_id":self.entity_id,
            "entity_type":self.entity_type,
            "latitude":self.latitude,
            "longitude":self.longitude,
        }