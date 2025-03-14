from svgpathtools import svg2paths
import json

file_name = "light_c"  # Keep this as a filename

# Load the SVG paths
paths, attributes = svg2paths(f'{file_name}.svg')  # Load the SVG file

# Extract the points from the paths
path_data = []

for path in paths:
    for segment in path:
        path_data.append({
            'start': {'x': segment.start.real, 'y': segment.start.imag},
            'end': {'x': segment.end.real, 'y': segment.end.imag}
        })

# Save the extracted data to a JSON file
with open(f'{file_name}.json', 'w') as f:
    json.dump(path_data, f)

print(f"Path data has been saved to '{file_name}.json'.")
