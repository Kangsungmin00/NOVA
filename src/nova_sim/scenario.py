from datetime import datetime
from nova_sim.entity import SpatialEntity
from nova_sim.world import World

def create_demo_world() -> World:
    world = World(
        world_id="NOVA_WORLD_001",
        start_time=datetime(2026, 1, 1, 0, 0),
        seed=42,
        center_latitude=37.5665,
        center_longitude=126.9780,
    )

    world.add_entity(
        SpatialEntity(
            entity_id="agent_001",
            entity_type="agent",
            latitude=37.5700,
            longitude=126.9850,
        )
    )

    world.add_entity(
        SpatialEntity(
            entity_id="vehicle_001",
            entity_type="vehicle",
            latitude=37.5665,
            longitude=126.9780,
        )
    )
    return world