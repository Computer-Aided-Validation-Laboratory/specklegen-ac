"""Speckle size selection and non-overlapping placement."""

import numpy as np

MAXIMUM_PLACEMENT_ATTEMPTS = 10000


def generate_placement(
    *,
    image_width: int,
    image_height: int,
    maximum_speckle_diameter: float,
    speckle_size_randomness: float,
    speckle_target_coverage: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    canvas_area = image_width * image_height
    target_dot_area = speckle_target_coverage * canvas_area
    minimum_diameter = maximum_speckle_diameter * (
        1 - speckle_size_randomness
    )
    diameters = []
    remaining_area = target_dot_area

    while remaining_area > 0:
        diameter = rng.uniform(minimum_diameter, maximum_speckle_diameter)
        diameter_area = np.pi * (diameter / 2) ** 2
        if diameter_area >= remaining_area:
            diameters.append(np.sqrt(4 * remaining_area / np.pi))
            break
        diameters.append(diameter)
        remaining_area -= diameter_area

    radii = np.sort(np.asarray(diameters) / 2)[::-1]
    if np.any(radii >= min(image_width, image_height) / 2):
        raise ValueError("The selected dot sizes do not fit inside the image")

    dot_count = len(radii)
    x_positions = np.empty(dot_count)
    y_positions = np.empty(dot_count)
    occupied_cells: dict[tuple[int, int], list[int]] = {}

    for index, radius in enumerate(radii):
        for _ in range(MAXIMUM_PLACEMENT_ATTEMPTS):
            center_x = rng.uniform(radius, image_width - radius)
            center_y = rng.uniform(radius, image_height - radius)
            cell_x = int(center_x // maximum_speckle_diameter)
            cell_y = int(center_y // maximum_speckle_diameter)
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

    return x_positions, y_positions, radii
