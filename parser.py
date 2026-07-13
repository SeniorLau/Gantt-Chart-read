from openpyxl import load_workbook
import pandas as pd


def normalize_progress(value):

    if value is None:
        return "0%"

    # Debug: keep original value if needed
    original = value

    try:

        # Numeric values from Excel
        if isinstance(value, (int, float)):

            # Excel percentage format:
            # 1 = 100%, 0.5 = 50%
            if value <= 1:
                return f"{round(value * 100)}%"

            return f"{round(value)}%"


        # Text values
        value = str(value).strip()

        # Remove % symbol
        value = value.replace("%", "")

        number = float(value)

        # If between 0 and 1, treat as Excel fraction
        if number <= 1:
            number = number * 100

        return f"{round(number)}%"


    except Exception:

        return "0%"

def parse_excel(filename):

    wb = load_workbook(
        filename,
        data_only=True
    )

    ws = wb.active


    tasks = []

    phase = None

    header_found = False


    for row_number, row in enumerate(
        ws.iter_rows(values_only=True),
        start=1
    ):


        # Excel columns:
        # B = Task
        # C = Assigned
        # D = Progress
        # E = Start
        # F = Finish

        b = row[1] if len(row) > 1 else None
        c = row[2] if len(row) > 2 else None
        d = row[3] if len(row) > 3 else None
        e = row[4] if len(row) > 4 else None
        f = row[5] if len(row) > 5 else None



        # Locate real project table header

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



        # Ignore empty rows

        if b is None:
            continue



        # Convert dates safely

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



        # Detect phase rows

        if (
            not pd.notna(start)
            and not pd.notna(finish)
            and b
        ):

            phase = str(b).strip()

            continue



        # Detect task rows

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

        # keep original Excel value for checking
        "Progress_raw": d,

        # formatted progress for chart/table
        "Progress": normalize_progress(d),

        "Start": start,

        "Finish": finish,
    }
)



    df = pd.DataFrame(tasks)


    return df
