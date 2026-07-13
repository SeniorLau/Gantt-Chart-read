from openpyxl import load_workbook
import pandas as pd


def parse_excel(filename):

    wb = load_workbook(filename, data_only=True)
    ws = wb.active

    phase = None
    tasks = []

    for row in ws.iter_rows(values_only=True):

        values = list(row[:5])

        while len(values) < 5:
            values.append(None)

        task, assigned, progress, start, end = values

        # skip empty rows
        if all(v is None for v in values):
            continue

        # detect phase header
        if (
            task
            and assigned is None
            and progress is None
            and start is None
            and end is None
        ):
            phase = str(task).strip()
            continue

        # skip template titles
        if start is None or end is None:
            continue

        tasks.append(
            {
                "Phase": phase,
                "Task": task,
                "Assigned": assigned,
                "Progress": progress,
                "Start": pd.to_datetime(start),
                "Finish": pd.to_datetime(end),
            }
        )

    return pd.DataFrame(tasks)
