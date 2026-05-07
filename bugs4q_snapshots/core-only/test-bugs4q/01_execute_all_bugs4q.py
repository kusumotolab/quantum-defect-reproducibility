import os
import subprocess
import csv
import argparse
from importlib.metadata import version, PackageNotFoundError

QISKIT_VERSION = version("qiskit")
VERSION_TAG = f"qiskit-{QISKIT_VERSION}"

# 引数
parser = argparse.ArgumentParser()
parser.add_argument(
    'project_id',
    nargs='?',
    type=int,
    help='実行するプロジェクトID (1-42)。未指定なら全件実行'
)
args = parser.parse_args()

project_id = args.project_id

# project_id の範囲チェック
if project_id is not None and not (1 <= project_id <= 42):
    parser.error('project_id は 1 から 42 の整数で指定してください。')

# ディレクトリのベースパス
BUGS4Q_DIR = '/src/bugs4q/'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 出力ファイル名
if project_id is None:
    OUTPUT_FILE = os.path.join(CURRENT_DIR, f'execution_results_{VERSION_TAG}.csv')
else:
    OUTPUT_FILE = os.path.join(CURRENT_DIR, f'for_resolve/execution_results_{VERSION_TAG}_id{project_id}.csv')

# ログディレクトリは常に共通
LOG_DIR = os.path.join(CURRENT_DIR, f'for_resolve/logs/logs_{VERSION_TAG}')
os.makedirs(LOG_DIR, exist_ok=True)

NUM_RUNS = 30

# 結果を格納するリスト
results = []

# 実行対象 id の決定
target_ids = [project_id] if project_id is not None else range(1, 43)

# 対象 id に対してループ
for id in target_ids:
    proj_dir = os.path.join(BUGS4Q_DIR, str(id))
    test_path = os.path.join(proj_dir, f'test_{id}.py')
    buggy_path = os.path.join(proj_dir, f'buggy_{id}.py')
    fixed_path = os.path.join(proj_dir, f'fixed_{id}.py')

    # テストファイルが無い場合はスキップ
    if not os.path.exists(test_path):
        continue

    # ログは共通ディレクトリ配下の id ごとのサブディレクトリ
    proj_log_dir = os.path.join(LOG_DIR, str(id))
    os.makedirs(proj_log_dir, exist_ok=True)

    for run in range(1, NUM_RUNS + 1):
        result = {'id': id, 'run': run, 'test_buggy': '', 'test_fixed': ''}

        # python test_{id}.py buggy_{id}.py
        try:
            proc = subprocess.run(
                ['python', test_path, buggy_path],
                capture_output=True, text=True, cwd=proj_dir
            )
            result['test_buggy'] = 'Pass' if proc.returncode == 0 else 'Fail'
        except Exception as e:
            proc = type('', (), {'stdout': '', 'stderr': str(e)})()
            result['test_buggy'] = 'Fail'
        with open(os.path.join(proj_log_dir, f'test_buggy_run{run:02d}.log'), 'w', encoding='utf-8') as f:
            f.write(f"--- STDOUT ---\n{proc.stdout}\n--- STDERR ---\n{proc.stderr}\n")
        print(proc.stdout, end='')
        print(proc.stderr, end='')

        # python test_{id}.py fixed_{id}.py
        try:
            proc = subprocess.run(
                ['python', test_path, fixed_path],
                capture_output=True, text=True, cwd=proj_dir
            )
            result['test_fixed'] = 'Pass' if proc.returncode == 0 else 'Fail'
        except Exception as e:
            proc = type('', (), {'stdout': '', 'stderr': str(e)})()
            result['test_fixed'] = 'Fail'
        with open(os.path.join(proj_log_dir, f'test_fixed_run{run:02d}.log'), 'w', encoding='utf-8') as f:
            f.write(f"--- STDOUT ---\n{proc.stdout}\n--- STDERR ---\n{proc.stderr}\n")
        print(proc.stdout, end='')
        print(proc.stderr, end='')

        results.append(result)

    # CURRENT_DIR直下に保存される副産物を削除
    rm_list = ['out.png', 'result.txt']
    for file in os.listdir(CURRENT_DIR):
        if file in rm_list:
            os.remove(os.path.join(CURRENT_DIR, file))

# CSVファイルに結果を書き込む
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'run', 'test_buggy', 'test_fixed'])
    writer.writeheader()
    writer.writerows(results)

print(f"Execution Results are saved at {OUTPUT_FILE}.")
print(f"Logs are saved under {LOG_DIR}/")