import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Expanded dataset (synthetic but better)
X = [
    [20,1,1,0,0,1],
    [100,5,0,3,1,4],
    [80,3,0,2,0,3],
    [30,1,1,0,0,1],
    [120,6,0,4,1,5],
    [25,1,1,0,0,1],
    [90,4,0,2,1,3],
    [150,7,0,5,1,6],
    [40,2,1,1,0,2],
    [110,5,0,3,1,4]
]

y = [0,1,1,0,1,0,1,1,0,1]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "model.pkl")

