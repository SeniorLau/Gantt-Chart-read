from openpyxl import load_workbook
import pandas as pd


def normalize_progress(value):

    if value is None:
        return "0%"

    try:

        if isinstance(value, (int, float)):

            if 0 <= value <= 1:
                return f"{round(value * 100)}%"

            return f"{round(value)}%"


        text = str(value).replace("%", "").strip()

        number = float(text)

        if 0 <= number <= 1:
            number *= 100

        return f"{round(number)}%"


    except Exception:
        return "0%"



def parse_excel(filename):

    # Keep cached Excel values
    wb = load_workbook(
        filename,
        data_only=True
    )

    ws = wb.active


    tasks = []
    phase = None
    header_found = False


    for row_number in range(1, ws.max_row + 1):

        # Read actual cells
        task_cell = ws.cell(row_number, 2)      # B
        person_cell = ws.cell(row_number, 3)    # C
        progress_cell = ws.cell(row_number, 4)  # D
        start_cell = ws.cell(row_number, 5)     # E
        finish_cell = ws.cell(row_number, 6)    # F


        b = task_cell.value
        c = person_cell.value
        d = progress_cell.value

        # Handle Excel percentage formatting
        if (
            progress_cell.number_format
            and "%"
            in progress_cell.number_format
        ):
        
            if isinstance(d, (int, float)):
        d = d * 100
        e = start_cell.value
        f = finish_cell.value


        # Find header

        if (
            str(b).strip() == "TAAK"
            and "TOEGEWEZEN" in str(c)
        ):
            header_found = True
            continue


        if not header_found:
            continue


        # Stop at footer

        if b and "Voeg nieuwe rijen" in str(b):
            break


        if b is None:
            continue


        # Dates

        start = pd.to_datetime(
            e,
            dayfirst=True,
            errors="coerce"
        )

        finish = pd.to_datetime(
            f,
            dayfirst=True,
            errors="coerce"
        )


        # Phase row

        if pd.isna(start) and pd.isna(finish):

            phase = str(b).strip()

            continue


        # Task row

        if pd.notna(start) and pd.notna(finish):

            tasks.append(
                {
                    "Phase": phase,
                    "Task": str(b).strip(),
                    "Assigned": str(c) if c else "Unknown",

                    # keep for debugging
                    "Progress_raw": d,

                    "Progress": normalize_progress(d),

                    "Start": start,
                    "Finish": finish
                }
            )


    df = pd.DataFrame(tasks)


    return df
