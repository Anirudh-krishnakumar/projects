import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv(r"C:\Users\anikt\Downloads\Test.csv")  # Update with your file path

# Drop identifier columns that do not contribute to prediction
df_clean = df.drop(columns=["Item_Identifier", "Outlet_Identifier"])

# Handle missing values (fill numeric with median, categorical with mode)
for col in df_clean.select_dtypes(include=['number']).columns:
    df_clean[col].fillna(df_clean[col].median(), inplace=True)
for col in df_clean.select_dtypes(include=['object']).columns:
    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)

# Encode categorical features
label_encoders = {}
for col in df_clean.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df_clean[col] = le.fit_transform(df_clean[col])
    label_encoders[col] = le

# Define features and target
X = df_clean.drop(columns=["Outlet_Type"])
y = df_clean["Outlet_Type"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Decision Tree classifier
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Predict and evaluate
y_pred = dt_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save the trained model
with open("dt_model.pkl", "wb") as f:
    pickle.dump(dt_model, f)

# Save the label encoders
with open("encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

print(f"Model saved successfully with accuracy: {accuracy:.2f}")
