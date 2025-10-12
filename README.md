# MLOps Project - Cloud Deployment

Projet MLOps simplifié avec déploiement cloud pour le TP.

## 🏗️ Structure du projet

```
mlops-project/
├── src/
│   ├── prepare.py      # Préparation des données
│   ├── train.py        # Entraînement avec MLflow
│   ├── evaluate.py     # Évaluation du modèle
│   ├── serve.py        # Service FastAPI
│   └── utils/
│       └── seed.py     # Utilitaires
├── data/               # Données (raw et prepared)
├── model/              # Modèles entraînés
├── evaluation/         # Résultats d'évaluation
├── params.yaml         # Paramètres du projet
├── dvc.yaml           # Pipeline DVC
├── requirements.txt    # Dépendances Python
├── Dockerfile         # Container Docker
└── .github/workflows/ # CI/CD GitHub Actions
```

## 🚀 Installation rapide

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer DVC
```bash
dvc remote add -d storage gs://mlops-project-storage
dvc remote modify storage projectname machledata-474307
```

### 3. Exécuter le pipeline
```bash
dvc repro
```

### 4. Tester le service
```bash
python src/serve.py
```

## ☁️ Configuration Google Cloud

### Variables d'environnement
```bash
export GOOGLE_CLOUD_PROJECT=machledata-474307
export MLFLOW_TRACKING_URI=gs://mlops-project-storage/mlflow
export MLFLOW_EXPERIMENT_NAME=mlops-experiment
```

### Secrets GitHub requis
- `GOOGLE_SERVICE_ACCOUNT_KEY`: Clé JSON du service account
- `GOOGLE_CLOUD_PROJECT`: `machledata-474307`

## 🔧 Utilisation

### Entraînement
```bash
python src/train.py data/prepared model
```

### Service API
```bash
python src/serve.py
# API disponible sur http://localhost:8000
```

### Docker
```bash
docker build -t mlops-service .
docker run -p 8000:8000 mlops-service
```

## 📊 Fonctionnalités

- ✅ Pipeline DVC avec Google Cloud Storage
- ✅ Tracking MLflow des expériences
- ✅ Service FastAPI pour l'inférence
- ✅ Containerisation Docker
- ✅ CI/CD avec GitHub Actions
- ✅ Déploiement Google Cloud Run

## 🎯 Endpoints API

- `GET /` - Health check
- `GET /health` - Status du service
- `POST /predict` - Prédiction d'image

### Exemple de prédiction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": [0.1, 0.2, ...],
    "image_shape": [32, 32, 1]
  }'
```