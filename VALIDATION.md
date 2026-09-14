# Local validation

Validated on 14 September 2026 on Linux, in a fresh virtual environment installed from `requirements.txt`.

| Component | Tested version |
| --- | --- |
| Python | 3.14.4 |
| NumPy | 2.5.3 |
| pandas | 3.0.5 |
| matplotlib | 3.11.2 |
| Pillow | 12.3.0 |
| opencv-python-headless | 5.0.0.93 |
| nbformat / nbclient | 5.11.1 / 0.11.0 |
| ipykernel / JupyterLab | 7.3.0 / 4.6.3 |

Command: `python run_notebook.py`

Passed:

- Notebook schema validation and execution from the repository root.
- Exact proposal-count agreement on all 12 RGB-D pairs.
- Empty image produces no proposals.
- Noncommuting relative-motion composition has the expected position/yaw.
- All 100 baseline and fused position/yaw estimates are finite.
- Removing every `gt_*` column leaves the seeded fused output unchanged.

Observed sample output:

```text
generated counts: [1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1]
camera accepted: 99; unavailable/rejected: 1
10 s snippet baseline RMSE: 1.111 m
10 s snippet fused RMSE:    0.344 m
```

The full-run reference metrics printed in the notebook are historical values. This sample execution does not regenerate the full-sequence tracker, bootstrap, or evaluation.

Source notebooks are stored without outputs for readable Git changes. The runner writes an executed copy (including smoke-check results) to `outputs/`, which is ignored by Git. The original edited notebook and its saved output remain in the separate submission package.
