# -*- coding: utf-8 -*-
"""
Drug Dose Calculator — File I/O
----------------------------------
Handles reading/writing drugs.json and patients.csv. Contains no
clinical or dose-calculation logic — that lives in dose_calculator.py.

Created on Wed Jul 29 2026
@author: Amirhesam Karbakhsh
"""
import json
import csv
import os


def load_drugs(filepath):
    """
    Read the drug database from a JSON file and return it as a dict.

    Returns
    -------
    dict or None
        The drugs dictionary on success. None if the file is missing
        or contains invalid JSON — callers should check for None and
        bail out of the current menu action rather than crashing.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"⚠️  Drug database not found: {filepath}")
        return None

    except json.JSONDecodeError:
        print(f"⚠️  Drug database file is corrupted or not valid JSON: {filepath}")
        return None


def save_drugs(filepath, drugs):
    """
    Write the full drugs dictionary back to drugs.json, overwriting
    the previous contents (JSON can't be appended to like CSV can —
    the whole structure has to be rewritten as one unit).
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(drugs, file, ensure_ascii=False, indent=2)

    except PermissionError:
        print(f"⚠️  Cannot write to {filepath} — check if it's open elsewhere.")

    else:
        print(f"✔ Drug database updated: {filepath}")


def parse_weight(raw_value):
    """
    Convert one raw CSV field into a usable numeric value.

    Returns
    -------
    float, None, or the string "invalid"
        None if the field was empty (nothing recorded).
        "invalid" if the field had non-numeric text in it.
    """
    if raw_value == "":
        return None

    try:
        value = float(raw_value)

    except ValueError:
        print(f"⚠️  '{raw_value}' is not a valid number — flagging as invalid data.")
        return "invalid"

    else:
        return value

    finally:
        print(f"Finished parsing value: '{raw_value}'")


def load_patients(filepath):
    """
    Read patients.csv and return a list of patient dictionaries.

    Each patient dict looks like:
        {"name": "Ali", "weight": 20.0,
         "drug_name": "amoxicillin", "calculated_dose": 500.0}

    Returns
    -------
    list of dict
        Empty list if the file is missing or malformed.
    """
    patients_list = []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                patient = {
                    "name": row["name"],
                    "weight": parse_weight(row["weight"]),
                    "drug_name": row["drug_name"],
                    "calculated_dose": parse_weight(row["calculated_dose"])
                }
                patients_list.append(patient)

    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        print("    No patients have been registered yet, or the file was moved.")
        return []

    except KeyError as missing_column:
        print(f"⚠️  Missing expected column in CSV: {missing_column}")
        print("    Check that the header row matches: "
              "name,weight,drug_name,calculated_dose")
        return []

    else:
        return patients_list


def ensure_csv_has_header(filepath, fieldnames):
    """
    Make sure patients.csv exists and starts with a header row.

    This matters because append_patient() always opens the file in
    "append" mode and only ever writes a data row — if the file
    didn't already have a header, the first patient's own data
    would be mistaken for the header the next time the file is
    read, silently corrupting every patient's data.

    Safe to call every time the program starts: if the file already
    exists, it is left completely untouched.
    """
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def append_patient(filepath, patient_row):
    """
    Add one new patient (flat dict matching the CSV columns) to the
    end of patients.csv, without touching any existing rows.
    """
    try:
        with open(filepath, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=patient_row.keys())
            writer.writerow(patient_row)

    except PermissionError:
        print(f"⚠️  Cannot write to {filepath} — make sure it's not open in another program (like Excel).")

    except KeyError:
        print("⚠️  Patient data is missing the 'name' field.")

    else:
        print(f"✔ Patient '{patient_row.get('name', 'Unknown')}' added successfully.")


def set_drug(drugs, drug_name, dose_per_kg, max_daily_mg, unit="mg"):
    """
    Add a new drug, or overwrite an existing one, in the drugs
    dictionary (in memory — caller must call save_drugs() afterward
    to persist the change to disk).

    Returns
    -------
    str
        A message saying whether this was an addition or an update.
    """
    is_update = drug_name in drugs

    drugs[drug_name] = {
        "dose_per_kg": dose_per_kg,
        "max_daily_mg": max_daily_mg,
        "unit": unit
    }

    if is_update:
        return f"✔ Updated existing drug: '{drug_name}'"
    else:
        return f"✔ Added new drug: '{drug_name}'"


def save_report(filepath, report):
    """
    Write the full dose report to a CSV file, overwriting any
    previous report — it always reflects the current state of all
    patients, not an accumulation of past runs.
    """
    try:
        fieldnames = report[0].keys()

    except IndexError:
        print("⚠️  Report is empty — nothing to save.")
        return

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report)

    except PermissionError:
        print(f"⚠️  Cannot write to {filepath} — check if it's open elsewhere.")

    else:
        print(f"✔ Report saved to {filepath}")
