from openpyxl import load_workbook
import pandas as pd


def normalize_progress(value):

    if value is None:
        return "0%"

    try:

        # Excel numeric percentage
        # 1.0 = 100%
        # 0.5 = 50%
        if isinstance(value, (int, float)):

            if 0 <= value <= 1:
                return f"{round(value * 100)}%"

            return f"{round(value)}%"


        # Text values
        text = str(value).strip()

        # Remove percentage sign
        text = text.replace("%", "")

        number = float(text)

        if 0 <= number <= 1:
            number = number * 100

        return f"{round(number)}%"


    except Exception:

        return "0%"



def parse_excel(filename):

    wb = load_workbook(
    filename,
    data_only=False
    )

    ws = wb.active


    tasks = []

    phase = None

    header_found = False



    for row_number, row in enumerate(
        ws.iter_rows(values_only=True),
        start=1
    ):

        # Columns:
        # B Task
        # C Assigned
        # D Progress
        # E Start
        # F Finish

        b = row[1] if len(row) > 1 else None
        c = row[2] if len(row) > 2 else None
        d = row[3] if len(row) > 3 else None
        e = row[4] if len(row) > 4 else None
        f = row[5] if len(row) > 5 else None



        # Find header row

        if (
            str(b).strip() == "TAAK"
            and "TOEGEWEZEN" in str(c)
        ):

            header_found = True
            continue



        if not header_found:
            continue



        # End of planning

        if (
            b
            and "Voeg nieuwe rijen" in str(b)
        ):
            break



        # Skip empty rows

        if b is None:
            continue



        # Convert dates

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



        # Phase row:
        # text in B but no dates

        if (
            pd.isna(start)
            and pd.isna(finish)
            and b
        ):

            phase = str(b).strip()

            continue



        # Task row

        if (
            pd.notna(start)
            and pd.notna(finish)
        ):

            tasks.append(
                {
                    "Phase": phase,

                    "Task": str(b).strip(),

                    "Assigned": (
                        str(c).strip()
                        if c
                        else "Unknown"
                    ),

                    "Progress_raw": d,

                    "Progress": normalize_progress(d),

                    "Start": start,

                    "Finish": finish,
                }
            )



    df = pd.DataFrame(tasks)


    return df
