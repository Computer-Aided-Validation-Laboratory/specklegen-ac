# specklegen-ac

## The following package generates a speckle pattern that can be configured based on user inputs.

The function create_speckle_image() can be called to create a pattern with default values, or can be called with user specified values.

In order, the following parameters can be adjusted:
- image_height in pixels,
- image_width in pixels,
- maximum_speckle_diameter in pixels,
- image_resolution in pixels per square mm for exporting,
- speckle_size_randomness as a value from 0-1,
- speckle_target_coverage as a value from 0-1,
- dot_color as either "black" or "white", with the background colour changing to match,
- output_path in naming the speckle patten saved,
- show whether the graph is shown as well as the export created.

A photo is automatically saved when using this function, similar to the image seen below. This photo was created using the default values within the function.
![Example of Speckle Pattern Image] (../../../../..)

The following is the figure produced in matplotlib, using the default values. This is useful when adjusting the speckle and image size, viewing the speckle pattern layout in terms of pixels.
![Example of Speckle Figure](<Example of figure.png>)

Default parameters:
- image_height=800
- image_width=1000
- maximum_speckle_diameter=6
- image_resolution=800 / 25.4
- speckle_size_randomness=0.4
- speckle_target_coverage=0.50
- dot_color="black"
- output_path="speckle_pattern.tif"
- show=True