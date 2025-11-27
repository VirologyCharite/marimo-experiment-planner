import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium", css_file="")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import itertools as it
    import re
    import numpy as np
    import math
    return it, math, mo, np, pd, re


@app.cell(hide_code=True)
def _(experiment, groups, mo, sample_sheet):
    _left_col = mo.vstack(
        [
            mo.md("## Input"),
            experiment,
            groups.style(width="400px").left(),
            mo.ui.array,
        ]
    )
    _right_col = mo.vstack(
        [
            mo.md("## Output"),
            mo.ui.table(sample_sheet),
        ]
    )
    mo.hstack([_left_col, _right_col])
    return


@app.cell
def _(data_checkboxes, mo, plate_type, rows_per_plate, samples_per_row):
    mo.vstack(
        [
            mo.hstack(
                [
                    mo.vstack([plate_type, samples_per_row, rows_per_plate]),
                    mo.vstack(
                        [
                            mo.md("**Data to show in plate view:**"),
                            *data_checkboxes,
                        ]
                    ),
                ]
            ),
        ]
    )
    return


@app.cell
def _(mo):
    plate_type = mo.ui.dropdown(
        options=[6, 12, 24, 48, 96],
        allow_select_none=False,
        value=6,
        label="Plate type",
    )
    return (plate_type,)


@app.cell
def _(mo, sample_sheet):
    data_checkboxes = mo.ui.array(
        [mo.ui.checkbox(label=x) for x in sample_sheet.columns]
    )
    return (data_checkboxes,)


@app.cell
def _():
    return


@app.cell
def _(mo, plate_type):
    plate_layout = {6: (3, 2), 12: (4, 3), 24: (6, 4), 48: (8, 6), 96: (12, 8)}
    samples_per_row = mo.ui.slider(
        label="Samples/row",
        start=1,
        stop=plate_layout[plate_type.value][0],
        value=plate_layout[plate_type.value][0],
        show_value=True,
    )
    rows_per_plate = mo.ui.slider(
        label="Rows/plate",
        start=1,
        stop=plate_layout[plate_type.value][1],
        value=plate_layout[plate_type.value][1],
        show_value=True,
    )
    return rows_per_plate, samples_per_row


@app.cell
def _(
    arrays_to_tables,
    data_checkboxes,
    generate_plate_new,
    mo,
    plate_type,
    rows_per_plate,
    sample_sheet,
    samples_per_row,
):
    mo.Html(
        arrays_to_tables(
            generate_plate_new(
                sample_sheet.loc[:, data_checkboxes.value],
                plate_type.value,
                samples_per_row.value,
                rows_per_plate.value,
            )
        )
    )
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell
def _(math, np):
    def arrays_to_tables(arrays):
        html = """<style>
        /* generated with chatgpt, as I don't want to learn CSS right now */

        /* Plate table container */
        table.plate {
            border-collapse: collapse;
            border-spacing: 0;
            margin: 10px 0;
            table-layout: fixed;           /* ensures fixed cell sizes */
            font-family: sans-serif;
        }

        /* All cells */
        table.plate th,
        table.plate td {
            width: 70px;                   /* fixed well width */
            height: 50px;                  /* fixed well height */
            border: 1px solid #bcbcbc;
            text-align: center;
            vertical-align: middle;
            padding: 4px;
            overflow-wrap: break-word;     /* allow line breaks */
            overflow: hidden;

            /* Auto-scaling font size depending on text length */
            font-size: clamp(0.55rem, 1.4vw, 0.95rem);
            line-height: 1.15;
        }

        /* Top header row */
        table.plate th {
            background-color: #e8e8e8;
            font-weight: 600;
        }

        /* First left-side index column */
        table.plate td:first-child {
            background-color: #e8e8e8;
            font-weight: 600;
            width: 45px;                   /* row label narrower than wells */
        }

        /* Optional: hover highlight */
        table.plate td:not(:first-child):hover {
            background-color: #f5faff;
        }
        </style>
                                                                    """

        for array_idx, array in enumerate(arrays):
            headers = "".join(
                [f"<th>{x}</th>" for x in range(1, array.shape[1] + 1)]
            )
            html_table = f"<b>Table {array_idx + 1}</b><table class='plate'><tr><th></th>{headers}</tr>"
            for row_idx, row in enumerate(array):
                html_table += f"<tr><td>{chr(row_idx + 65)}</td>"
                for cell in row:
                    html_table += f"<td>{cell}</td>"
                html_table += "</tr>"
            html_table += "</table>"
            html += html_table
        return html


    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]


    # Plate generator
    def generate_plate_new(
        df,
        plate_type=24,
        samples_per_row=None,
        rows_per_plate=None,
    ):
        plate_layouts = {  # row, col
            6: (2, 3),
            12: (3, 4),
            24: (4, 6),
            48: (6, 8),
            96: (8, 12),
        }
        plate_layout = plate_layouts[plate_type]

        content = [list(x)[1:] for x in df.itertuples()]
        content = ["<br />".join([str(x) for x in y]) for y in content]

        samples_per_plate = samples_per_row * rows_per_plate
        n_plates = math.ceil(len(content) / samples_per_plate)
        content_idx = 0
        plates = []
        for _ in range(0, n_plates):
            plate = np.full(plate_layout, "", dtype=object)
            for row_idx, row in enumerate(plate):
                if row_idx >= rows_per_plate:
                    continue
                for col_idx, col in enumerate(row):
                    if col_idx >= samples_per_row:
                        continue
                    if content_idx >= len(content):
                        continue
                    plate[row_idx, col_idx] = content[content_idx]
                    content_idx += 1
            plates.append(plate)

        return plates
    return arrays_to_tables, generate_plate_new


@app.cell
def _(mo):
    groups_placeholder = """Cell lines
    - A549
    - HEK293T
    - Calu3
    Plasmid
    - EV
    - E
    - M
    Treatment
    - Mock
    - BafA1
    """

    groups = mo.ui.text_area(
        label="Define your groups",
        placeholder=groups_placeholder,
        rows=11,
        full_width=True,  # or False, depending on desired layout
    )
    experiment = mo.ui.text(label="Experiment code")
    return experiment, groups


@app.cell
def _(experiment, groups, it, pd, re):
    _groups = {}
    current_group = ""
    for line in groups.value.split("\n"):
        if len(line) == 0:
            continue
        line = line.lstrip()
        line = re.sub("^\t\d\.", "-", line)
        line = re.sub("^\d\.", "-", line)
        if line.startswith("-"):
            _groups[current_group].append(line[1:].strip())
        else:
            _groups[line.strip()] = []
            current_group = line.strip()

    _combinations = it.product(*(_groups[_name] for _name in _groups))


    sample_sheet = pd.DataFrame(_combinations, columns=_groups)
    _id_len = len(str(len(sample_sheet)))
    _ids = [
        f"{experiment.value}_{str(x).rjust(_id_len, '0')}"
        for x in range(1, len(sample_sheet) + 1)
    ]
    sample_sheet.insert(0, "ID", _ids)
    return (sample_sheet,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
