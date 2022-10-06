from datetime import datetime
import plotly.graph_objects as go


def render_fig(data):
    x0, x1, p0, xt = parse_fig_data(data)
    fig_settings = {
        # 'width': 100
    }
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=xt,
            y=x0,
            name="systolic [mmHg]",
            # width=[0.8]*len(xt),
            **fig_settings,
        )
    )
    fig.add_trace(
        go.Bar(
            x=xt,
            y=x1,
            name="diastolic [mmHg]",
            **fig_settings,
        )
    )
    fig.add_trace(
        go.Bar(
            x=xt,
            y=p0,
            name="pulse [bpm]",
            **fig_settings,
        )
    )
    fig = fig.update_traces(
        showlegend=True,
    )

    return fig


def parse_fig_data(data):
    x0 = []
    x1 = []
    p0 = []
    xt = []

    def parse_date(date: str, timestamp: str):
        day, month, year = date.split(".")
        hour, minute = timestamp.split(":")
        return datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
        )

    for item in data["items"]:
        if shard := item.get("morning"):
            x0.append(shard["up"])
            x1.append(shard["down"])
            p0.append(shard["pulse"])
            xt.append(parse_date(item["date"], shard["timestamp"]))
        if shard := item.get("evening"):
            x0.append(shard["up"])
            x1.append(shard["down"])
            p0.append(shard["pulse"])
            xt.append(parse_date(item["date"], shard["timestamp"]))
    return x0, x1, p0, xt
