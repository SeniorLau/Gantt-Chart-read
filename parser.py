from openpyxl import load_workbook
import pandas as pd


def normalize_progress(value):

    if value is None:
        return "0%"

    try:

        if isinstance(value, (int, float)):
            return f"{round(value)}%"

        text = str(value).replace("%", "").strip()

        return f"{round(float(text))}%"

    except:
        return "0%"



def parse_excel(filename):

    wb = load_workbook(
        filename,
        data_only=True
    )

    ws = wb.active

    tasks = []

    phase = "Unknown phase"

    header_found = False


    for r in range(1, ws.max_row + 1):

        # Current Excel structure:
        # A = Assigned
        # B = Progress
        # C = Start
        # D = End

        assigned = ws.cell(r, 1).value
        progress = ws.cell(r, 2).value
        start = ws.cell(r, 3).value
        finish = ws.cell(r, 4).value


        # Detect header

        row_text = " ".join(
            [
                str(ws.cell(r,c).value)
                for c in range(1,5)
                if ws.cell(r,c).value
            ]
        )


        if (
            "TOEGEWEZEN" in row_text
            and "VOORTGANG" in row_text
        ):
            header_found = True
            continue


        if not header_found:
            continue


        # Empty rows

        if (
            assigned is None
            and progress is None
            and start is None
            and finish is None
        ):
            continue


        start_date = pd.to_datetime(
            start,
            dayfirst=True,
            errors="coerce"
        )

        finish_date = pd.to_datetime(
            finish,
            dayfirst=True,
            errors="coerce"
        )


        if (
            pd.notna(start_date)
            and pd.notna(finish_date)
        ):

            tasks.append(
                {
                    "Phase": phase,

                    "Task": f"Task {len(tasks)+1}",

                    "Assigned": str(assigned),

                    "Progress": normalize_progress(progress),

                    "Start": start_date,

                    "Finish": finish_date
                }
            )


    return pd.DataFrame(tasks)
