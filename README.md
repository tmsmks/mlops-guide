# MLOps Project

This is a machine learning operations project that demonstrates the use of DVC (Data Version Control) for managing ML experiments.

## Project Structure

- `src/` - Source code for the ML pipeline
- `data/` - Data storage (raw and prepared datasets)
- `model/` - Trained model artifacts
- `evaluation/` - Model evaluation results and plots
- `params.yaml` - Experiment parameters
- `dvc.yaml` - DVC pipeline configuration

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the pipeline:
   ```bash
   dvc repro
   ```

## Pipeline Stages

1. **Prepare** - Data preprocessing and preparation
2. **Train** - Model training
3. **Evaluate** - Model evaluation and metrics generation