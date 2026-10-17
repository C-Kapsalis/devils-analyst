"""Build every benchmark case: runs each cases/*.py, which simulates data, computes
ground truth, asserts the naive answer differs, and writes the case files."""

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

only = set(sys.argv[1:])
for script in sorted((HERE / "cases").glob("*.py")):
    if only and script.stem not in only:
        continue
    runpy.run_path(str(script), run_name="__main__")
    print(f"built {script.stem}")
