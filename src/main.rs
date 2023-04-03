use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use serde_json::{Value};
use valico::json_schema;
use tera::{Tera};

#[derive(Debug, Serialize, Deserialize)]
struct Status {
    level: String,
    description: String,
    unique_id: String,
    action: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct Component {
    name: String,
    status: Status,
}

#[derive(Debug, Serialize, Deserialize)]
struct Robot {
    name: String,
    components: Vec<Component>,
}

fn load_yaml(file_path: &Path) -> Result<Vec<Robot>, Box<dyn std::error::Error>> {
    let mut file = File::open(file_path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let data: serde_yaml::Value = serde_yaml::from_str(&contents)?;
    let robots = serde_yaml::from_value::<Vec<Robot>>(data["robots"].clone())?;

    // Load schema and validate
    let mut schema_file = File::open("robot_operational_status_schema.json")?;
    let mut schema_contents = String::new();
    schema_file.read_to_string(&mut schema_contents)?;
    let schema_json: Value = serde_json::from_str(&schema_contents)?;

    let mut scope = json_schema::Scope::new();
    let schema = scope.compile_and_return(schema_json, false)?;
    let validation = schema.validate(&serde_json::to_value(data)?);

    if !validation.is_valid() {
        for error in validation.errors {
            eprintln!("Validation error: {:?}", error);
        }
        return Err("Invalid YAML data".into());
    }

    Ok(robots)
}

fn render_html(robots: &Vec<Robot>) -> String {
    let template_str = r#"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Operational Status</title>
</head>
<body>
    <h1>Robot Operational Status</h1>
    {% for robot in robots %}
    <h2>{{ robot.name }}</h2>
    <table border="1">
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
"#;

let mut context = tera::Context::new();
context.insert("robots", robots);

let tera = match Tera::one_off(template_str, &context, false) {
    Ok(s) => s,
    Err(e) => panic!("Template error: {:?}", e),
};
    tera
}

fn main() {
    let robots = load_yaml(Path::new("robot_operational_status.yaml")).expect("Failed to load YAML");
    let html_output = render_html(&robots);

    let mut html_file = File::create("robot_operational_status_rs.html").expect("Failed to create HTML file");
    html_file.write_all(html_output.as_bytes()).expect("Failed to write to HTML file");
}   