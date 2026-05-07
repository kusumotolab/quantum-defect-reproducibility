import csv
from pathlib import Path
from collections import Counter

# Category definition for each artifact ID.
CATEGORY_MAP = {}

for artifact_id in [5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 25, 26, 27, 29, 30, 31, 39]:
    CATEGORY_MAP[artifact_id] = "Output Wrong"

for artifact_id in [1, 2, 3, 6, 13, 15, 18, 19, 20, 24, 28, 33, 35, 36, 37, 38, 40, 42]:
    CATEGORY_MAP[artifact_id] = "Throw Exception"

for artifact_id in [4, 41]:
    CATEGORY_MAP[artifact_id] = "Simulation Failure"


def classify(test_buggy: str, test_fixed: str) -> str:
    test_buggy = test_buggy.strip()
    test_fixed = test_fixed.strip()

    if test_buggy == "Fail" and test_fixed == "Pass":
        return "Complete Success"

    if test_buggy == "Fail" and test_fixed == "Fail":
        return "Partial Success"

    return "Failure"


def count_results(input_csv: Path, output_csv: Path) -> None:
    counter = Counter()
    id_sets = {}  # (category, result) -> set of artifact IDs

    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        required_columns = {"id", "test_buggy", "test_fixed"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                f"Missing required CSV columns. "
                f"Required: {sorted(required_columns)}, "
                f"found: {reader.fieldnames}"
            )

        for row in reader:
            artifact_id = int(row["id"])
            category = CATEGORY_MAP.get(artifact_id)

            # Skip artifacts whose category is not defined in this study.
            if category is None:
                continue

            result = classify(row["test_buggy"], row["test_fixed"])
            counter[(category, result)] += 1

            key = (category, result)
            if key not in id_sets:
                id_sets[key] = set()
            id_sets[key].add(artifact_id)

    categories = ["Output Wrong", "Throw Exception", "Simulation Failure"]
    results = ["Complete Success", "Partial Success", "Failure"]

    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Result", "Count", "IDs"])

        for category in categories:
            for result in results:
                count = counter[(category, result)]
                ids = sorted(id_sets.get((category, result), set()))
                ids_str = ",".join(str(artifact_id) for artifact_id in ids)
                writer.writerow([category, result, count, ids_str])


def main() -> None:
    script_dir = Path(__file__).resolve().parent

    input_files = sorted(script_dir.glob("execution_results_qiskit-*.csv"))
    if not input_files:
        print("No execution_results_qiskit-*.csv files were found.")
        return

    for input_csv in input_files:
        output_csv = script_dir / f"count_{input_csv.name}"
        count_results(input_csv, output_csv)
        print(f"Saved aggregated results to {output_csv}.")


if __name__ == "__main__":
    main()