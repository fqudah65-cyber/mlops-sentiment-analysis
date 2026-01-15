#!/bin/bash

# Initialize project directory structure
mkdir -p backend/src/{api,models,services,utils,config}
mkdir -p backend/tests/{unit,integration}
mkdir -p backend/azure_functions
mkdir -p frontend/src
mkdir -p docs
mkdir -p .github/workflows
mkdir -p docker

echo "Project structure initialized successfully"
