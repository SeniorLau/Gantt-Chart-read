from openpyxl import load_workbook
import pandas as pd


def parse_excel(filename):

    wb = load_workbook(filename, data_only=True)
    ws = wb.active

    tasks = []
    phase = None

    header_found = False

    for row in ws.iter_rows(values_only=True):

        b = row[1] if len(row) > 1 else None
        c = row[2] if len(row) > 2 else None
        d = row[3] if len(row) > 3 else None
        e = row[4] if len(row) > 4 else None
        f = row[5] if len(row) > 5 else None


        # Find the real header row
        if (
            str(b).strip() == "TAAK"
            and str(c).strip().startswith("TOEGEWEZEN")
        ):
            header_found = True
            continue


        if not header_found:
            continue


        # Ignore empty rows
        if b is None:
            continue


        # Ignore footer
        if "Voeg nieuwe rijen" in str(b):
            break


        # Convert dates
        try:
            start = pd.to_datetime(e, dayfirst=True)
            finish = pd.to_datetime(f, dayfirst=True)

        except Exception:
            start = None
            finish = None


        # Phase row
        if (
            b
            and start is None
            and finish is None
        ):
            phase = str(b).strip()
            continue


        # Task row
        if start is not None and finish is not None:

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


    return pd.DataFrame(tasks)
