# Cyborg Dragon Ball Super Robot Operational Status

This project provides a Python and Rust implementation for parsing a YAML file that contains the operational status of various cyborg robots inspired by characters from the Dragon Ball Super series. The YAML file is verified against a JSON schema, and the operational status is used to generate an HTML documentation page.

## Project description

In a world where the powerful warriors from Dragon Ball Super have been transformed into cyborgs, a system is required to monitor their operational status. This project ingests YAML files containing the details of various robots, each inspired by a Dragon Ball Super character, and their components, along with their operational statuses.

The system checks the YAML file against a predefined JSON schema to ensure that the data is consistent and well-structured. Once verified, the program generates an HTML documentation page that presents the operational status of each robot and its components.

Experience the fusion of Dragon Ball Super with cutting-edge robotics and witness the power of Goku, Vegeta, Beerus, and Whis in their new cyborg forms!

## Example output

The generated HTML page will display the robot operational status in a table format:


Robot Operational Status

```python
Cyborg Goku
  Component       | Status Level       | Description             | Unique ID | Action
  Kamehameha Arm  | operational        | Fully functional        | c001      | None
  Ultra Instinct Eye | needs_maintenance | Vision is slightly blurry | c002      | Calibrate Ultra Instinct Eye

Cyborg Vegeta
  Component       | Status Level       | Description             | Unique ID | Action
  Galick Gun Arm  | needs_repair       | Energy output is low    | c003      | Replace energy capacitor
  Saiyan Pride Sensor | operational    | Fully functional        | c004      | None

... (other robots and their components)
```

## Prerequisites

### Python
- Python 3.6 or higher
- Python packages: pyyaml, jsonschema, Jinja2
- 
### Rust
- Rust 1.54.0 or higher
- Rust packages (crates): serde, serde_yaml, serde_json, valico, tera

## Setting up the development environment

### Python
1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3.Install the required packages:
```bash
pip install pyyaml jsonschema Jinja2
```


### Rust
1. Install Rust from the official website: https://www.rust-lang.org/tools/install
2. In the project directory, create a new Rust project:
```bash
cargo init
```

3. Add the required dependencies to the Cargo.toml file:
```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_yaml = "0.8"
serde_json = "1.0"
valico = "3.6"
tera = "1.12"
```

4. Run cargo build to download and compile the dependencies.


## Running the programs

### Python
Execute the Python script:

```bash
python dbzpy/ingest.py
```

### Rust
Build and run the Rust project:
```bash
cargo run
```