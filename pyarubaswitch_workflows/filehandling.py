import csv
from typing import List

from pydantic import BaseModel


def export_transceivers_csv(switches, filename):
    """
    Exports transceivers from switch objects to csv file
    params:
    :switches list of switch objects
    : filename string, filename of csvfile
    """
    with open(file=filename, mode="w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # header
        header = [
            "switch_ip",
            "part_number",
            "port_id",
            "product_number",
            "serial_number",
            "type",
        ]
        writer.writerow(header)

        for sw in switches:
            for trans in sw.transceivers:
                writer.writerow(
                    [
                        sw.switch_ip,
                        trans.part_number,
                        trans.port_id,
                        trans.product_number,
                        trans.serial_number,
                        trans.type,
                    ]
                )


def models_to_csv(
    csv_filepath: str,
    models: List[BaseModel],
    include_fields: dict,
    exlude_none: bool = True,
    append: bool = False,
) -> None:
    """
    Export list of models to csv-file.
    Can be: Switches, APs or Gateways, events.

    Args:
        csv_filepath(str): Path where to create the csv-file.
        models(list[BaseModel]): List of BaseModel objects.

        include_fields(dict)Optional: dict of fields to include from model.
                e.g. {'name','id','site'} if not supplied include all fields.
        append(bool)Optional: Append to file, default = False (as in write mode)
    """
    # set header
    if include_fields is not None:
        sample_dict = models[0].model_dump(include=include_fields)
    else:
        sample_dict = models[0].model_dump()

    fields = list(sample_dict.keys())

    if append:
        mode = "a"
    else:
        mode = "w"
    with open(csv_filepath, mode=mode, encoding="utf-8-sig") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fields)
        # write header
        writer.writeheader()

        for entry in models:
            if include_fields is not None:
                row = entry.model_dump(include=include_fields, exclude_none=exlude_none)
            else:
                row = entry.model_dump(exclude_none=exlude_none)
            writer.writerow(row)
