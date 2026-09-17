from nicegui import ui

from nova_sim.renderer import render_grid
from nova_sim.scenario import create_demo_world


world = create_demo_world()
SELECTED_ENTITY_ID = "agent_001"


@ui.page("/")
def main() -> None:
    initial_state = world.get_state()

    def refresh(state: dict) -> None:
        current_time = state["current_time"]
        tick_label.set_text(f'Tick: {state["tick"]}')
        time_label.set_text(
            f'Simulation Time: {current_time.strftime("%Y-%m-%d %H:%M:%S")}'
        )

        selected_entity = next(
            entity
            for entity in state["entities"]
            if entity["entity_id"] == SELECTED_ENTITY_ID
        )
        entity_id_label.set_text(f'ID: {selected_entity["entity_id"]}')
        entity_type_label.set_text(f'Type: {selected_entity["entity_type"]}')
        position_label.set_text(
            f'Position: ({selected_entity["x"]}, {selected_entity["y"]})'
        )
        render_grid(
            grid_container,
            state["entities"],
            width=state["grid_width"],
            height=state["grid_height"],
        )

    def move(direction: str) -> None:
        try:
            world.step(SELECTED_ENTITY_ID, direction)
        except ValueError as error:
            ui.notify(str(error), type="warning")
            return

        refresh(world.get_state())

    ui.label("NOVA-SIM").classes("text-2xl font-bold")

    with ui.row().classes("gap-8"):
        tick_label = ui.label()
        time_label = ui.label()

    with ui.card():
        ui.label("SIMULATION GRID").classes("text-lg font-bold")
        grid_container = ui.column().classes("gap-0")

    with ui.card().classes("w-72"):
        ui.label("Agent").classes("text-lg font-bold")
        entity_id_label = ui.label()
        entity_type_label = ui.label()
        position_label = ui.label()

    with ui.column().classes("items-center"):
        ui.button("↑", on_click=lambda: move("N"))
        with ui.row():
            ui.button("←", on_click=lambda: move("W"))
            ui.button("↓", on_click=lambda: move("S"))
            ui.button("→", on_click=lambda: move("E"))

    refresh(initial_state)


ui.run(title="NOVA-SIM Observer")
