import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import itertools as it
    import re
    return it, mo, pd, re


@app.cell
def _(experiment, groups, mo, sample_sheet):
    left_col = mo.vstack(
        [
            mo.md("## Input"),
            experiment,
            groups.style(width="400px").left(),
        ]
    )
    right_col = mo.vstack([
        mo.md("## Output"),
        mo.ui.table(sample_sheet),
    ])
    mo.hstack([left_col,right_col])
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(experiment, groups, it, pd, re):
    _groups = {}
    current_group = ""
    for line in groups.value.split("\n"):
        if len(line) == 0:
            continue
        line = re.sub("^\t\d\.","-",line)
        line = re.sub("^\d\.","-",line)
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
        for x in range(1, len(sample_sheet)+1)
    ]
    sample_sheet.insert(0,"ID",_ids)
    return (sample_sheet,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
