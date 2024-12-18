import os
import yaml
from jinja2 import Template

# Load default rules
rules_file = os.path.join(os.path.dirname(__file__), "default.yml")
with open(rules_file, "r") as f:
    ruleset = yaml.safe_load(f)

# Variables for template rendering
city = "Paris"
postal_code = "75013"

# Render each rule template
rendered_rules = []
for rule in ruleset["rules"]:
    template = Template(rule["template"])
    rendered = template.render(city=city, postal_code=postal_code)
    rendered_rules.append(rendered)

print(rendered_rules)