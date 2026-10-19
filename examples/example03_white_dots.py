"""Generate white dots on a black background."""

from pathlib import Path

import numpy as np

from specklegen_ac import create_speckle_image

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_speckle_image(
        dot_color="white",
        output_path=OUTPUT_DIR / "example03-white-dots.tif",
        rng=np.random.default_rng(42),
    )


if __name__ == "__main__":
    main()
