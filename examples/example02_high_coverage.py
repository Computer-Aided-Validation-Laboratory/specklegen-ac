"""Generate a pattern with a higher target area coverage."""

from pathlib import Path

import numpy as np

from specklegen_ac import create_speckle_image

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_speckle_image(
        image_height=800,
        image_width=1000,
        maximum_speckle_diameter=6,
        speckle_target_coverage=0.55,
        output_path=OUTPUT_DIR / "example02-high-coverage.tif",
        rng=np.random.default_rng(2025),
    )


if __name__ == "__main__":
    main()
