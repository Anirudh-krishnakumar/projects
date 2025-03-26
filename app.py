from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load trained model and encoders
model_file = "dt_model.pkl"
encoders_file = "encoders.pkl"

def load_model():
    with open(model_file, "rb") as f:
        model = pickle.load(f)
    with open(encoders_file, "rb") as f:
        encoders = pickle.load(f)
    return model, encoders

@app.route("/")
def home():
    return render_template("index.html")  # Load frontend

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    model, encoders = load_model()

    df_input = pd.DataFrame([data])

    # Encode categorical features
    categorical_features = ["Item_Fat_Content", "Item_Type", "Outlet_Size", "Outlet_Location_Type"]
    for col in categorical_features:
        if col in df_input and col in encoders:
            df_input[col] = encoders[col].transform(df_input[col])

    # Ensure correct feature order
    expected_columns = ["Item_Weight", "Item_Fat_Content", "Item_Visibility", "Item_Type",
                        "Item_MRP", "Outlet_Establishment_Year", "Outlet_Size", "Outlet_Location_Type"]
    df_input = df_input[expected_columns]

    # Make a prediction
    prediction_encoded = model.predict(df_input)[0]  # This is an encoded integer

    # Decode the predicted value back to its original category
    outlet_type_encoder = encoders["Outlet_Type"]
    predicted_outlet_type = outlet_type_encoder.inverse_transform([prediction_encoded])[0]

    return jsonify({"predicted_outlet_type": predicted_outlet_type})



if __name__ == "__main__":
    app.run(debug=True)
