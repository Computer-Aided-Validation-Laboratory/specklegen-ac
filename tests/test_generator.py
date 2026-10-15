import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest
from PIL import Image

from specklegen_ac import create_speckle_image
from specklegen_ac._placement import generate_placement


def test_generate_placement_matches_target_coverage() -> None:
    x_positions, y_positions, radii = generate_placement(
        image_width=160,
        image_height=120,
        maximum_speckle_diameter=6,
        speckle_size_randomness=0.4,
        speckle_target_coverage=0.2,
        rng=np.random.default_rng(42),
    )

    assert len(x_positions) == len(y_positions) == len(radii)
    assert np.all((x_positions >= radii) & (x_positions <= 160 - radii))
    assert np.all((y_positions >= radii) & (y_positions <= 120 - radii))
    assert np.sum(np.pi * radii**2) / (160 * 120) == pytest.approx(0.2)

    for index, radius in enumerate(radii):
        distances_squared = (
            (x_positions[index + 1 :] - x_positions[index]) ** 2
            + (y_positions[index + 1 :] - y_positions[index]) ** 2
        )
        minimum_distances = radius + radii[index + 1 :]
        assert np.all(distances_squared >= minimum_distances**2)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"image_height": 0}, "Image dimensions"),
        ({"maximum_speckle_diameter": 0}, "maximum_speckle_diameter"),
        ({"image_resolution": 0}, "image_resolution"),
        ({"speckle_size_randomness": 1}, "speckle_size_randomness"),
        ({"speckle_target_coverage": 1}, "speckle_target_coverage"),
        ({"dot_color": "blue"}, "dot_color"),
    ],
)
def test_create_speckle_image_rejects_invalid_parameters(
    kwargs: dict[str, object], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        create_speckle_image(**kwargs)


def test_create_speckle_image_exports_tiff_and_returns_stats(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)
    output_path = tmp_path / "speckles.tif"

    figure, axis, stats = create_speckle_image(
        image_height=80,
        image_width=100,
        maximum_speckle_diameter=5,
        image_resolution=10,
        speckle_target_coverage=0.1,
        output_path=output_path,
        rng=np.random.default_rng(7),
    )

    assert output_path.is_file()
    with Image.open(output_path) as image:
        assert image.format == "TIFF"
        assert image.size == (100, 80)
    assert stats["dot_count"] > 0
    assert stats["dot_density"] == pytest.approx(stats["dot_count"] / 8000)
    assert stats["actual_coverage"] == pytest.approx(0.1)
    assert axis.get_title().startswith(f"{stats['dot_count']} dots")
    figure.clear()
