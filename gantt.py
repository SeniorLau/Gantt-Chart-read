import plotly.express as px
import pandas as pd


def make_gantt(df, color_by="Assigned"):

    df = df.copy()


    # Convert progress

    df["Progress_num"] = (
        df["Progress"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )


    # Make one-day tasks visible

    df["Display_Finish"] = df["Finish"]

    one_day = df["Start"] == df["Finish"]

    df.loc[
        one_day,
        "Display_Finish"
    ] = (
        df.loc[one_day, "Finish"]
        + pd.Timedelta(hours=12)
    )


    # Select grouping

    if color_by == "Phase":

        df["Color_group"] = (
            df["Phase"]
            .fillna("No phase")
            .astype(str)
        )

    else:

        df["Color_group"] = (
            df["Assigned"]
            .fillna("Unknown")
            .astype(str)
        )


    # Completed tasks get separate group

    df["Display_color"] = df["Color_group"]

    df.loc[
        df["Progress_num"] >= 100,
        "Display_color"
    ] = "✓ Completed"



    # Task label

    df["Task_label"] = (
        df["Task"]
        + " ("
        + df["Progress"]
        + ")"
    )


    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Display_Finish",
        y="Task_label",
        color="Display_color",
        hover_data=[
            "Phase",
            "Assigned",
            "Progress",
            "Start",
            "Finish"
        ]
    )


    # Reverse order

    fig.update_yaxes(
        autorange="reversed",
        showgrid=True
    )


    # Daily grid

    fig.update_xaxes(
        dtick="D1",
        tickformat="%d %b",
        showgrid=True
    )


    fig.update_layout(

        height=max(
            450,
            len(df)*35
        ),

        margin=dict(
            l=250,
            r=20,
            t=40,
            b=80
        ),

        bargap=0.3,

        legend_title_text=color_by
    )


    # Force completed bars green

    for trace in fig.data:

        if trace.name == "✓ Completed":

            trace.marker.color = "green"


    return fig
