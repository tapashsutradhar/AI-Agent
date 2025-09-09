from typing import List, Dict
import pandas as pd
import numpy as np


class ForecastEngine:
def __init__(self):
# placeholder for loaded model
self.model = None


def _prepare(self, series: List[Dict]):
df = pd.DataFrame(series)
if 'ds' not in df.columns or 'y' not in df.columns:
raise ValueError("Series must contain 'ds' and 'y' columns")
df['ds'] = pd.to_datetime(df['ds'])
df = df.sort_values('ds')
df = df.set_index('ds')
# infer daily frequency — if data is irregular, reindex to daily and interpolate
df = df.asfreq('D')
df['y'] = df['y'].astype(float)
df['y'] = df['y'].interpolate()
return df


def predict(self, series: List[Dict], horizon: int = 14):
df = self._prepare(series)
vals = df['y'].values


# If very small dataset, fallback to naive persistence
if len(vals) < 10:
last = float(vals[-1])
preds = [last] * horizon
dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=horizon)
return [{"ds": d.strftime('%Y-%m-%d'), "y": p} for d,p in zip(dates, preds)]


# Create lag features
N_LAGS = 14
X_sup, y_sup = [], []
for i in range(N_LAGS, len(vals)):
X_sup.append(vals[i-N_LAGS:i])
y_sup.append(vals[i])
X_sup = np.array(X_sup)
y_sup = np.array(y_sup)


# Train a simple RandomForest
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_sup, y_sup, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)


# iterative forecasting
preds = []
window = vals[-N_LAGS:].tolist()
for _ in range(horizon):
p = model.predict([window])[0]
preds.append(float(p))
window = window[1:] + [p]


dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=horizon)
return [{"ds": d.strftime('%Y-%m-%d'), "y": p} for d,p in zip(dates, preds)]