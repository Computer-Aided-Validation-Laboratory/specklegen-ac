"""Matplotlib preview and TIFF rendering."""

from os import PathLike
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle

DISPLAY_DPI = 100


def create_preview(
    *,
    image_width: int,
    image_height: int,
    x_positions: np.ndarray,
    y_positions: np.ndarray,
    radii: np.ndarray,
    dot_color: Literal["black", "white"],
    background_color: Literal["black", "white"],
    dot_count: int,
    actual_coverage: float,
) -> tuple[Figure, Axes]:
    figure, axis = plt.subplots(
        figsize=(image_width / DISPLAY_DPI, image_height / DISPLAY_DPI),
        dpi=DISPLAY_DPI,
    )
    figure.patch.set_facecolor(background_color)
    axis.set_facecolor(background_color)

    for center_x, center_y, radius in zip(x_positions, y_positions, radii):
        axis.add_patch(
            Circle(
                (center_x, center_y),
                radius,
                facecolor=dot_color,
                edgecolor="none",
            )
        )

    axis.set_xlim(0, image_width)
    axis.set_ylim(0, image_height)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("Width (pixels)")
    axis.set_ylabel("Height (pixels)")
    axis.set_title(f"{dot_count} dots | {actual_coverage:.1%} coverage")
    return figure, axis


def save_tiff(
    *,
    output_path: str | PathLike[str],
    image_width: int,
    image_height: int,
    export_dpi: float,
    x_positions: np.ndarray,
    y_positions: np.ndarray,
    radii: np.ndarray,
    dot_color: Literal["black", "white"],
    background_color: Literal["black", "white"],
) -> None:
    export_figure = plt.figure(
        figsize=(image_width / export_dpi, image_height / export_dpi),
        dpi=export_dpi,
        facecolor=background_color,
    )
    export_axis = export_figure.add_axes([0, 0, 1, 1])
    export_axis.set_facecolor(background_color)
    export_axis.set_xlim(0, image_width)
    export_axis.set_ylim(0, image_height)
    export_axis.set_aspect("equal", adjustable="box")
    export_axis.set_axis_off()

    for center_x, center_y, radius in zip(x_positions, y_positions, radii):
        export_axis.add_patch(
            Circle(
                (center_x, center_y),
                radius,
                facecolor=dot_color,
                edgecolor="none",
            )
        )

    try:
        export_figure.savefig(
            output_path,
            format="tiff",
            dpi=export_dpi,
            facecolor=background_color,
            edgecolor=background_color,
        )
    finally:
        plt.close(export_figure)
