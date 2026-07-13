import plotly.express as px


def make_gantt(df, color="Assigned"):

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color=color,
        hover_data=[
            "Assigned",
            "Phase",
            "Progress",
        ],
    )

    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        height=800,
        legend_title=color,
        xaxis_title="Date",
        yaxis_title="",
    )

    return fig
