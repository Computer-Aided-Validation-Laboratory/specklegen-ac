"""Public API for generating and exporting speckle patterns."""

from os import PathLike
from typing import Literal

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._placement import generate_placement
from ._rendering import create_preview, save_tiff


def create_speckle_image(
    image_height: int = 800,
    image_width: int = 1000,
    maximum_speckle_diameter: float = 6,
    image_resolution: float = 800 / 25.4,
    speckle_size_randomness: float = 0.4,
    speckle_target_coverage: float = 0.50,
    dot_color: Literal["black", "white"] = "black",
    output_path: str | PathLike[str] = "speckle_pattern.tif",
    rng: np.random.Generator | None = None,
) -> tuple[Figure, Axes, dict[str, int | float]]:
    """Create a pattern, save it as TIFF, show its preview, and return statistics."""
    if image_height <= 0 or image_width <= 0:
        raise ValueError("Image dimensions must be positive")
    if maximum_speckle_diameter <= 0:
        raise ValueError("maximum_speckle_diameter must be positive")
    if image_resolution <= 0:
        raise ValueError("image_resolution must be positive")
    if not 0 <= speckle_size_randomness < 1:
        raise ValueError(
            "speckle_size_randomness must be between 0 (inclusive) and 1"
        )
    if not 0 < speckle_target_coverage < 1:
        raise ValueError("speckle_target_coverage must be between 0 and 1")
    if dot_color not in {"black", "white"}:
        raise ValueError("dot_color must be 'black' or 'white'")
    if rng is None:
        rng = np.random.default_rng()

    background_color = "white" if dot_color == "black" else "black"
    canvas_area = image_width * image_height
    x_positions, y_positions, radii = generate_placement(
        image_width=image_width,
        image_height=image_height,
        maximum_speckle_diameter=maximum_speckle_diameter,
        speckle_size_randomness=speckle_size_randomness,
        speckle_target_coverage=speckle_target_coverage,
        rng=rng,
    )
    dot_count = len(radii)
    dot_density = dot_count / canvas_area
    actual_coverage = np.sum(np.pi * radii**2) / canvas_area

    figure, axis = create_preview(
        image_width=image_width,
        image_height=image_height,
        x_positions=x_positions,
        y_positions=y_positions,
        radii=radii,
        dot_color=dot_color,
        background_color=background_color,
        dot_count=dot_count,
        actual_coverage=actual_coverage,
    )
    export_dpi = image_resolution * 25.4
    save_tiff(
        output_path=output_path,
        image_width=image_width,
        image_height=image_height,
        export_dpi=export_dpi,
        x_positions=x_positions,
        y_positions=y_positions,
        radii=radii,
        dot_color=dot_color,
        background_color=background_color,
    )

    stats = {
        "dot_count": dot_count,
        "dot_density": dot_density,
        "actual_coverage": actual_coverage,
    }
    print(f"Dot count: {dot_count}")
    print(f"Dot density: {dot_density:.6f} dots/pixel²")
    print(f"Area coverage: {actual_coverage:.1%}")

    plt.show()

    return figure, axis, stats


    