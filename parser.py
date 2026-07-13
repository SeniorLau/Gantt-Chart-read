from openpyxl import load_workbook
import pandas as pd


def normalize_progress(value):

    if value is None:
        return "0%"

    try:

        # Excel value entered as 100 and formatted as %
        if isinstance(value, (int, float)):
            return f"{round(value)}%"

        text = str(value).strip()
        text = text.replace("%", "")

        return f"{round(float(text))}%"

    except Exception:
        return "0%"



def parse_excel(filename):

    wb = load_workbook(
        filename,
        data_only=True
    )

    ws = wb.active


    tasks = []

    phase = "Unknown"

    header_found = False



    for r in range(1, ws.max_row + 1):

        task = ws.cell(r, 2).value       # B
        assigned = ws.cell(r, 3).value   # C
        progress = ws.cell(r, 4).value   # D
        start = ws.cell(r, 5).value      # E
        finish = ws.cell(r, 6).value     # F



        # Find header

        if (
            str(task).strip() == "TAAK"
            and "TOEGEWEZEN" in str(assigned)
        ):
            header_found = True
            continue


        if not header_found:
            continue



        # End of file

        if (
            task
            and "Voeg nieuwe rijen" in str(task)
        ):
            break



        if task is None:
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



        # Phase row

        if (
            pd.isna(start_date)
            and pd.isna(finish_date)
        ):

            phase = str(task).strip()

            continue



        # Task row

        if (
            pd.notna(start_date)
            and pd.notna(finish_date)
        ):

            tasks.append(
                {
                    "Phase": phase,

                    "Task": str(task).strip(),

                    "Assigned": (
                        str(assigned).strip()
                        if assigned
                        else "Unknown"
                    ),

                    "Progress": normalize_progress(
                        progress
                    ),

                    "Start": start_date,

                    "Finish": finish_date
                }
            )


    df = pd.DataFrame(tasks)


    return df
