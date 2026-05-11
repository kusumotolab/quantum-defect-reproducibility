import csv
from pathlib import Path
from collections import Counter, defaultdict

CATEGORY_MAP = {}

for pid in [5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 25, 26, 27, 29, 30, 31, 39]:
    CATEGORY_MAP[pid] = "Output Wrong"

for pid in [1, 2, 3, 6, 13, 15, 18, 19, 20, 24, 28, 33, 35, 36, 37, 38, 40, 42]:
    CATEGORY_MAP[pid] = "Throw Exception"

for pid in [4, 41]:
    CATEGORY_MAP[pid] = "Simulation Failure"


def normalize_status(value: str) -> str:
    return value.strip().lower()


def classify(test_buggy: str, test_fixed: str) -> str:
    buggy = normalize_status(test_buggy)
    fixed = normalize_status(test_fixed)

    if buggy == "fail" and fixed == "pass":
        return "Complete Success"

    if buggy == "fail" and fixed == "fail":
        return "Partial Success"

    return "Failure"


def count_results(input_csv: Path, output_csv: Path) -> None:
    counter = Counter()
    id_sets = defaultdict(set)

    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        required = {"id", "run", "test_buggy", "test_fixed"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                f"CSV do not have necessory raw. required: {required}, fact: {reader.fieldnames}"
            )

        for row in reader:
            proj_id = int(row["id"])
            category = CATEGORY_MAP.get(proj_id)

            if category is None:
                continue

            result = classify(row["test_buggy"], row["test_fixed"])

            counter[(category, result)] += 1
            id_sets[(category, result)].add(proj_id)

    categories = [
        "Output Wrong",
        "Throw Exception",
        "Simulation Failure",
    ]

    results = [
        "Complete Success",
        "Partial Success",
        "Failure",
    ]

    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Result", "Count", "IDs"])

        for category in categories:
            for result in results:
                count = counter[(category, result)]
                ids = sorted(id_sets[(category, result)])
                ids_str = ",".join(str(i) for i in ids)

                writer.writerow([
                    category,
                    result,
                    count,
                    ids_str,
                ])


def main() -> None:
    script_dir = Path(__file__).resolve().parent

    input_csv = script_dir / "execution_results.csv"
    output_csv = script_dir / "count_results.csv"

    if not input_csv.exists():
        print(f"{input_csv} not found.")
        return

    count_results(input_csv, output_csv)

    print(f"save count result at {output_csv} ")


if __name__ == "__main__":
    main()