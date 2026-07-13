import plotly.express as px
import pandas as pd


def make_gantt(df):

    df = df.copy()

    # Convert progress to number
    df["Progress_num"] = (
        df["Progress"]
        .astype(str)
        .str.replace("%", "")
        .astype(float)
    )

    # Make one-day tasks visible
    df["Display_Finish"] = df["Finish"]

    one_day = df["Start"] == df["Finish"]

    df.loc[one_day, "Display_Finish"] = (
        df.loc[one_day, "Finish"]
        + pd.Timedelta(hours=12)
    )

    # Color by person
    df["Color"] = df["Assigned"].astype(str)

    # Completed tasks become green
    df.loc[
        df["Progress_num"] >= 100,
        "Color"
    ] = "✓ Completed"


    df["Task_label"] = (
    df["Task"]
    + "  ("
    + df["Progress"].astype(str)
    + ")"
)


fig = px.timeline(
    df,
    x_start="Start",
    x_end="Display_Finish",
    y="Task_label",
    color="Color",


    # Reverse task order
    fig.update_yaxes(
        autorange="reversed",
        tickfont=dict(size=10),
        showgrid=True,
        gridwidth=1
    )


    # Daily X-axis with grid lines
    fig.update_xaxes(
        dtick="D1",
        tickformat="%d\n%b",
        tickfont=dict(size=9),
        showgrid=True,
        gridwidth=1
    )


    # Layout
    fig.update_layout(

        height=max(400, len(df) * 32),

        margin=dict(
            l=170,
            r=20,
            t=40,
            b=60
        ),

        bargap=0.25,

        plot_bgcolor="white",

        legend_title_text="Assigned",

        hovermode="closest"
    )


    # Make completed tasks green
    for trace in fig.data:
        if trace.name == "✓ Completed":
            trace.marker.color = "green"


    return fig
