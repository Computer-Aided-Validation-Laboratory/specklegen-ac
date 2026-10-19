# Specklegen AC examples

This folder contains small, runnable scripts that demonstrate the public
`specklegen_ac.create_speckle_image` API. Each script creates a TIFF and opens
a Matplotlib preview. The scripts use a seeded NumPy random generator so that
the dot placement can be reproduced.

## Run an example

From the root of the repository, install the package and its dependencies:

```bash
python -m pip install -e .
```

Run any example from the repository root:

```bash
python examples/example01.py
python examples/example02_high_coverage.py
python examples/example03_white_dots.py
python examples/example04_size_variability.py
```

The TIFFs are saved in `examples/output/`. The folder is created automatically
the first time an example runs and is ignored by Git. A Matplotlib window
shows the preview; close the window to let the script finish. To run in a
headless environment, set a non-interactive Matplotlib backend, for example:

```bash
MPLBACKEND=Agg python examples/example01.py
```

## Examples

| Script | Demonstrates | Output |
| --- | --- | --- |
| [`example01.py`](example01.py) | Baseline pattern using the standard dimensions and a fixed random seed. | `output/example01-default.tif` |
| [`example02_high_coverage.py`](example02_high_coverage.py) | A higher target area coverage. Dense patterns can be harder to place without overlap. | `output/example02-high-coverage.tif` |
| [`example03_white_dots.py`](example03_white_dots.py) | White dots on a black background. | `output/example03-white-dots.tif` |
| [`example04_size_variability.py`](example04_size_variability.py) | A wider range of speckle diameters. | `output/example04-size-variability.tif` |

## Adjusting a pattern

Import the public function and pass only the options you want to change:

```python
from pathlib import Path

import numpy as np
from specklegen_ac import create_speckle_image

output_path = Path("speckle_pattern.tif")
figure, axis, stats = create_speckle_image(
    image_height=800,
    image_width=1000,
    maximum_speckle_diameter=6,
    speckle_target_coverage=0.5,
    output_path=output_path,
    rng=np.random.default_rng(42),
)
```

The function saves a TIFF, displays a Matplotlib preview, and returns
`(figure, axis, stats)`. The `stats` mapping contains:

| Key | Meaning |
| --- | --- |
| `dot_count` | Number of circular dots in the pattern. |
| `dot_density` | Number of dots per pixel squared (`dot_count / (image_width * image_height)`). |
| `actual_coverage` | Fraction of the canvas area covered by the dots. |

## Parameters

All parameters are optional. The defaults below describe the standard pattern.

| Parameter | Description | Default | Valid values |
| --- | --- | --- | --- |
| `image_height` | Image height in pixels. | `800` | Positive integer |
| `image_width` | Image width in pixels. | `1000` | Positive integer |
| `maximum_speckle_diameter` | Largest dot diameter in pixels. | `6` | Positive number |
| `image_resolution` | Export resolution in pixels per millimetre. | `800 / 25.4` | Positive number |
| `speckle_size_randomness` | Relative diameter range: `0` produces uniform sizes; values closer to `1` allow smaller dots. | `0.4` | `0 <= value < 1` |
| `speckle_target_coverage` | Target fraction of canvas area covered by dots. | `0.50` | `0 < value < 1` |
| `dot_color` | Dot color; the background is set to the opposite color. | `"black"` | `"black"` or `"white"` |
| `output_path` | Destination for the exported TIFF. | `"speckle_pattern.tif"` | File path |
| `rng` | NumPy random generator for reproducible placement. | `None` | `numpy.random.Generator` or `None` |

`image_resolution` controls the TIFF's physical print size, not its pixel
dimensions. The default corresponds to 800 pixels per inch because there are
25.4 millimetres in an inch.

## Notes

- Dots are circular and placed without overlap.
- A seeded `rng`, such as `np.random.default_rng(42)`, makes the generated
  placement reproducible.
- Very dense targets or small canvases may not leave enough room to place every
  dot. In that case, the generator raises a `RuntimeError`; lower
  `speckle_target_coverage`, reduce `maximum_speckle_diameter`, or increase the
  image dimensions.
- Invalid dimensions, resolutions, colors, and parameter ranges raise
  `ValueError`.
- The command-line entry point also generates the standard pattern:

  ```bash
  specklegen-ac
  # or
  python -m specklegen_ac
  ```
