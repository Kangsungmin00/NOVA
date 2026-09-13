from nicegui import ui

from nova_sim.renderer import render_entity
from nova_sim.scenario import create_demo_world


world = create_demo_world()


@ui.page('/')
async def main():

    event_logs = []

    # Observer 최초 실행 시점의 World 상태
    initial_state = world.get_state()

    # --------------------------------
    # 화면 갱신
    # --------------------------------

    def refresh(state):
        current_time = state.get("current_time")

        if current_time:
            time_text = current_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        else:
            time_text = "-"

        world_id_label.set_text(
            f'World ID: {state.get("world_id", "-")}'
        )

        time_label.set_text(
            f'Time: {time_text}'
        )

        tick_label.set_text(
            f'Tick: {state.get("tick", "-")}'
        )

        seed_label.set_text(
            f'Seed: {state.get("seed", "-")}'
        )

        inspector_tick.set_text(
            f'Tick: {state.get("tick", "-")}'
        )

    # --------------------------------
    # STEP
    # --------------------------------

    def step():
        world.step()

        state = world.get_state()

        event_logs.append(
            f'Tick {state["tick"]} completed'
        )

        event_log.set_text(
            "\n".join(event_logs[-10:])
        )

        refresh(state)

    # --------------------------------
    # TITLE
    # --------------------------------

    ui.label(
        'NOVA-SIM Observer'
    ).classes(
        'text-2xl font-bold'
    )

    # --------------------------------
    # SIMULATION CONTROL
    # --------------------------------

    with ui.card().classes("w-full"):

        world_id_label = ui.label()
        time_label = ui.label()
        tick_label = ui.label()
        seed_label = ui.label()

        ui.button(
            "STEP",
            on_click=step,
        )

    # --------------------------------
    # WORLD VIEW + INSPECTOR
    # --------------------------------

    with ui.row().classes(
        "w-full items-stretch"
    ):

        # WORLD VIEW
        with ui.card().classes("flex-grow"):

            ui.label(
                "WORLD VIEW"
            ).classes(
                "text-lg font-bold"
            )

            world_center = initial_state["world_center"]

            world_map = ui.leaflet(
                center=(
                    world_center["latitude"],
                    world_center["longitude"],
                ),
                zoom=13,
            ).classes(
                "w-full h-[500px]"
            )

        # INSPECTOR
        with ui.card().classes("w-64"):

            ui.label(
                "INSPECTOR"
            ).classes(
                "text-lg font-bold"
            )

            ui.label("World")

            inspector_tick = ui.label()

    # --------------------------------
    # EVENT LOG
    # --------------------------------

    with ui.card().classes("w-full"):

        ui.label(
            "EVENT LOG"
        ).classes(
            "text-lg font-bold"
        )

        event_log = ui.label(
            "No events yet"
        ).classes(
            "whitespace-pre-line"
        )

    # --------------------------------
    # Leaflet 초기화 대기
    # --------------------------------

    await world_map.initialized()

    # --------------------------------
    # 최초 Entity 렌더링
    # --------------------------------

    for entity in initial_state["entities"]:
        render_entity(
            world_map,
            entity,
        )

    # --------------------------------
    # 최초 상태 표시
    # --------------------------------

    refresh(initial_state)


ui.run(
    title='NOVA-SIM Observer'
)