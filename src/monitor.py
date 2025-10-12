"""
Model monitoring and drift detection
"""
import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.metrics import accuracy_score, classification_report
import mlflow
from mlflow_config import setup_mlflow_tracking

class ModelMonitor:
    def __init__(self, model_name="cifar10-cnn"):
        self.model_name = model_name
        setup_mlflow_tracking()
        self.client = mlflow.tracking.MlflowClient()
    
    def get_model_performance(self, days_back=7):
        """Get model performance metrics for the last N days"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_back)
        
        # Get runs from the last N days
        runs = self.client.search_runs(
            experiment_ids=[mlflow.get_experiment_by_name("mlops-experiment").experiment_id],
            filter_string=f"start_time >= {start_time.timestamp()}"
        )
        
        performance_data = []
        for run in runs:
            if run.data.metrics:
                performance_data.append({
                    'run_id': run.info.run_id,
                    'start_time': run.info.start_time,
                    'val_accuracy': run.data.metrics.get('final_val_accuracy', 0),
                    'val_loss': run.data.metrics.get('final_val_loss', 0),
                    'train_accuracy': run.data.metrics.get('final_train_accuracy', 0),
                    'train_loss': run.data.metrics.get('final_train_loss', 0)
                })
        
        return pd.DataFrame(performance_data)
    
    def detect_performance_drift(self, threshold=0.05):
        """Detect if model performance has degraded significantly"""
        performance_df = self.get_model_performance()
        
        if len(performance_df) < 2:
            return {"drift_detected": False, "message": "Insufficient data for drift detection"}
        
        # Compare latest performance with historical average
        latest_performance = performance_df.iloc[-1]['val_accuracy']
        historical_avg = performance_df.iloc[:-1]['val_accuracy'].mean()
        
        performance_drop = historical_avg - latest_performance
        
        drift_detected = performance_drop > threshold
        
        return {
            "drift_detected": drift_detected,
            "latest_accuracy": latest_performance,
            "historical_avg": historical_avg,
            "performance_drop": performance_drop,
            "threshold": threshold,
            "message": f"Performance drift detected: {performance_drop:.4f} drop" if drift_detected else "No significant drift detected"
        }
    
    def generate_monitoring_report(self):
        """Generate comprehensive monitoring report"""
        performance_df = self.get_model_performance()
        drift_analysis = self.detect_performance_drift()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "model_name": self.model_name,
            "total_runs": len(performance_df),
            "latest_accuracy": performance_df.iloc[-1]['val_accuracy'] if len(performance_df) > 0 else None,
            "average_accuracy": performance_df['val_accuracy'].mean() if len(performance_df) > 0 else None,
            "drift_analysis": drift_analysis,
            "performance_trend": "improving" if len(performance_df) > 1 and performance_df['val_accuracy'].iloc[-1] > performance_df['val_accuracy'].iloc[-2] else "declining"
        }
        
        return report
    
    def save_monitoring_report(self, output_path="monitoring/report.json"):
        """Save monitoring report to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        report = self.generate_monitoring_report()
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Monitoring report saved to {output_path}")
        return report

def main():
    """Main monitoring function"""
    monitor = ModelMonitor()
    
    # Generate and save monitoring report
    report = monitor.save_monitoring_report()
    
    # Print summary
    print("\n=== Model Monitoring Report ===")
    print(f"Model: {report['model_name']}")
    print(f"Total runs: {report['total_runs']}")
    print(f"Latest accuracy: {report['latest_accuracy']:.4f}")
    print(f"Average accuracy: {report['average_accuracy']:.4f}")
    print(f"Performance trend: {report['performance_trend']}")
    print(f"Drift detected: {report['drift_analysis']['drift_detected']}")
    
    if report['drift_analysis']['drift_detected']:
        print(f"⚠️  WARNING: {report['drift_analysis']['message']}")
    else:
        print("✅ Model performance is stable")

if __name__ == "__main__":
    main()