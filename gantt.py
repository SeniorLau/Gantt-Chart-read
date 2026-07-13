import plotly.express as px
import pandas as pd


def make_gantt(df):

    df = df.copy()

    # Convert progress to numeric
    df["Progress_num"] = (
        df["Progress"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    # Make one-day tasks visible
    df["Display_Finish"] = df["Finish"]

    mask = df["Start"] == df["Finish"]

    df.loc[mask, "Display_Finish"] = (
        df.loc[mask, "Finish"]
        + pd.Timedelta(hours=12)
    )

    # Color by person
    df["Color"] = df["Assigned"].fillna("Unknown").astype(str)

    # Completed tasks override color
    df.loc[
        df["Progress_num"] >= 100,
        "Color"
    ] = "Completed"


    # Add progress to task label
    df["Task_label"] = (
        df["Task"].astype(str)
        + " ("
        + df["Progress"].astype(str)
        + ")"
    )


    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Display_Finish",
        y="Task_label",
        color="Color",
        hover_data={
            "Phase": True,
            "Assigned": True,
            "Progress": True,
            "Start": True,
            "Finish": True
        }
    )


    # Reverse task order
    fig.update_yaxes(
        autorange="reversed",
        showgrid=True,
        gridwidth=1
    )


    # Daily timeline resolution
    fig.update_xaxes(
        dtick="D1",
        tickformat="%d\n%b",
        showgrid=True,
        gridwidth=1
    )


    fig.update_layout(
        height=max(400, len(df) * 32),

        margin=dict(
            l=180,
            r=20,
            t=40,
            b=60
        ),

        bargap=0.25,

        plot_bgcolor="white",

        legend_title_text="Assigned"
    )


    # Make completed tasks green
    for trace in fig.data:
        if trace.name == "Completed":
            trace.marker.color = "green"


    return fig
