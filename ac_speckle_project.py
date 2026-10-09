# CAV Starter Pack
# Python Speckle Generator

# Setting up the environment for the speckle image generation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

MAXIMUM_PLACEMENT_ATTEMPTS = 10000
DISPLAY_DPI = 100


# Main speckle function
def create_speckle_image(
    # Default parameters for the speckle image generation
    image_height=800,  # pixels
    image_width=1000,  # pixels
    maximum_speckle_diameter=6,  # pixels
    image_resolution=800 / 25.4,
    speckle_size_randomness=0.4,
    speckle_target_coverage=0.50,
    dot_color="black",
    output_path="speckle_pattern.tif",
    rng=None,
    show=True,
):
    # Validate inputs and initialize RNG.
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

    # Calculate target area and initialize dot diameters.
    canvas_area = image_width * image_height
    target_dot_area = speckle_target_coverage * canvas_area
    minimum_diameter = maximum_speckle_diameter * (
        1 - speckle_size_randomness)
    diameters = []
    remaining_area = target_dot_area

    # Generate a set of dot diameters that matches the coverage target.
    while remaining_area > 0:
        diameter = rng.uniform(minimum_diameter, maximum_speckle_diameter)
        diameter_area = np.pi * (diameter / 2) ** 2
        if diameter_area >= remaining_area:
            diameters.append(np.sqrt(4 * remaining_area / np.pi))
            break
        diameters.append(diameter)
        remaining_area -= diameter_area

    radii = np.sort(np.asarray(diameters) / 2)[::-1]
    dot_count = len(radii)

    # Ensure the selected dot sizes fit in the image.
    if np.any(radii >= min(image_width, image_height) / 2):
        raise ValueError("The selected dot sizes do not fit inside the image")

    x_positions = np.empty(dot_count)
    y_positions = np.empty(dot_count)
    grid_cell_size = maximum_speckle_diameter
    occupied_cells = {}

    # Place dots on the canvas without overlap.
    for index, radius in enumerate(radii):
        for _ in range(MAXIMUM_PLACEMENT_ATTEMPTS):
            center_x = rng.uniform(radius, image_width - radius)
            center_y = rng.uniform(radius, image_height - radius)
            cell_x = int(center_x // grid_cell_size)
            cell_y = int(center_y // grid_cell_size)
            overlaps = False

            for neighbor_x in range(cell_x - 1, cell_x + 2):
                for neighbor_y in range(cell_y - 1, cell_y + 2):
                    for other_index in occupied_cells.get(
                        (neighbor_x, neighbor_y), ()
                    ):
                        distance_x = x_positions[other_index] - center_x
                        distance_y = y_positions[other_index] - center_y
                        minimum_distance = radii[other_index] + radius
                        if distance_x**2 + distance_y**2 < minimum_distance**2:
                            overlaps = True
                            break
                    if overlaps:
                        break
                if overlaps:
                    break

            if not overlaps:
                x_positions[index] = center_x
                y_positions[index] = center_y
                occupied_cells.setdefault((cell_x, cell_y), []).append(index)
                break
        else:
            raise RuntimeError(
                "Could not place all dots without overlap. Lower "
                "speckle_target_coverage or increase the image dimensions."
            )

    dot_density = dot_count / canvas_area
    actual_coverage = np.sum(np.pi * radii**2) / canvas_area

    figure, axis = plt.subplots(
        figsize=(
            image_width / DISPLAY_DPI,
            image_height / DISPLAY_DPI,
        ),
        dpi=DISPLAY_DPI,
    )
    figure.patch.set_facecolor(background_color)
    axis.set_facecolor(background_color)

    # Prevent circles from drawing with edges.
    # This avoids visual artifacts when dots are close together.
    for center_x, center_y, radius in zip(x_positions, y_positions, radii):
        axis.add_patch(
            Circle(
                (center_x, center_y),
                radius,
                facecolor=dot_color,
                edgecolor="none",
            )
        )

    # Configure the figure details.
    axis.set_xlim(0, image_width)
    axis.set_ylim(0, image_height)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("Width (pixels)")
    axis.set_ylabel("Height (pixels)")
    axis.set_title(f"{dot_count} dots | {actual_coverage:.1%} coverage")

    export_dpi = image_resolution * 25.4
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

    stats = {
        "dot_count": dot_count,
        "dot_density": dot_density,
        "actual_coverage": actual_coverage,
    }
    print(f"Dot count: {dot_count}")
    print(f"Dot density: {dot_density:.6f} dots/pixel²")
    print(f"Area coverage: {actual_coverage:.1%}")

    if show:
        plt.show()

    return figure, axis, stats


# Create the speckle image when the script is run directly.
if __name__ == "__main__":
    create_speckle_image()
    