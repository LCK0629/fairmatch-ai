from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .models import load_allocation_input
from .solver import solve_allocation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a FairMatch AI allocation sample.")
    parser.add_argument("--input", required=True, help="Path to a FairMatch JSON input file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    problem = load_allocation_input(payload)
    result = solve_allocation(problem)

    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()