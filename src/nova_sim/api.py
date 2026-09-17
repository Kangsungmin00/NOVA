from fastapi import FastAPI, HTTPException
from nova_sim.scenario import create_demo_world

app = FastAPI(
    title = "NOVA-SIM API",
    version = "0.1.0",
)

world = create_demo_world()

@app.get("/app/world")
def get_world():
    return world.get_state()

@app.post("/app/world/step")
def step_world(entity_id: str | None = None, direction: str | None = None):
    try:
        world.step(entity_id, direction)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return world.get_state()
