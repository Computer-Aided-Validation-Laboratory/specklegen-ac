"""Generate a pattern with a wider range of speckle diameters."""

from pathlib import Path

import numpy as np

from specklegen_ac import create_speckle_image

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_speckle_image(
        maximum_speckle_diameter=8,
        speckle_size_randomness=0.75,
        output_path=OUTPUT_DIR / "example04-size-variability.tif",
        rng=np.random.default_rng(7),
    )


if __name__ == "__main__":
    main()
