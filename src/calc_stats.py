from typing import Collection


def calc_stats(arr: Collection) -> list[dict]:
    avg_val = round(sum(arr) / len(arr), 2)
    return [
        {
            "name": "Avg",
            "value": avg_val,
        },
        {
            "name": "Max",
            "value": max(arr),
        },
        {
            "name": "Min",
            "value": min(arr),
        },
    ]


def prepare_data_for_stats(data: dict) -> dict[str, list]:
    all_up = []
    all_down = []
    all_pulse = []
    for item in data["items"]:
        if morning := item.get("morning"):
            all_up.append(morning["up"])
            all_down.append(morning["down"])
            all_pulse.append(morning["pulse"])
        if evening := item.get("evening"):
            all_up.append(evening["up"])
            all_down.append(evening["down"])
            all_pulse.append(evening["pulse"])
    return {
        "data_up": calc_stats(all_up),
        "data_down": calc_stats(all_down),
        "data_pulse": calc_stats(all_pulse),
    }
