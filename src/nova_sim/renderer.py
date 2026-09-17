from nicegui import ui


ENTITY_SYMBOLS = {
    "agent": "A",
    "vehicle": "V",
    "robot": "R",
    "warehouse": "W",
}


def get_entity_symbol(entity_type: str) -> str:
    return ENTITY_SYMBOLS.get(entity_type, "●")


def render_grid(
        container,
        entities: list[dict],
        width: int,
        height: int,
        ) -> None:
    """Render simulation entities on a zero-based Cartesian grid."""
    entities_by_position: dict[tuple[int, int], list[dict]] = {}
    for entity in entities:
        position = (entity["x"], entity["y"])
        entities_by_position.setdefault(position, []).append(entity)

    container.clear()
    with container:
        with ui.element("div").style(
                f"display: grid; grid-template-columns: 48px repeat({width}, 64px); "
                "gap: 2px; align-items: center; text-align: center;"
        ):
            ui.label("y \\ x").classes("font-bold")
            for x in range(width):
                ui.label(str(x)).classes("font-bold")

            for y in reversed(range(height)):
                ui.label(str(y)).classes("font-bold")
                for x in range(width):
                    occupants = entities_by_position.get((x, y), [])
                    symbol = " ".join(
                        get_entity_symbol(entity["entity_type"])
                        for entity in occupants
                    )
                    ui.label(symbol).style(
                        "height: 48px; border: 1px solid #9ca3af; "
                        "display: flex; align-items: center; justify-content: center;"
                    ).tooltip(", ".join(entity["entity_id"] for entity in occupants))
