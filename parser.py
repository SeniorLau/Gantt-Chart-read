from openpyxl import load_workbook
import pandas as pd


def parse_excel(filename):

    wb = load_workbook(filename, data_only=True)
    ws = wb.active

    tasks = []
    phase = None
    header_found = False

    for row_number, row in enumerate(ws.iter_rows(values_only=True), start=1):

        b = row[1] if len(row) > 1 else None
        c = row[2] if len(row) > 2 else None
        d = row[3] if len(row) > 3 else None
        e = row[4] if len(row) > 4 else None
        f = row[5] if len(row) > 5 else None


        # find table header
        if (
            str(b).strip() == "TAAK"
            and "TOEGEWEZEN" in str(c)
        ):
            header_found = True
            continue


        if not header_found:
            continue


        # stop at end
        if b and "Voeg nieuwe rijen" in str(b):
            break


        # ignore empty
        if b is None:
            continue


        # try dates
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


        # phase
        if (
            pd.isna(start)
            and pd.isna(finish)
            and b
        ):
            phase = str(b).strip()
            continue


        # task
        if (
            not pd.isna(start)
            and not pd.isna(finish)
        ):

            tasks.append(
                {
                    "Phase": phase,
                    "Task": str(b).strip(),
                    "Assigned": c,
                    "Progress": d,
                    "Start": start,
                    "Finish": finish,
                }
            )


    df = pd.DataFrame(tasks)

    return df
