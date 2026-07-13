import plotly.express as px


def make_gantt(df, color="Assigned"):

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color=color,
        hover_data=[
            "Phase",
            "Assigned",
            "Progress",
            "Start",
            "Finish"
        ],
    )

    # Task order: first task at the top
    fig.update_yaxes(
        autorange="reversed",
        tickfont=dict(size=10)
    )

    # Compact layout
    fig.update_layout(
        height=max(400, len(df) * 35),
        margin=dict(
            l=180,
            r=20,
            t=40,
            b=40
        ),
        xaxis=dict(
            tickformat="%d %b",
            tickangle=0
        ),
        bargap=0.35,
        legend_title_text=color
    )

    return fig
