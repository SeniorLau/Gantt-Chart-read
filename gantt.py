import plotly.express as px
import pandas as pd


def make_gantt(df, color_by="Assigned"):

    df = df.copy()


    # Convert progress to numeric
    df["Progress_num"] = (
    df["Progress"]
    .str.replace("%","")
    .astype(float)
    )

    df.loc[
    df["Progress_num"] == 100,
    "Color"
    ] = "Completed"


    # Make one-day tasks visible
    df["Display_Finish"] = df["Finish"]

    one_day = df["Start"] == df["Finish"]

    df.loc[one_day, "Display_Finish"] = (
        df.loc[one_day, "Finish"]
        + pd.Timedelta(hours=12)
    )


    # Select coloring mode
    if color_by not in ["Assigned", "Phase"]:
        color_by = "Assigned"


    df["Color"] = df[color_by].fillna("Unknown").astype(str)


    # Completed tasks override color
    df.loc[
        df["Progress_num"] >= 100,
        "Color"
    ] = "✓ Completed"



    # Add progress to task name
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


    # Put first task on top
    fig.update_yaxes(
        autorange="reversed",
        showgrid=True,
        gridwidth=1,
        tickfont=dict(size=10)
    )


    # Daily timeline
    fig.update_xaxes(
        dtick="D1",
        tickformat="%d\n%b",
        showgrid=True,
        gridwidth=1,
        tickfont=dict(size=9)
    )



    # Compact layout

    fig.update_layout(

        height=max(
            400,
            len(df) * 32
        ),

        margin=dict(
            l=200,
            r=20,
            t=40,
            b=70
        ),

        bargap=0.25,

        plot_bgcolor="white",

        legend_title_text=color_by,

        hovermode="closest"
    )



    # Completed tasks green

    for trace in fig.data:

        if trace.name == "✓ Completed":

            trace.marker.color = "green"



    return fig
