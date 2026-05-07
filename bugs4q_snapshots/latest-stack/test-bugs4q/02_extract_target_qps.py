import csv
from pathlib import Path
from collections import Counter

# IDごとのカテゴリ定義
CATEGORY_MAP = {}
for id in [5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 25, 26, 27, 29, 30, 31, 39]:
    CATEGORY_MAP[id] = "Output Wrong"
for id in [1, 2, 3, 6, 13, 15, 18, 19, 20, 24, 28, 33, 35, 36, 37, 38, 40, 42]:
    CATEGORY_MAP[id] = "Throw Exception"
for id in [4, 41]:
    CATEGORY_MAP[id] = "Simulation Failure"


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
    id_sets = {}  # (category, result) -> set of ids

    with input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        required = {"id", "test_buggy", "test_fixed"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                f"CSVに必要な列がありません。必要: {required}, 実際: {reader.fieldnames}"
            )

        for row in reader:
            proj_id = int(row["id"])
            category = CATEGORY_MAP.get(proj_id)
            if category is None:
                continue  # カテゴリ未定義のIDはスキップ

            result = classify(row["test_buggy"], row["test_fixed"])
            counter[(category, result)] += 1

            key = (category, result)
            if key not in id_sets:
                id_sets[key] = set()
            id_sets[key].add(proj_id)

    categories = ["Output Wrong", "Throw Exception", "Simulation Failure"]
    results = ["Complete Success", "Partial Success", "Failure"]

    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Result", "Count", "IDs"])

        for category in categories:
            for result in results:
                count = counter[(category, result)]
                ids = sorted(id_sets.get((category, result), set()))
                ids_str = ",".join(str(i) for i in ids)
                writer.writerow([category, result, count, ids_str])


def main() -> None:
    script_dir = Path(__file__).resolve().parent

    input_files = sorted(script_dir.glob("for_resolve/execution_results_qiskit-*.csv"))
    if not input_files:
        print("execution_results_qiskit-*.csv が見つかりませんでした。")
        return

    for input_csv in input_files:
        suffix = input_csv.name.removeprefix("for_resolve/execution_results_")
        output_csv = script_dir / f"for_resolve/count_{suffix}"
        count_results(input_csv, output_csv)
        print(f"集計結果を {output_csv} に保存しました。")


if __name__ == "__main__":
    main()