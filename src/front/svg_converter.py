from svgpathtools import svg2paths
import json

# Load the SVG paths
paths, attributes = svg2paths('path1.svg')  # Replace with your SVG file path

# Extract the points from the paths
path_data = []

for path in paths:
    for segment in path:
        path_data.append({
            'start': {'x': segment.start.real, 'y': segment.start.imag},
            'end': {'x': segment.end.real, 'y': segment.end.imag}
        })

# Save the extracted data to a JSON file
with open('path_data.json', 'w') as f:
    json.dump(path_data, f)

print("Path data has been saved to 'path_data.json'.")
