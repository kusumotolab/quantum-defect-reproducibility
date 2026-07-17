# Third-Party Notices

The subject programs in this repository are NOT authored by us and are NOT covered by the LICENSE file in this repository.

## Bugs4Q-derived subject programs

Directories:
- bugs4q_snapshots/core-only/bugs4q/
- bugs4q_snapshots/pinned-stack/bugs4q/
- bugs4q-robust_snapshot/bugs4q-robust/

Origin:
Derived from the Bugs4Q dataset.
  Bugs4Q: https://github.com/Z-928/Bugs4Q-Framework

Modifications:
We modified these programs to run them in our experiments. Modifications include, but are not limited to:
  - adapting deprecated or removed Qiskit APIs,
  - updating import paths,
  - revising test oracles where output formats changed,
  - adjusting probabilistic execution settings for quantum-sampling behavior,
  - excluding or updating individual artifacts to fit the experimental protocol.
The detailed rationale and classification of these edits are described in the associated paper.

Rights and licensing:
Copyright in these subject programs remains with their original authors and contributors.
We claim no ownership and apply no license of our own to them.
Any reuse or redistribution must follow the terms of the original Bugs4Q distribution and of the upstream sources from which Bugs4Q was assembled.
These files are included solely to enable reproduction of the results in the associated paper.