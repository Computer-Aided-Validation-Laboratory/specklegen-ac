# specklegen-ac

## The following package generates a speckle pattern [consisting of x y z].

The function create_speckle_image() can be called to create a patten with default values or can be called with specific values.

In order, the following parameters can be adjusted:
- image_height in pixels,
- image_width in pixels,
- maximum_speckle_diameter in pixels,
- image_resolution in pixels per square mm for exporting,
- speckle_size_randomness as a value from 0-1,
- speckle_target_coverage as a value from 0-1,
- dot_color as either "black" or "white", with the background collour changing to match,
- output_path in naming the speckle patten saved,
- show whether the graph is shown as well as the export created.

Default parameters:
image_height=800,  # pixels
image_width=1000,  # pixels
maximum_speckle_diameter=6,  # pixels
image_resolution=800 / 25.4,
speckle_size_randomness=0.4,
speckle_target_coverage=0.50,
dot_color="black",
output_path="speckle_pattern.tif",
rng=None,
show=True