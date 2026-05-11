# Replication Package for "On the Reproducibility of Quantum Software Defect Datasets: A Case Study of Bugs4Q"

![Requires Docker](https://img.shields.io/badge/Requires-Docker-blue?logo=docker)
![Requires Docker Compose](https://img.shields.io/badge/Requires-Docker--Compose-blue)
![Requires Make](https://img.shields.io/badge/Requires-Make-yellow?logo=gnu)

## Overview

This repository contains the replication package for our study on the reproducibility of the Bugs4Q quantum software defect dataset across Qiskit versions.
The package contains two groups of experiment snapshots.

1. `bugs4q_snapshots/`: snapshots for the main Bugs4Q reproducibility experiments under two dependency configurations:
   - `core-only`
   - `pinned-stack`

2. `bugs4q-robust_snapshot/`: a snapshot for the additional rerun experiment using the edited dataset, referred to as Bugs4Q-Robust in the paper.

Each snapshot preserves the original workspace layout used in the experiments. The directory layout is intentionally kept unchanged because the Docker files, Makefile targets, requirements files, and Python scripts rely on relative paths.

## Artifact Summary

This replication package provides the following artifacts:

- the curated Bugs4Q artifacts used in the main reproducibility experiments;
- Docker files and requirements files for constructing the experimental environments;
- execution scripts used to run buggy and fixed programs;
- raw execution logs for each Qiskit version;
- aggregated CSV files used to obtain the reported results;
- analysis notes for the research questions, including artifact-level ID lists that are more detailed than the tables in the paper;
- a separate snapshot for the Bugs4Q-Robust rerun experiment.

The package is organized as snapshots rather than as a single unified execution directory. This design prioritizes traceability to the actual experiment workspaces.

## Directory Structure

```text
.
├── README.md
├── bugs4q_snapshots/        # Main Bugs4Q reproducibility experiments
│   ├── core-only/
│   └── pinned-stack/
└── bugs4q-robust_snapshot/    # Bugs4Q-Robust rerun experiment
```

## Snapshot Design

This package uses snapshot-based organization rather than a single unified execution directory.
Each snapshot preserves the exact directory layout used during the corresponding experiment. The main reason is that the Docker build files, Makefile targets, requirements files, and execution scripts depend on relative paths. Moving files into a cleaner shared structure could make the package harder to rerun and could introduce inconsistencies between the released package and the actual experiment workspace.
The two snapshots under `bugs4q_snapshots/` correspond to the main Bugs4Q reproducibility experiments. The snapshot under `bugs4q-robust_snapshot/` corresponds to the additional experiment after applying code edits to the subject programs.

## Quick Start for Reviewers

This package can be inspected without rerunning the full experiments. We recommend the following order for artifact review.

1. Check the preserved result CSV files.
2. Inspect the corresponding raw logs for selected artifacts and Qiskit versions.
3. Rebuild and rerun selected configuration-version pairs only if needed.

The main Bugs4Q result files are located under each configuration snapshot:

```text
bugs4q_snapshots/<configuration>/test-bugs4q/execution_results_qiskit-<version>.csv
bugs4q_snapshots/<configuration>/test-bugs4q/count_execution_results_qiskit-<version>.csv
bugs4q_snapshots/<configuration>/test-bugs4q/logs/logs_qiskit-<version>/
```

For example, the result files for Qiskit 2.3.1 under `pinned-stack` are:

```text
bugs4q_snapshots/pinned-stack/test-bugs4q/execution_results_qiskit-2.3.1.csv
bugs4q_snapshots/pinned-stack/test-bugs4q/count_execution_results_qiskit-2.3.1.csv
bugs4q_snapshots/pinned-stack/test-bugs4q/logs/logs_qiskit-2.3.1/
```

The Bugs4Q-Robust rerun results are located at:

```text
bugs4q-robust_snapshot/execution_results.csv
bugs4q-robust_snapshot/count_results.csv
bugs4q-robust_snapshot/logs/
```

Building all Docker environments can take substantial time and disk space. Reviewers who only want to check the reported results can inspect the preserved CSV files and logs first.

## Prerequisites

This package requires the following tools:

- Docker
- Docker Compose
- Make

Python is provided inside each Docker container rather than by the host system. The host system does not need a `python` command to run the Docker-based experiments.

## Tested Host Environment

The experiments were conducted on WSL2 with Ubuntu 24.04.4 LTS.

| Item | Version / Description |
|---|---|
| Host subsystem | WSL2 |
| WSL version | 2.4.13.0 |
| Linux kernel | 5.15.167.4-microsoft-standard-WSL2 |
| Distribution | Ubuntu 24.04.4 LTS (noble) |
| Architecture | x86_64 |
| Docker | 29.4.0 |
| Docker Compose | v5.1.2 |
| GNU Make | 4.3 |
| Windows version | 10.0.26200.8246 |

---

## Part I: Bugs4Q Reproducibility Experiments

This part corresponds to the main reproducibility experiments conducted on the Bugs4Q-derived study snapshot under two dependency configurations.

### Directory Layout

```text
bugs4q_snapshots/
├── core-only/
│   ├── bugs4q/
│   ├── note/
│   │   └── criteria.md
│   ├── requirements/
│   ├── test-bugs4q/
│   ├── bash_setting
│   ├── docker-compose.yml
│   ├── Dockerfile.qiskit0
│   ├── Dockerfile.qiskit1
│   ├── Dockerfile.qiskit2
│   └── Makefile
└── pinned-stack/
    ├── bugs4q/
    ├── note/
    │   ├── breakage.md
    │   └── criteria.md
    ├── requirements/
    ├── test-bugs4q/
    ├── bash_setting
    ├── docker-compose.yml
    ├── Dockerfile.qiskit0
    ├── Dockerfile.qiskit1
    ├── Dockerfile.qiskit2
    └── Makefile
```

### Experimental Configurations

The main Bugs4Q reproducibility experiments are conducted under two configurations.

#### Core-only

`core-only` uses the core Qiskit library and the minimum surrounding package setup required by the experiment.
This configuration is intended to observe what happens when the core Qiskit library evolves while the surrounding ecosystem support is kept minimal.

#### Pinned-stack

`pinned-stack` uses a pinned set of Qiskit-related packages. This configuration is designed to reduce unnecessary dependency variation while keeping the target Qiskit core-library version fixed for each checkpoint.
This configuration is used as the basis for detailed root-cause analysis in the paper.

### Qiskit Version Tags

The main Bugs4Q snapshots use Docker Compose service names as version tags. These tags are passed to Makefile targets through the `v` argument.

For example:

```bash
make bs v=qiskit231
make uc v=qiskit231
```

builds and enters the environment for Qiskit 2.3.1.

The 0.x series tags keep the leading zero, such as `qiskit0231` for Qiskit 0.23.1, to avoid collision with 2.x tags such as `qiskit231` for Qiskit 2.3.1.

| Version tag | Qiskit series | Target Qiskit version |
|---|---:|---:|
| `qiskit0201` | 0.x | 0.20.1 |
| `qiskit0211` | 0.x | 0.21.1 |
| `qiskit0212` | 0.x | 0.21.2 |
| `qiskit0222` | 0.x | 0.22.2 |
| `qiskit0223` | 0.x | 0.22.3 |
| `qiskit0232` | 0.x | 0.23.2 |
| `qiskit0240` | 0.x | 0.24.0 |
| `qiskit100` | 1.x | 1.0.0 |
| `qiskit102` | 1.x | 1.0.2 |
| `qiskit110` | 1.x | 1.1.0 |
| `qiskit120` | 1.x | 1.2.0 |
| `qiskit124` | 1.x | 1.2.4 |
| `qiskit131` | 1.x | 1.3.1 |
| `qiskit132` | 1.x | 1.3.2 |
| `qiskit200` | 2.x | 2.0.0 |
| `qiskit202` | 2.x | 2.0.2 |
| `qiskit211` | 2.x | 2.1.1 |
| `qiskit221` | 2.x | 2.2.1 |
| `qiskit223` | 2.x | 2.2.3 |
| `qiskit230` | 2.x | 2.3.0 |
| `qiskit231` | 2.x | 2.3.1 |

### Makefile Targets

The two main snapshots under `bugs4q_snapshots/` use the same Makefile interface.
Move to one configuration snapshot:

```bash
cd bugs4q_snapshots/<configuration>
```

where `<configuration>` is one of:

```text
core-only
pinned-stack
```

The available Makefile targets are:

| Target | Description |
|---|---|
| `make b` | Build all Docker images for all Qiskit versions. |
| `make b0` | Build all Qiskit 0.x images. |
| `make b1` | Build all Qiskit 1.x images. |
| `make b2` | Build all Qiskit 2.x images. |
| `make bs v=<version-tag>` | Build one Docker image specified by `<version-tag>`. |
| `make u` | Start all containers. |
| `make us v=<version-tag>` | Start one container specified by `<version-tag>`. |
| `make c v=<version-tag>` | Connect to a running container. |
| `make uc v=<version-tag>` | Start one container and connect to it. |
| `make d` | Stop all containers. |
| `make clean-v v=<version-tag>` | Remove one service container and its local image. |
| `make clean-all` | Remove containers, images, volumes, custom networks, and build cache. Use with care. |
| `make help` | Show Makefile help. |

For example, to build and enter the Qiskit 2.3.1 environment:

```bash
make bs v=qiskit231
make uc v=qiskit231
```

### Reproduction Steps

Move to one of the two configuration snapshots.

```bash
cd bugs4q_snapshots/core-only
```

or

```bash
cd bugs4q_snapshots/pinned-stack
```

Build the target Docker environment. For example, to build the Qiskit 2.3.1 environment:

```bash
make bs v=qiskit231
```

Start and enter the corresponding container:

```bash
make uc v=qiskit231
```

Inside the container, move to the experiment script directory and run the main execution script:

```bash
cd test-bugs4q
python 01_execute_all_bugs4q.py
```

This script executes the buggy and fixed versions of each Bugs4Q artifact and stores the result CSV files and logs under `test-bugs4q/`.

Then aggregate the per-run results:

```bash
python 02_count_execution_results.py
```

This script reads `execution_results_qiskit-<version>.csv` and generates:

```text
count_execution_results_qiskit-<version>.csv
```

If the container is already running, reconnect to it with:

```bash
make c v=qiskit231
```

To stop containers after the experiment:

```bash
make d
```

### Script-to-Output Mapping

The main Bugs4Q experiment uses scripts under `test-bugs4q/`.

| Script | Purpose | Main outputs |
|---|---|---|
| `01_execute_all_bugs4q.py` | Executes the buggy and fixed versions of each Bugs4Q artifact for the current Qiskit environment. | `execution_results_qiskit-<version>.csv`; `logs/logs_qiskit-<version>/<artifact-id>/test_buggy_runXX.log`; `logs/logs_qiskit-<version>/<artifact-id>/test_fixed_runXX.log` |
| `02_count_execution_results.py` | Aggregates per-run execution outcomes by bug category and result class. | `count_execution_results_qiskit-<version>.csv` |

The exact `<version>` suffix is determined from the Qiskit version installed inside the Docker container.

### Expected Outputs

For each Qiskit version in each configuration snapshot, the expected result files are:

```text
test-bugs4q/execution_results_qiskit-<version>.csv
test-bugs4q/count_execution_results_qiskit-<version>.csv
test-bugs4q/logs/logs_qiskit-<version>/
```

The execution logs are organized by Qiskit version and artifact ID.

### Analysis Notes

In addition to the CSV files and raw logs., each Bugs4Q snapshot includes a `note/` directory. 
The `criteria.md` file is included in both `core-only` and `pinned-stack`, while `breakage.md` is included only in `pinned-stack`.

The files in `note/` record intermediate analysis results for the research questions. They are included to make the artifact-level judgments traceable. Unlike the paper tables, which report aggregated results, these notes may include the IDs of artifacts that satisfy each criterion or fall into each breakage category.

The currently included analysis-note files are:

| File | Configuration | Purpose |
|---|---|---|
| `note/criteria.md` | `core-only`, `pinned-stack` | Records criterion-level analysis results, including artifact IDs for reproducibility judgments. |
| `note/breakage.md` | `pinned-stack` | Records breakage-analysis results, including artifact IDs used in the root-cause analysis. |

These files are auxiliary analysis records. The authoritative executable evidence remains the preserved CSV files and raw logs under `test-bugs4q/`.

### Result File Semantics

The main Bugs4Q experiments produce two types of CSV files for each Qiskit version.

| File | Meaning |
|---|---|
| `execution_results_qiskit-<version>.csv` | Per-run execution outcomes for buggy and fixed programs. |
| `count_execution_results_qiskit-<version>.csv` | Aggregated counts derived from the execution-result CSV. |

The counts in `count_execution_results_qiskit-<version>.csv` are run-level counts, not artifact-level counts. For example, if one artifact is executed 30 times and all runs are classified as complete success, the corresponding count increases by 30.

The execution-result CSV files use the following columns.

| Column | Meaning | Possible values |
|---|---|---|
| `id` | Bugs4Q artifact ID. | Integer artifact ID. |
| `run` | Repetition index. | Integer from `1` to `30`. |
| `test_buggy` | Execution outcome of the test against the buggy program. | `Pass`, `Fail` |
| `test_fixed` | Execution outcome of the test against the fixed program. | `Pass`, `Fail` |

The count CSV files summarize the per-run outcomes by bug category and result class.

| Column | Meaning | Possible values |
|---|---|---|
| `Category` | Bugs4Q bug category used in the experiment. | `Output Wrong`, `Throw Exception`, `Simulation Failure` |
| `Result` | Aggregated result class. | `Complete Success`, `Partial Success`, `Failure` |
| `Count` | Number of runs in that result class. | Non-negative integer. |
| `IDs` | Artifact IDs that appeared in that result class. | Comma-separated artifact IDs. |

The result classes are defined as follows.

| Result | Definition |
|---|---|
| `Complete Success` | `test_buggy = Fail` and `test_fixed = Pass`. |
| `Partial Success` | `test_buggy = Fail` and `test_fixed = Fail`. |
| `Failure` | Any other combination. |

The execution logs are stored under:

```text
test-bugs4q/logs/logs_qiskit-<version>/
```

Each version-specific log directory contains logs grouped by artifact ID. These logs are the primary evidence used to inspect failure symptoms, exception types, and runtime messages.
The log directory has the following nested structure.

```text
test-bugs4q/
└── logs/
    └── logs_qiskit-<version>/
        └── <artifact-id>/
            ├── test_buggy_run01.log
            ├── test_buggy_run02.log
            ├── ...
            ├── test_buggy_run30.log
            ├── test_fixed_run01.log
            ├── test_fixed_run02.log
            ├── ...
            └── test_fixed_run30.log
```

For each artifact ID, the directory contains 60 logs in total: 30 logs for the buggy version and 30 logs for the fixed version.

### Setup Failures

Some configuration-version pairs fail before artifact execution because the Docker environment cannot be built or the Python package set cannot be installed.
In such cases, no artifact-level buggy/fixed execution logs are available. Instead, the corresponding version log directory contains `setup.log`. These cases should be interpreted as setup failures rather than artifact execution failures.

The setup-failure logs are stored as follows.

| Configuration | Version tag | Target Qiskit version | Status | Evidence log |
|---|---|---:|---|---|
| `core-only` | `qiskit200` | 2.0.0 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.0.0/setup.log` |
| `core-only` | `qiskit202` | 2.0.2 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.0.2/setup.log` |
| `core-only` | `qiskit211` | 2.1.1 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.1.1/setup.log` |
| `core-only` | `qiskit221` | 2.2.1 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.2.1/setup.log` |
| `core-only` | `qiskit223` | 2.2.3 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.2.3/setup.log` |
| `core-only` | `qiskit230` | 2.3.0 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.3.0/setup.log` |
| `core-only` | `qiskit231` | 2.3.1 | Setup failure | `bugs4q_snapshots/core-only/test-bugs4q/logs/logs_qiskit-2.3.1/setup.log` |

No setup failures were observed for `pinned-stack` in the released snapshots.

### Notes on Non-Determinism

Some Bugs4Q artifacts involve probabilistic quantum program outputs. To reduce the effect of sampling fluctuation on the reported results, each buggy/fixed pair is executed 30 times where applicable.
In the main experiment scripts, the buggy and fixed versions are repeatedly executed and the results are summarized in CSV files. The corresponding raw logs are preserved to allow inspection of individual runs.

---

## Part II: Bugs4Q-Robust Rerun Experiment

This part corresponds to the additional rerun experiment using the edited subject dataset stored in `bugs4q-robust_snapshot/`.
Bugs4Q-Robust is an edited study snapshot derived from the Bugs4Q artifacts. The edits are intended to make the artifacts executable under the target modern Qiskit environment while preserving the original bug-revealing intent where possible. Typical edits include adapting deprecated or removed Qiskit APIs, updating import paths, revising test oracles when output formats changed, and adjusting probabilistic execution settings for quantum-sampling behavior. The detailed repair rationale and classification are described in the submitted paper.

### Directory Layout

```text
bugs4q-robust_snapshot/
├── bugs4q-robust/
├── logs/
├── bash_setting
├── count_results.csv
├── count.py
├── Dockerfile
├── execution_results.csv
├── Makefile
├── requirements.txt
└── run.py
```

### Makefile Targets

The Bugs4Q-Robust rerun snapshot has a separate Makefile.
Move to the Bugs4Q-Robust snapshot:

```bash
cd bugs4q-robust_snapshot
```

The available Makefile targets are:

| Target | Description |
|---|---|
| `make b` | Build the Docker image. |
| `make u` | Start the container in the background. |
| `make c` | Connect to the running container. |
| `make uc` | Run and connect to the container interactively. |
| `make d` | Stop and remove the container. |
| `make re` | Remove the container, rebuild the image, and connect. |
| `make clean` | Remove the container, image, and dangling images. |
| `make help` | Show Makefile help. |

For example:

```bash
make b
make uc
```

### Reproduction Steps

Move to the Bugs4Q-Robust snapshot.

```bash
cd bugs4q-robust_snapshot
```

Build and enter the Docker environment.

```bash
make b
make uc
```

Inside the container, run the Bugs4Q-Robust experiment.

```bash
python run.py
```

This script executes each artifact in `bugs4q-robust/` and stores the execution results in:

```text
execution_results.csv
```

It also stores raw logs under:

```text
logs/
```

Aggregate the results.

```bash
python count.py
```

This generates:

```text
count_results.csv
```

After the experiment, stop and remove the container from another terminal if necessary:

```bash
make d
```

### Script-to-Output Mapping

The Bugs4Q-Robust rerun experiment uses the following scripts.

| Script | Purpose | Main outputs |
|---|---|---|
| `run.py` | Executes each buggy/fixed pair in `bugs4q-robust/` 30 times and stores per-run outcomes. | `execution_results.csv`; `logs/<artifact-id>/test_buggy_runXX.log`; `logs/<artifact-id>/test_fixed_runXX.log` |
| `count.py` | Aggregates the per-run outcomes by bug category and result class. | `count_results.csv` |

### Expected Outputs

The Bugs4Q-Robust snapshot produces:

```text
bugs4q-robust_snapshot/execution_results.csv
bugs4q-robust_snapshot/count_results.csv
bugs4q-robust_snapshot/logs/
```

### Result File Semantics

For Bugs4Q-Robust, `execution_results.csv` contains the per-run outcomes, `count_results.csv` contains aggregated counts, and `logs/` contains the corresponding raw execution logs.
The counts in `bugs4q-robust_snapshot/count_results.csv` are run-level counts, not artifact-level counts.
The Bugs4Q-Robust execution-result CSV uses the following columns.

| Column | Meaning | Possible values |
|---|---|---|
| `id` | Bugs4Q-Robust artifact ID. | Integer artifact ID. |
| `run` | Repetition index. | Integer from `1` to `30`. |
| `test_buggy` | Execution outcome of the test against the buggy program. | `Pass`, `Fail` |
| `test_fixed` | Execution outcome of the test against the fixed program. | `Pass`, `Fail` |

The Bugs4Q-Robust count CSV uses the following columns.

| Column | Meaning | Possible values |
|---|---|---|
| `Category` | Bug category used in the experiment. | `Output Wrong`, `Throw Exception`, `Simulation Failure` |
| `Result` | Aggregated result class. | `Complete Success`, `Partial Success`, `Failure` |
| `Count` | Number of runs in that result class. | Non-negative integer. |
| `IDs` | Artifact IDs that appeared in that result class. | Comma-separated artifact IDs. |

The result classes are defined as follows.

| Result | Definition |
|---|---|
| `Complete Success` | `test_buggy = Fail` and `test_fixed = Pass`. |
| `Partial Success` | `test_buggy = Fail` and `test_fixed = Fail`. |
| `Failure` | Any other combination. |

The Bugs4Q-Robust log directory has the following nested structure.

```text
logs/
└── <artifact-id>/
    ├── test_buggy_run01.log
    ├── test_buggy_run02.log
    ├── ...
    ├── test_buggy_run30.log
    ├── test_fixed_run01.log
    ├── test_fixed_run02.log
    ├── ...
    └── test_fixed_run30.log
```

For each artifact ID, the directory contains 60 logs in total: 30 logs for the buggy version and 30 logs for the fixed version.

### Notes on Non-Determinism

For Bugs4Q-Robust, `run.py` executes each artifact 30 times and stores both CSV summaries and per-run logs.

---

## Subject Programs and Licensing

The `bugs4q/` directories under `bugs4q_snapshots/` contain the subject programs used in the main reproducibility experiments.
These subject programs are derived from the original Bugs4Q dataset. Some artifacts were excluded or updated for the experimental protocol. Therefore, these directories should be interpreted as the study snapshot used in this paper, not as the unmodified original Bugs4Q dataset. Their reuse and redistribution should follow the licensing terms, if any, of the original Bugs4Q distribution. We do not claim a new license for those Bugs4Q-derived subject programs in this package.
The `bugs4q-robust/` directory under `bugs4q-robust_snapshot/` contains the edited subject programs used in the Bugs4Q-Robust rerun experiment. The Bugs4Q-Robust snapshot is included as part of the replication package so that the additional experiment reported in the paper can be traced to the exact edited programs and logs. It should not be confused with a standalone dataset release.
This replication package contains materials with different origins. The experiment scripts, Docker files, requirements files, execution logs, and aggregated result CSV files created by the authors will be licensed before public release. Until the licensing status is finalized, this package is provided for artifact review and reproducibility inspection only. Redistribution or reuse beyond artifact review should follow the licensing terms of the respective original sources.

## Citation

During double-blind review, citation, author, and contact information are intentionally redacted. They will be added before public release.
A `CITATION.cff` file will be added before public release. For artifact review, please refer to the submitted paper together with this replication package.

## Contact

During double-blind review, direct author contact information is intentionally redacted.
For artifact review, please contact the authors through the submission system. A public contact address will be added before release.