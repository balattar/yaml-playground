import json
import yaml
from jsonschema import validate
from dataclasses import dataclass
from typing import List
from jinja2 import Template

@dataclass
class Status:
    level: str
    description: str
    unique_id: str
    action: str

@dataclass
class Component:
    name: str
    status: Status

@dataclass
class Robot:
    name: str
    components: List[Component]

def load_yaml(file_path: str) -> List[Robot]:
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        
        with open("./spec/robot_operational_status_schema.json", 'r') as schema_file:
            schema = json.load(schema_file)
            validate(data, schema)

        robots = []
        for robot in data['robots']:
            components = [Component(name=component['name'],
                                    status=Status(level=component['status']['level'],
                                                  description=component['status']['description'],
                                                  unique_id=component['status']['unique_id'],
                                                  action=component['status']['action']))
                          for component in robot['components']]
            robots.append(Robot(name=robot['name'], components=components))
        return robots

def render_html(robots: List[Robot]) -> str:
    template_str = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Operational Status</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #F8F8F8;
            color: #333;
        }
        h1 {
            font-size: 36px;
            color: #E74C3C;
        }
        h2 {
            font-size: 28px;
            color: #3498DB;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th {
            background-color: #34495E;
            color: #FFF;
            font-weight: bold;
            padding: 8px;
        }
        td {
            border: 1px solid #DDD;
            padding: 8px;
        }
        tr:nth-child(even) {
            background-color: #F2F2F2;
        }
    </style>
</head>
<body>
    <h1>Robot Operational Status</h1>
    {% for robot in robots %}
    <h2>{{ robot.name }}</h2>
    <img src="../static/{{ robot.name | lower }}.jpeg" alt="{{ robot.name }} Image" width="200" />
    <table>
        <thead>
            <tr>
                <th>Component</th>
                <th>Status Level</th>
                <th>Description</th>
                <th>Unique ID</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for component in robot.components %}
            <tr>
                <td>{{ component.name }}</td>
                <td>{{ component.status.level }}</td>
                <td>{{ component.status.description }}</td>
                <td>{{ component.status.unique_id }}</td>
                <td>{{ component.status.action }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endfor %}
</body>
</html>
'''
    template = Template(template_str)
    return template.render(robots=robots)

if __name__ == "__main__":
    robots = load_yaml("./spec/robot_operational_status.yaml")
    html_output = render_html(robots)
    
    with open("./out/robot_operational_status_py.html", "w") as html_file:
        html_file.write(html_output)
