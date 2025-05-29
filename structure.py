import os
from pathlib import Path
from rich.console import Console

# Initialize logger
console = Console()

# Project name
project_name = "src"

# List of files to create
list_of_files = [
    f"{project_name}/__init__.py",

    # Components
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",  
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",

    # Configuration
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongo_db_connection.py",
    f"{project_name}/configuration/aws_connection.py",

    # Cloud Storage
    f"{project_name}/cloud_storage/__init__.py",
    f"{project_name}/cloud_storage/aws_storage.py",

    # Data Access Layer
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/data_access/proj1_data.py",

    # Constants and Entities
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/estimator.py",
    f"{project_name}/entity/s3_estimator.py",

    # Logger and Exception
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",

    # Pipelines
    f"{project_name}/pipline/__init__.py",
    f"{project_name}/pipline/training_pipeline.py",
    f"{project_name}/pipline/prediction_pipeline.py",

    # Utilities
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",

    # Root level
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    ".gitignore",
    "demo.py",
    "setup.py",
    "pyproject.toml",
    "README.md",
    
    # Configs
    "config/model.yaml",
    "config/schema.yaml",
]

# Create files and folders
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent

    # Create directory if not exists
    if not filedir.exists():
        filedir.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]Created directory:[/green] {filedir}")

    # Create file if not exists or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass  # Leave it empty for now
        console.print(f"[blue]Created file:[/blue] {filepath}")
    else:
        console.print(f"[yellow]File already exists and is not empty:[/yellow] {filepath}")
