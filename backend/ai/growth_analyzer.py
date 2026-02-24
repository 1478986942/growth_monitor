import numpy as np
from datetime import datetime, date
from typing import List, Dict, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

class GrowthAnalyzer:
    def __init__(self, model_dir='backend/ai/models'):
        self.model_dir = model_dir
        self.stunting_model = None
        self.obesity_model = None
        self.scaler = None
        
        self.height_percentiles = self._load_height_percentiles()
        self.weight_percentiles = self._load_weight_percentiles()
        self.bmi_percentiles = self._load_bmi_percentiles()
        
        os.makedirs(model_dir, exist_ok=True)
        
        self._load_models()

    def _load_height_percentiles(self):
        return {
            'male': {
                0: [49.9, 51.2, 52.7, 54.7, 57.3, 59.7, 62.0, 64.4, 66.8, 69.2, 71.6, 74.0],
                1: [54.7, 56.2, 57.7, 59.8, 62.4, 64.8, 67.3, 69.9, 72.3, 74.8, 77.2, 79.6],
                2: [58.4, 60.0, 61.7, 63.9, 66.6, 69.1, 71.7, 74.3, 76.9, 79.4, 82.0, 84.5],
                3: [61.4, 63.1, 64.8, 67.2, 70.0, 72.6, 75.3, 78.0, 80.7, 83.3, 86.0, 88.7],
                4: [63.9, 65.7, 67.5, 70.0, 72.9, 75.7, 78.5, 81.3, 84.1, 86.9, 89.7, 92.4],
                5: [65.9, 67.8, 69.7, 72.4, 75.4, 78.3, 81.2, 84.1, 87.0, 89.8, 92.7, 95.6],
                6: [67.6, 69.6, 71.6, 74.4, 77.5, 80.5, 83.5, 86.5, 89.5, 92.4, 95.4, 98.3],
                7: [69.2, 71.2, 73.3, 76.2, 79.4, 82.5, 85.6, 88.7, 91.7, 94.7, 97.8, 100.8],
                8: [70.6, 72.7, 74.8, 77.9, 81.1, 84.3, 87.5, 90.6, 93.8, 96.9, 100.0, 103.1],
                9: [72.0, 74.1, 76.3, 79.4, 82.8, 86.0, 89.3, 92.5, 95.8, 99.0, 102.2, 105.4],
                10: [73.3, 75.5, 77.7, 80.9, 84.3, 87.6, 91.0, 94.3, 97.6, 100.9, 104.2, 107.5],
                11: [74.5, 76.7, 79.0, 82.3, 85.8, 89.2, 92.6, 96.0, 99.4, 102.7, 106.1, 109.5],
                12: [75.7, 78.0, 80.3, 83.7, 87.2, 90.7, 94.2, 97.6, 101.1, 104.5, 107.9, 111.4],
            },
            'female': {
                0: [49.1, 50.5, 52.0, 54.0, 56.7, 59.1, 61.5, 63.9, 66.3, 68.7, 71.1, 73.5],
                1: [53.7, 55.2, 56.8, 59.0, 61.7, 64.2, 66.6, 69.1, 71.6, 74.0, 76.5, 78.9],
                2: [57.1, 58.7, 60.4, 62.7, 65.5, 68.0, 70.6, 73.2, 75.7, 78.3, 80.8, 83.3],
                3: [59.8, 61.5, 63.3, 65.7, 68.6, 71.2, 73.8, 76.4, 79.0, 81.5, 84.1, 86.7],
                4: [62.1, 63.9, 65.7, 68.2, 71.2, 73.9, 76.6, 79.3, 81.9, 84.6, 87.2, 89.8],
                5: [64.0, 65.9, 67.8, 70.4, 73.5, 76.3, 79.1, 81.8, 84.6, 87.3, 90.1, 92.8],
                6: [65.7, 67.6, 69.6, 72.3, 75.5, 78.4, 81.2, 84.1, 86.9, 89.7, 92.5, 95.3],
                7: [67.3, 69.2, 71.3, 74.1, 77.3, 80.3, 83.2, 86.1, 89.0, 91.9, 94.8, 97.6],
                8: [68.7, 70.7, 72.8, 75.7, 79.0, 82.0, 85.0, 88.0, 91.0, 93.9, 96.9, 99.8],
                9: [70.1, 72.1, 74.3, 77.3, 80.6, 83.7, 86.8, 89.8, 92.9, 95.9, 99.0, 102.0],
                10: [71.4, 73.4, 75.7, 78.7, 82.1, 85.3, 88.5, 91.6, 94.7, 97.8, 100.9, 104.0],
                11: [72.6, 74.7, 77.0, 80.1, 83.6, 86.8, 90.1, 93.3, 96.5, 99.7, 102.9, 106.0],
                12: [73.8, 75.9, 78.3, 81.5, 85.0, 88.3, 91.6, 94.9, 98.2, 101.4, 104.7, 108.0],
            }
        }

    def _load_weight_percentiles(self):
        return {
            'male': {
                0: [3.3, 3.6, 3.9, 4.3, 4.9, 5.5, 6.0, 6.6, 7.2, 7.8, 8.4, 9.0],
                1: [4.5, 4.9, 5.3, 5.8, 6.6, 7.4, 8.1, 8.9, 9.6, 10.4, 11.1, 11.9],
                2: [5.7, 6.2, 6.7, 7.4, 8.4, 9.3, 10.2, 11.1, 12.0, 12.9, 13.8, 14.7],
                3: [6.7, 7.2, 7.8, 8.6, 9.7, 10.8, 11.8, 12.9, 13.9, 15.0, 16.0, 17.1],
                4: [7.5, 8.1, 8.7, 9.6, 10.8, 12.0, 13.2, 14.4, 15.6, 16.8, 18.0, 19.2],
                5: [8.3, 8.9, 9.6, 10.5, 11.8, 13.1, 14.4, 15.7, 17.0, 18.3, 19.6, 20.9],
                6: [8.9, 9.6, 10.3, 11.3, 12.7, 14.1, 15.5, 16.9, 18.3, 19.7, 21.1, 22.5],
                7: [9.5, 10.2, 11.0, 12.0, 13.5, 15.0, 16.5, 18.0, 19.5, 21.0, 22.5, 24.0],
                8: [10.0, 10.8, 11.6, 12.7, 14.3, 15.9, 17.4, 19.0, 20.6, 22.2, 23.8, 25.4],
                9: [10.5, 11.3, 12.1, 13.3, 15.0, 16.6, 18.3, 20.0, 21.6, 23.3, 25.0, 26.6],
                10: [10.9, 11.7, 12.6, 13.8, 15.6, 17.3, 19.1, 20.8, 22.6, 24.3, 26.1, 27.8],
                11: [11.3, 12.2, 13.1, 14.3, 16.2, 18.0, 19.8, 21.6, 23.5, 25.3, 27.1, 28.9],
                12: [11.7, 12.6, 13.5, 14.8, 16.7, 18.6, 20.5, 22.4, 24.3, 26.2, 28.1, 30.0],
            },
            'female': {
                0: [3.2, 3.5, 3.8, 4.2, 4.8, 5.4, 5.9, 6.5, 7.1, 7.7, 8.3, 8.9],
                1: [4.2, 4.6, 5.0, 5.5, 6.2, 6.9, 7.6, 8.3, 9.0, 9.7, 10.4, 11.1],
                2: [5.3, 5.7, 6.2, 6.9, 7.8, 8.7, 9.6, 10.5, 11.4, 12.3, 13.2, 14.1],
                3: [6.2, 6.7, 7.3, 8.0, 9.1, 10.1, 11.1, 12.2, 13.2, 14.3, 15.3, 16.4],
                4: [7.0, 7.5, 8.2, 9.0, 10.2, 11.4, 12.5, 13.7, 14.9, 16.1, 17.3, 18.5],
                5: [7.7, 8.3, 9.0, 9.9, 11.2, 12.5, 13.8, 15.1, 16.4, 17.7, 19.0, 20.3],
                6: [8.3, 9.0, 9.7, 10.7, 12.1, 13.5, 14.9, 16.3, 17.7, 19.1, 20.5, 21.9],
                7: [8.9, 9.6, 10.4, 11.4, 12.9, 14.4, 15.9, 17.4, 18.9, 20.4, 21.9, 23.4],
                8: [9.4, 10.1, 11.0, 12.1, 13.7, 15.3, 16.9, 18.5, 20.1, 21.7, 23.3, 24.9],
                9: [9.9, 10.7, 11.6, 12.7, 14.4, 16.1, 17.8, 19.5, 21.2, 22.9, 24.6, 26.3],
                10: [10.4, 11.2, 12.1, 13.3, 15.1, 16.9, 18.7, 20.5, 22.3, 24.1, 25.9, 27.7],
                11: [10.8, 11.7, 12.6, 13.9, 15.8, 17.7, 19.5, 21.4, 23.3, 25.2, 27.0, 28.9],
                12: [11.2, 12.1, 13.1, 14.4, 16.4, 18.4, 20.3, 22.3, 24.2, 26.2, 28.1, 30.1],
            }
        }

    def _load_bmi_percentiles(self):
        return {
            'male': {
                0: [11.8, 12.4, 13.0, 13.8, 15.0, 16.1, 17.1, 18.1, 19.1, 20.1, 21.1, 22.1],
                1: [13.6, 14.3, 15.0, 15.9, 17.3, 18.6, 19.8, 20.9, 22.0, 23.1, 24.2, 25.3],
                2: [14.2, 15.0, 15.7, 16.7, 18.2, 19.6, 20.9, 22.1, 23.3, 24.5, 25.7, 26.9],
                3: [14.4, 15.2, 16.0, 17.1, 18.7, 20.2, 21.6, 22.9, 24.2, 25.5, 26.8, 28.1],
                4: [14.5, 15.3, 16.2, 17.3, 19.0, 20.6, 22.1, 23.5, 24.9, 26.3, 27.7, 29.1],
                5: [14.6, 15.4, 16.3, 17.5, 19.2, 20.9, 22.5, 24.0, 25.5, 27.0, 28.5, 30.0],
                6: [14.6, 15.5, 16.4, 17.6, 19.4, 21.1, 22.8, 24.4, 25.9, 27.5, 29.1, 30.7],
                7: [14.7, 15.5, 16.5, 17.7, 19.5, 21.3, 23.0, 24.7, 26.3, 28.0, 29.6, 31.3],
                8: [14.7, 15.6, 16.5, 17.8, 19.6, 21.5, 23.2, 24.9, 26.7, 28.4, 30.1, 31.9],
                9: [14.8, 15.6, 16.6, 17.9, 19.7, 21.6, 23.4, 25.2, 27.0, 28.8, 30.6, 32.4],
                10: [14.8, 15.7, 16.6, 18.0, 19.8, 21.8, 23.6, 25.4, 27.3, 29.1, 31.0, 32.8],
                11: [14.9, 15.7, 16.7, 18.1, 19.9, 21.9, 23.8, 25.6, 27.5, 29.4, 31.3, 33.2],
                12: [14.9, 15.8, 16.8, 18.2, 20.1, 22.1, 24.0, 25.9, 27.8, 29.7, 31.6, 33.5],
            },
            'female': {
                0: [11.8, 12.4, 13.0, 13.8, 15.0, 16.1, 17.1, 18.1, 19.1, 20.1, 21.1, 22.1],
                1: [13.4, 14.1, 14.8, 15.7, 17.1, 18.4, 19.6, 20.7, 21.8, 22.9, 24.0, 25.1],
                2: [14.0, 14.8, 15.5, 16.5, 18.0, 19.4, 20.7, 21.9, 23.1, 24.3, 25.5, 26.7],
                3: [14.3, 15.1, 15.8, 16.9, 18.5, 20.0, 21.4, 22.7, 24.0, 25.3, 26.6, 27.9],
                4: [14.5, 15.3, 16.1, 17.2, 18.9, 20.5, 22.0, 23.4, 24.8, 26.2, 27.6, 29.0],
                5: [14.7, 15.5, 16.3, 17.5, 19.2, 20.9, 22.4, 23.9, 25.4, 26.9, 28.4, 29.9],
                6: [14.8, 15.6, 16.5, 17.7, 19.5, 21.2, 22.8, 24.4, 25.9, 27.5, 29.0, 30.6],
                7: [15.0, 15.8, 16.7, 17.9, 19.8, 21.5, 23.2, 24.8, 26.4, 28.0, 29.6, 31.2],
                8: [15.1, 15.9, 16.8, 18.1, 20.0, 21.8, 23.5, 25.2, 26.9, 28.6, 30.2, 31.9],
                9: [15.2, 16.1, 17.0, 18.3, 20.2, 22.1, 23.8, 25.6, 27.3, 29.1, 30.8, 32.6],
                10: [15.4, 16.2, 17.2, 18.5, 20.5, 22.4, 24.2, 26.0, 27.8, 29.6, 31.4, 33.2],
                11: [15.5, 16.4, 17.3, 18.7, 20.7, 22.7, 24.5, 26.4, 28.3, 30.1, 32.0, 33.9],
                12: [15.6, 16.5, 17.5, 18.9, 21.0, 23.0, 24.9, 26.8, 28.8, 30.7, 32.6, 34.6],
            }
        }

    def _load_models(self):
        stunting_model_path = os.path.join(self.model_dir, 'stunting_model.pkl')
        obesity_model_path = os.path.join(self.model_dir, 'obesity_model.pkl')
        scaler_path = os.path.join(self.model_dir, 'scaler.pkl')

        if os.path.exists(stunting_model_path) and os.path.exists(obesity_model_path) and os.path.exists(scaler_path):
            self.stunting_model = joblib.load(stunting_model_path)
            self.obesity_model = joblib.load(obesity_model_path)
            self.scaler = joblib.load(scaler_path)
        else:
            self._train_demo_models()

    def _train_demo_models(self):
        X, y_stunting, y_obesity = self._generate_demo_data()
        
        X_train, X_test, y_stunting_train, y_stunting_test = train_test_split(
            X, y_stunting, test_size=0.2, random_state=42
        )
        _, _, y_obesity_train, y_obesity_test = train_test_split(
            X, y_obesity, test_size=0.2, random_state=42
        )

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.stunting_model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        )
        self.stunting_model.fit(X_train_scaled, y_stunting_train)

        self.obesity_model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        )
        self.obesity_model.fit(X_train_scaled, y_obesity_train)

        self._save_models()

    def _generate_demo_data(self, n_samples=1000):
        np.random.seed(42)
        
        ages = np.random.randint(0, 144, n_samples)
        genders = np.random.randint(0, 2, n_samples)
        heights = np.random.normal(100, 20, n_samples)
        weights = np.random.normal(20, 8, n_samples)
        father_heights = np.random.normal(170, 10, n_samples)
        mother_heights = np.random.normal(160, 8, n_samples)
        birth_weights = np.random.normal(3.3, 0.5, n_samples)

        X = np.column_stack([
            ages, genders, heights, weights, father_heights, mother_heights, birth_weights
        ])

        y_stunting = []
        y_obesity = []

        for i in range(n_samples):
            age = ages[i]
            gender = 'male' if genders[i] == 0 else 'female'
            height = heights[i]
            weight = weights[i]

            stunting_assessment = self.assess_stunting_risk(height, age, gender)
            obesity_assessment = self.assess_obesity_risk(weight, height, age, gender)

            y_stunting.append(stunting_assessment['risk'])
            y_obesity.append(obesity_assessment['risk'])

        return X, np.array(y_stunting), np.array(y_obesity)

    def train(self, X, y_stunting, y_obesity):
        X_train, X_test, y_stunting_train, y_stunting_test = train_test_split(
            X, y_stunting, test_size=0.2, random_state=42
        )
        _, _, y_obesity_train, y_obesity_test = train_test_split(
            X, y_obesity, test_size=0.2, random_state=42
        )

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)

        self.stunting_model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        )
        self.stunting_model.fit(X_train_scaled, y_stunting_train)

        self.obesity_model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        )
        self.obesity_model.fit(X_train_scaled, y_obesity_train)

        self._save_models()

        stunting_score = self.stunting_model.score(
            self.scaler.transform(X_test), y_stunting_test
        )
        obesity_score = self.obesity_model.score(
            self.scaler.transform(X_test), y_obesity_test
        )

        return {
            'stunting_r2_score': stunting_score,
            'obesity_r2_score': obesity_score
        }

    def predict(self, features):
        if self.stunting_model is None or self.obesity_model is None or self.scaler is None:
            self._load_models()

        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)

        stunting_risk = self.stunting_model.predict(features_scaled)[0]
        obesity_risk = self.obesity_model.predict(features_scaled)[0]

        stunting_risk = max(5, min(95, stunting_risk))
        obesity_risk = max(5, min(95, obesity_risk))

        return {
            'stunting_risk': round(float(stunting_risk), 2),
            'obesity_risk': round(float(obesity_risk), 2)
        }

    def _save_models(self):
        stunting_model_path = os.path.join(self.model_dir, 'stunting_model.pkl')
        obesity_model_path = os.path.join(self.model_dir, 'obesity_model.pkl')
        scaler_path = os.path.join(self.model_dir, 'scaler.pkl')

        joblib.dump(self.stunting_model, stunting_model_path)
        joblib.dump(self.obesity_model, obesity_model_path)
        joblib.dump(self.scaler, scaler_path)

    def calculate_age_months(self, birth_date: date, measure_date: date) -> int:
        years = measure_date.year - birth_date.year
        months = measure_date.month - birth_date.month
        if measure_date.day < birth_date.day:
            months -= 1
        return years * 12 + months

    def get_percentile(self, value: float, percentiles: List[float]) -> int:
        for i, p in enumerate(percentiles):
            if value <= p:
                return (i + 1) * 10
        return 100

    def assess_stunting_risk(self, height: float, age_months: int, gender: str) -> Dict:
        if age_months > 144:
            age_months = 144
        if age_months < 0:
            age_months = 0

        age_key = min(age_months // 12, 12)
        percentiles = self.height_percentiles.get(gender, {}).get(age_key, [])
        
        if not percentiles:
            return {'risk': 50, 'percentile': 50, 'status': 'normal'}

        percentile = self.get_percentile(height, percentiles)
        
        if percentile < 3:
            risk = 85 + (3 - percentile) * 2
            status = 'severe'
        elif percentile < 10:
            risk = 70 + (10 - percentile) * 1.5
            status = 'moderate'
        elif percentile < 25:
            risk = 40 + (25 - percentile)
            status = 'mild'
        else:
            risk = max(5, 25 - (percentile - 25) * 0.3)
            status = 'normal'

        return {
            'risk': min(95, max(5, round(risk, 2))),
            'percentile': percentile,
            'status': status,
            'height': height,
            'age_months': age_months
        }

    def assess_obesity_risk(self, weight: float, height: float, age_months: int, gender: str) -> Dict:
        bmi = weight / ((height / 100) ** 2) if height > 0 else 0
        
        if age_months > 144:
            age_months = 144
        if age_months < 0:
            age_months = 0

        age_key = min(age_months // 12, 12)
        percentiles = self.bmi_percentiles.get(gender, {}).get(age_key, [])
        
        if not percentiles:
            return {'risk': 50, 'percentile': 50, 'status': 'normal', 'bmi': bmi}

        percentile = self.get_percentile(bmi, percentiles)
        
        if percentile >= 95:
            risk = 80 + (percentile - 95) * 0.5
            status = 'obesity'
        elif percentile >= 85:
            risk = 60 + (percentile - 85)
            status = 'overweight'
        elif percentile < 3:
            risk = 70 + (3 - percentile) * 2
            status = 'underweight'
        else:
            risk = max(5, 20 - (percentile - 50) * 0.2)
            status = 'normal'

        return {
            'risk': min(95, max(5, round(risk, 2))),
            'percentile': percentile,
            'status': status,
            'bmi': round(bmi, 2),
            'age_months': age_months
        }

    def analyze_growth(self, birth_date: date, measure_date: date, height: float, weight: float, gender: str, father_height: float = None, mother_height: float = None, birth_weight: float = None) -> Dict:
        age_months = self.calculate_age_months(birth_date, measure_date)
        
        gender_code = 0 if gender == 'male' else 1
        father_height = father_height or 170
        mother_height = mother_height or 160
        birth_weight = birth_weight or 3.3

        features = [age_months, gender_code, height, weight, father_height, mother_height, birth_weight]
        ml_prediction = self.predict(features)
        
        stunting_assessment = self.assess_stunting_risk(height, age_months, gender)
        obesity_assessment = self.assess_obesity_risk(weight, height, age_months, gender)
        
        stunting_risk = (ml_prediction['stunting_risk'] + stunting_assessment['risk']) / 2
        obesity_risk = (ml_prediction['obesity_risk'] + obesity_assessment['risk']) / 2
        
        overall_risk = (stunting_risk + obesity_risk) / 2
        
        risk_factors = []
        if stunting_risk > 50:
            risk_factors.append({
                'type': 'stunting',
                'description': f'身高发育{stunting_assessment["status"]}，位于第{stunting_assessment["percentile"]}百分位',
                'risk': stunting_risk
            })
        if obesity_risk > 50:
            risk_factors.append({
                'type': 'obesity',
                'description': f'体重发育{obesity_assessment["status"]}，BMI为{obesity_assessment["bmi"]}，位于第{obesity_assessment["percentile"]}百分位',
                'risk': obesity_risk
            })

        return {
            'stunting_risk': round(stunting_risk, 2),
            'obesity_risk': round(obesity_risk, 2),
            'overall_risk': round(overall_risk, 2),
            'age_months': age_months,
            'ml_prediction': ml_prediction,
            'details': {
                'stunting': stunting_assessment,
                'obesity': obesity_assessment,
                'risk_factors': risk_factors
            }
        }

    def generate_intervention_plan(self, risk_assessment: Dict) -> Dict:
        stunting_risk = risk_assessment.get('stunting_risk', 0)
        obesity_risk = risk_assessment.get('obesity_risk', 0)
        details = risk_assessment.get('details', {})
        stunting_status = details.get('stunting', {}).get('status', 'normal')
        obesity_status = details.get('obesity', {}).get('status', 'normal')
        
        interventions = []
        
        if stunting_risk > 50:
            if stunting_status == 'severe':
                interventions.append({
                    'category': 'medical',
                    'priority': 'high',
                    'title': '立即就医检查',
                    'content': '建议立即到儿科内分泌专科进行详细检查，包括生长激素水平、甲状腺功能、骨龄评估等。'
                })
                interventions.append({
                    'category': 'nutrition',
                    'priority': 'high',
                    'title': '营养强化',
                    'content': '增加优质蛋白质摄入，每日保证牛奶、鸡蛋、瘦肉等高蛋白食物。适当补充维生素D和钙剂。'
                })
            elif stunting_status == 'moderate':
                interventions.append({
                    'category': 'medical',
                    'priority': 'medium',
                    'title': '定期监测',
                    'content': '建议每月测量身高体重，每3-6个月到儿科进行生长发育评估。'
                })
                interventions.append({
                    'category': 'nutrition',
                    'priority': 'medium',
                    'title': '均衡饮食',
                    'content': '保证每日三餐营养均衡，增加富含蛋白质和钙质的食物摄入。'
                })
            else:
                interventions.append({
                    'category': 'lifestyle',
                    'priority': 'low',
                    'title': '保持良好生活习惯',
                    'content': '保证充足睡眠（每日10-12小时），适当进行户外运动，促进生长发育。'
                })
        
        if obesity_risk > 50:
            if obesity_status == 'obesity':
                interventions.append({
                    'category': 'medical',
                    'priority': 'high',
                    'title': '医学评估',
                    'content': '建议到儿科或营养科进行专业评估，排除内分泌疾病，制定个性化减重方案。'
                })
                interventions.append({
                    'category': 'diet',
                    'priority': 'high',
                    'title': '饮食控制',
                    'content': '控制总热量摄入，减少高糖、高脂肪食物，增加蔬菜水果摄入。建立规律的饮食习惯，避免暴饮暴食。'
                })
                interventions.append({
                    'category': 'exercise',
                    'priority': 'high',
                    'title': '增加运动',
                    'content': '每日保证至少60分钟中等强度运动，如游泳、跑步、骑自行车等。减少久坐时间。'
                })
            elif obesity_status == 'overweight':
                interventions.append({
                    'category': 'diet',
                    'priority': 'medium',
                    'title': '饮食调整',
                    'content': '适当控制零食和含糖饮料摄入，增加蔬菜水果比例，保持饮食均衡。'
                })
                interventions.append({
                    'category': 'exercise',
                    'priority': 'medium',
                    'title': '规律运动',
                    'content': '每日保证30-60分钟运动，培养运动习惯。'
                })
        
        if stunting_risk <= 50 and obesity_risk <= 50:
            interventions.append({
                'category': 'prevention',
                'priority': 'low',
                'title': '保持健康生活方式',
                'content': '继续保持均衡饮食、规律作息和适量运动，定期监测生长发育情况。'
            })
        
        return {
            'interventions': interventions,
            'total_count': len(interventions),
            'high_priority': len([i for i in interventions if i['priority'] == 'high']),
            'medium_priority': len([i for i in interventions if i['priority'] == 'medium']),
            'low_priority': len([i for i in interventions if i['priority'] == 'low'])
        }
