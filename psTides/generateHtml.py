import json
import os
# print("Current Working Directory:", os.getcwd())

with open('tide_data.json') as f:
    tide_data = json.load(f)
    
# # Set up Jinja2 template environment
# env = Environment(loader=FileSystemLoader('templates'))
# template = env.get_template('tide_template.html')

# # Render the template with tide data
# output = template.render(tides=tide_data['predictions'])

# # Save the output to an HTML file
# with open('output/tides.html', 'w') as f:
#     f.write(output)