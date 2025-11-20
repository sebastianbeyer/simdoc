#!/usr/bin/env python3

import yaml
import glob
import os
import re
from jinja2 import Environment, FileSystemLoader

DATA_DIR = "data"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Load templates
base_tpl = env.get_template("base.html.j2")
sim_tpl = env.get_template("simulation.html.j2")

# Load YAML data
simulations = []

for path in sorted(glob.glob(f"{DATA_DIR}/*.yaml")):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    # Create slug from filename
    slug = os.path.splitext(os.path.basename(path))[0]
    slug = re.sub(r'[^a-zA-Z0-9_-]', '-', slug)
    print(slug)
    data["slug"] = slug

    simulations.append(data)

# Generate pages
for sim in simulations:


    mars_lines = ["retrieve,"]
    for key, value in sim["data-access"].items():
        mars_lines.append(f"  {key}={value},")
    sim["mars_example"] = "\n".join(mars_lines)

    poly_lines = ["request = { "]
    for key, value in sim["data-access"].items():
        poly_lines.append(f"  '{key}': '{value}',")
    sim["polytope_example"] = "\n".join(poly_lines)

    #print(mars_lines)
    #print(poly_lines)

    print(sim)


    content = sim_tpl.render(sim=sim)
    page = base_tpl.render(
        page_title=sim["title"],
        content=content,
        simulations=simulations,
    )

    out_path = os.path.join(OUTPUT_DIR, f"{sim['slug']}.html")
    with open(out_path, "w") as f:
        f.write(page)

print(f"Generated {len(simulations)} pages into '{OUTPUT_DIR}/'")

