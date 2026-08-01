def validate_positive(func):
    def wrapper(drug_name, weight_kg, drugs):
        if weight_kg <= 0:
            return f"Invalid weight: {weight_kg} kg. Weight must be positive."
        return func(drug_name, weight_kg, drugs)
    return wrapper


def cache_dose(func):
    cache = {}

    def wrapper(drug_name, weight_kg, drugs):
        key = (drug_name, weight_kg)

        if key in cache:
            print(f"(Using cached result for {drug_name}, {weight_kg}kg)")
            return cache[key]

        result = func(drug_name, weight_kg, drugs)

        if isinstance(result, (int, float)):
            cache[key] = result

        return result

    return wrapper


@cache_dose
@validate_positive
def calculate_dose(drug_name, weight_kg, drugs):
    try:
        drug_info = drugs[drug_name]
        dose_per_kg = drug_info["dose_per_kg"]
        max_daily_mg = drug_info["max_daily_mg"]

    except KeyError:
        return f"'{drug_name}' not found in drug database."

    else:
        calculated_dose = dose_per_kg * weight_kg
        return min(calculated_dose, max_daily_mg)


def build_report(patients, drugs):
    """
    Combine patient records with drug info to build a full report,
    flagging any dose that was capped at the drug's daily maximum.

    Returns
    -------
    list of dict
        One row per patient. A patient whose drug isn't in the
        database is skipped (with a warning) instead of crashing
        the whole report.
    """
    report = []

    for patient in patients:
        try:
            drug_info = drugs[patient["drug_name"]]

        except KeyError:
            print(f"⚠️  Skipping {patient['name']} — drug "
                  f"'{patient['drug_name']}' not found in database.")
            continue

        was_capped = patient["calculated_dose"] == drug_info["max_daily_mg"]

        row = {
            "name": patient["name"],
            "weight": patient["weight"],
            "drug_name": patient["drug_name"],
            "calculated_dose": patient["calculated_dose"],
            "unit": drug_info.get("unit", "mg"),
            "capped_at_max": "yes" if was_capped else "no"
        }
        report.append(row)

    return report
