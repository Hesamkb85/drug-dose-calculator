# 💊 Drug Dose Calculator

A console-based Python application for calculating weight-based drug dosages, managing a drug reference database, and generating patient dose reports — with built-in safety caps against exceeding maximum daily doses.

---

## 🚀 Key Features

* **Weight-Based Dose Calculation:** Computes patient-specific doses from a per-kilogram rate, automatically capped at each drug's maximum safe daily dose.
* **Editable Drug Database:** Add new drugs or update existing ones (dose per kg, max daily dose) — changes are persisted to a JSON file.
* **Report Generation:** Produces a CSV report for all registered patients, flagging any dose that was capped at the drug's daily maximum.
* **Robust Error Handling:** Gracefully handles missing drugs, corrupted data files, and invalid input without crashing.
* **Performance Optimization:** Uses a caching decorator to avoid recalculating the dose for a repeated (drug, weight) pair.

---

## 📂 Project Structure

```text
├── calculator/
│   ├── __init__.py
│   ├── Drugs.json          # Drug reference database (dose/kg, max daily dose)
│   ├── dose_calculator.py  # Core dose calculation logic + decorators
│   └── data_loader.py      # File I/O: drugs, patients, and reports
├── main.py                 # Main execution engine & interactive CLI menu
└── README.md
```

---

## 🧠 How It Works

1. **Register a patient** with their name, weight, and prescribed drug.
2. The app looks up the drug's `dose_per_kg` in the database and multiplies it by the patient's weight.
3. If the result exceeds the drug's `max_daily_mg`, the dose is automatically capped at the safe maximum.
4. All patients are saved to `patients.csv`, and a full report (with a `capped_at_max` flag) can be generated to `dose_report.csv`.

---

## 👤 Author

**Amirhesam Karbakhsh** — Biomedical Engineering Student
GitHub: [github.com/Hesamkb85](https://github.com/Hesamkb85)
