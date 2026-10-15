"""Generate a baseline speckle pattern using the standard settings."""

from pathlib import Path

import numpy as np

from specklegen_ac import create_speckle_image

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_speckle_image(
        output_path=OUTPUT_DIR / "example01-default.tif",
        rng=np.random.default_rng(42),
    )


if __name__ == "__main__":
    main()