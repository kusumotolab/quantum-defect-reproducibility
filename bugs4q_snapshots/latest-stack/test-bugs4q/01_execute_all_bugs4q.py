import os
import subprocess
import csv
import argparse
from importlib.metadata import version

QISKIT_VERSION = version("qiskit")
VERSION_TAG = f"qiskit-{QISKIT_VERSION}"

parser = argparse.ArgumentParser()
parser.add_argument(
    "project_id",
    nargs="?",
    type=int,
    help="Project ID to execute (1-42). If omitted, all projects are executed.",
)
args = parser.parse_args()

project_id = args.project_id

# Validate the project ID range.
if project_id is not None and not (1 <= project_id <= 42):
    parser.error("project_id must be an integer from 1 to 42.")

# Base directory paths.
BUGS4Q_DIR = "/src/bugs4q/"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Output file path.
if project_id is None:
    OUTPUT_FILE = os.path.join(CURRENT_DIR, f"execution_results_{VERSION_TAG}.csv")
else:
    OUTPUT_FILE = os.path.join(CURRENT_DIR, f"execution_results_{VERSION_TAG}_id{project_id}.csv")

# Log directory shared across all project IDs for the current Qiskit version.
LOG_DIR = os.path.join(CURRENT_DIR, f"logs/logs_{VERSION_TAG}")
os.makedirs(LOG_DIR, exist_ok=True)

NUM_RUNS = 30

# Store per-run execution results.
results = []

# Determine target project IDs.
target_ids = [project_id] if project_id is not None else range(1, 43)

# Execute each target project.
for artifact_id in target_ids:
    project_dir = os.path.join(BUGS4Q_DIR, str(artifact_id))
    test_path = os.path.join(project_dir, f"test_{artifact_id}.py")
    buggy_path = os.path.join(project_dir, f"buggy_{artifact_id}.py")
    fixed_path = os.path.join(project_dir, f"fixed_{artifact_id}.py")

    # Skip projects without a test file.
    if not os.path.exists(test_path):
        continue

    # Store logs under the version-specific directory, grouped by artifact ID.
    project_log_dir = os.path.join(LOG_DIR, str(artifact_id))
    os.makedirs(project_log_dir, exist_ok=True)

    for run in range(1, NUM_RUNS + 1):
        result = {
            "id": artifact_id,
            "run": run,
            "test_buggy": "",
            "test_fixed": "",
        }

        # Execute: python test_<id>.py buggy_<id>.py
        try:
            proc = subprocess.run(
                ["python", test_path, buggy_path],
                capture_output=True,
                text=True,
                cwd=project_dir,
            )
            result["test_buggy"] = "Pass" if proc.returncode == 0 else "Fail"
        except Exception as e:
            proc = type("", (), {"stdout": "", "stderr": str(e)})()
            result["test_buggy"] = "Fail"

        with open(
            os.path.join(project_log_dir, f"test_buggy_run{run:02d}.log"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(f"--- STDOUT ---\n{proc.stdout}\n--- STDERR ---\n{proc.stderr}\n")

        print(proc.stdout, end="")
        print(proc.stderr, end="")

        # Execute: python test_<id>.py fixed_<id>.py
        try:
            proc = subprocess.run(
                ["python", test_path, fixed_path],
                capture_output=True,
                text=True,
                cwd=project_dir,
            )
            result["test_fixed"] = "Pass" if proc.returncode == 0 else "Fail"
        except Exception as e:
            proc = type("", (), {"stdout": "", "stderr": str(e)})()
            result["test_fixed"] = "Fail"

        with open(
            os.path.join(project_log_dir, f"test_fixed_run{run:02d}.log"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(f"--- STDOUT ---\n{proc.stdout}\n--- STDERR ---\n{proc.stderr}\n")

        print(proc.stdout, end="")
        print(proc.stderr, end="")

        results.append(result)

    # Remove temporary byproducts generated in the script directory.
    removable_files = ["out.png", "result.txt"]
    for file_name in os.listdir(CURRENT_DIR):
        if file_name in removable_files:
            os.remove(os.path.join(CURRENT_DIR, file_name))

# Write per-run execution results to CSV.
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "run", "test_buggy", "test_fixed"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved execution results to {OUTPUT_FILE}.")
print(f"Saved logs under {LOG_DIR}/.")