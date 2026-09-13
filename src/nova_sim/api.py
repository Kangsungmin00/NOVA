from datetime import datetime
from fastapi import FastAPI
from nova_sim.world import World

app = FastAPI(
    title = "NOVA-SIM API",
    version = "0.1.0",
)

world = World(
    world_id = "NOVA_WORLD_001",
    start_time=datetime(2026,1,1,0,0),
    seed = 42,
)

@app.get("/app/world")
def get_world():
    return world.get_state()

@app.post("/app/world/step")
def step_world():
    world.step()
    return world.get_state()