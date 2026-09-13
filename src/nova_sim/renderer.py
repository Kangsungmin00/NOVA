ENTITY_ICONS = {
    "agent": "📍",
    "vehicle": "🚚",
    "robot": "🤖",
    "warehouse": "🏭",
}


def get_entity_icon(entity_type: str) -> str:
    return ENTITY_ICONS.get(
        entity_type,
        "●",
    )


def render_entity(world_map, entity):
    icon = get_entity_icon(
        entity["entity_type"]
    )

    marker = world_map.marker(
        latlng=(
            entity["latitude"],
            entity["longitude"],
        )
    )

    marker.run_method(
        ":setIcon",
        f'window.L.divIcon({{html: "{icon}", className: ""}})'
    )

    return marker