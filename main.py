# -*- coding: utf-8 -*-
"""
Drug Dose Calculator — Main Program
--------------------------------------
Created on Tue Jul 28 2026
@author: Amirhesam Karbakhsh
"""
import os
from calculator.dose_calculator import calculate_dose, build_report
from calculator.data_loader import (
    load_drugs,
    load_patients,
    save_report,
    append_patient,
    ensure_csv_has_header,
    save_drugs,
    set_drug,
)


def clear_screen():
    """Clear the terminal screen based on the user's Operating System."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_positive_float(prompt):
    """
    Ask the user for a positive decimal number and keep asking
    until they give one. Used for both patient weight and drug
    dose values, since both must be greater than zero.
    """
    while True:
        raw_value = input(prompt).strip()

        try:
            value = float(raw_value)

        except ValueError:
            print(f"⚠️  '{raw_value}' is not a valid number. Try again.")
            continue

        else:
            if value <= 0:
                print("⚠️  Value must be greater than zero. Try again.")
                continue
            return value


def get_drug_input(drugs):
    drug_name = input("Drug name: ").strip().lower()

    if drug_name in drugs:
        print(f"'{drug_name}' already exists. You are about to update it.")
        print(f"Current values: {drugs[drug_name]}")
    else:
        print(f"'{drug_name}' is new — adding it to the database.")

    dose_per_kg = get_valid_positive_float("Dose per kg (mg): ")
    max_daily_mg = get_valid_positive_float("Max daily dose (mg): ")

    return drug_name, dose_per_kg, max_daily_mg


def show_author_info():
    """Display the developer profile inside a styled ASCII frame."""
    print("\n" + "┌" + "─" * 43 + "┐")
    print("│             DEVELOPER PROFILE               │")
    print("├" + "─" * 43 + "┤")
    print("│  👤 Author: Amirhesam Karbakhsh             │")
    print("│  🎓 Field: Biomedical Engineering           │")
    print("│  💻 GitHub: github.com/Hesamkb85            │")
    print("└" + "─" * 43 + "┘")


def display_menu():
    """Render the interactive console CLI main menu options."""
    print("\n" + "=" * 50)
    print("   💊  DRUG DOSE CALCULATOR  💊")
    print("=" * 50)
    print(" [1] ➕ Register Patient & Calculate Dose")
    print(" [2] 💉 Add or Update a Drug")
    print(" [3] 📋 Generate & Save Report")
    print(" [4] 👤 Author Info")
    print(" [5] ❌ Exit")
    print("=" * 50)


drugs_file = os.path.join("calculator", "Drugs.json")
patients_csv = "patients.csv"
report_file = "dose_report.csv"
fieldnames = ["name", "weight", "drug_name", "calculated_dose"]

ensure_csv_has_header(patients_csv, fieldnames)

while True:
    clear_screen()
    display_menu()
    menu_choice = input("Please select an option (1-5): ").strip()

    if menu_choice == "1":
        clear_screen()
        drugs = load_drugs(drugs_file)

        if drugs is None:
            input("\nPress Enter to return to main menu...")
            continue

        name = input("Patient's name: ").strip()
        weight = get_valid_positive_float("Weight (kg): ")
        drug_name = input("Drug name: ").strip().lower()
        calculated_dose = calculate_dose(drug_name, weight, drugs)
        print(f"\nCalculated dose for {name}: {calculated_dose}")

        patient_row = {
            "name": name,
            "weight": weight,
            "drug_name": drug_name,
            "calculated_dose": calculated_dose
        }
        append_patient(patients_csv, patient_row)

        input("\nPress Enter to return to main menu...")

    elif menu_choice == "2":
        clear_screen()

        drugs = load_drugs(drugs_file)
        if drugs is None:
            input("\nPress Enter to return to main menu...")
            continue

        drug_name, dose_per_kg, max_daily_mg = get_drug_input(drugs)
        message = set_drug(drugs, drug_name, dose_per_kg, max_daily_mg)
        print(message)
        save_drugs(drugs_file, drugs)

        input("\nPress Enter to return to main menu...")

    elif menu_choice == "3":
        clear_screen()

        drugs = load_drugs(drugs_file)
        if drugs is None:
            input("\nPress Enter to return to main menu...")
            continue

        patients = load_patients(patients_csv)
        if not patients:
            print("⚠️  No patients found to generate a report.")
            print("    Register at least one patient first (option 1).")
            input("\nPress Enter to return to main menu...")
            continue

        report = build_report(patients, drugs)
        save_report(report_file, report)
        input("\nPress Enter to return to main menu...")

    elif menu_choice == "4":
        clear_screen()
        show_author_info()
        input("\nPress Enter to return to main menu...")

    elif menu_choice == "5":
        clear_screen()
        print("\n" + "=" * 50)
        print("  Thank you for using Drug Dose Calculator! 👋")
        print("              Exiting program...")
        print("=" * 50)
        break

    else:
        print("\n❌ Invalid choice! Please select 1, 2, 3, 4, or 5.")
        input("\nPress Enter to try again...")
