"""Execute the fusion notebook and smoke checks; save results under outputs/."""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / 'notebooks/02_rgbd_uwb_particle_fusion.ipynb'

CHECKS = '''
assert np.isfinite(baseline).all() and np.isfinite(fused).all()
assert baseline.shape == fused.shape == (len(data), 3)
assert generate_candidates(np.zeros((720,1280,3), dtype=np.uint8),
                           np.zeros((720,1280), dtype=np.uint16)) == []
# An observer translating in its rotated frame must left-compose the inverse.
state = np.array([[2., 1., np.pi / 2]])
predicted = left_compose(inverse(np.array([1., 0., np.pi / 2])),
                        compose_batch(state, np.array([1., 0., 0.])))
np.testing.assert_allclose(predicted, [[2., -1., 0.]], atol=1e-12)
# Removing protected columns must leave the seeded online filter identical.
data = data.drop(columns=[c for c in data.columns if c.startswith('gt_')])
rng = np.random.default_rng(7)
np.testing.assert_allclose(run_filter(True), fused, atol=1e-12, rtol=0)
print('PASS: proposals, empty image, pose composition, finite estimates, GT-independent filtering')
'''


if __name__ == '__main__':
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    notebook.cells.append(nbformat.v4.new_code_cell(CHECKS))
    NotebookClient(notebook, timeout=600, kernel_name='python3',
                   resources={'metadata': {'path': str(ROOT)}}).execute()
    output = ROOT / 'outputs' / NOTEBOOK.name
    output.parent.mkdir(exist_ok=True)
    nbformat.write(notebook, output)
    for cell in notebook.cells:
        for result in cell.get('outputs', []):
            if result.output_type == 'stream':
                print(result.text, end='')
    print(f'Executed notebook: {output}')
