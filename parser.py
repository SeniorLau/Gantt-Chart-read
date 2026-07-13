from openpyxl import load_workbook
import pandas as pd


def parse_excel(filename):

    wb = load_workbook(filename, data_only=True)
    ws = wb.active

    phase = None
    tasks = []

    for row in ws.iter_rows(values_only=True):

        # Take first five columns only
        values = list(row[:5])

        while len(values) < 5:
            values.append(None)

        task, assigned, progress, start, end = values

        # Ignore completely empty rows
        if all(v is None for v in values):
            continue

        # Detect phase headers
        if (
            task
            and assigned is None
            and progress is None
            and start is None
            and end is None
        ):
            phase = str(task).strip()
            continue

        # Convert dates safely
        try:
            start_date = pd.to_datetime(start, dayfirst=True)
            end_date = pd.to_datetime(end, dayfirst=True)
        except Exception:
            continue

        # Ignore rows without a valid task
        if task is None:
            continue

        tasks.append(
            {
                "Phase": phase,
                "Task": str(task).strip(),
                "Assigned": assigned,
                "Progress": progress,
                "Start": start_date,
                "Finish": end_date,
            }
        )

    return pd.DataFrame(tasks)
