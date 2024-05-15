{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": "None",
   "id": "5099355e-94ab-420e-aba3-33c0a123392f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import streamlit as st\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.ensemble import IsolationForest\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.neighbors import LocalOutlierFactor\n",
    "from sklearn.svm import OneClassSVM\n",
    "from sklearn.impute import SimpleImputer\n",
    "from sklearn.metrics import accuracy_score\n",
    "from sklearn.cluster import DBSCAN\n",
    "\n",
    "def load_data():\n",
    "    data = pd.read_csv('reduced_variables.csv')\n",
    "    return data\n",
    "\n",
    "def preprocess_data(data):\n",
    "    imputer = SimpleImputer(strategy='mean')\n",
    "    data_imputed = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)\n",
    "    preprocessor = StandardScaler()\n",
    "    X = data_imputed.drop(columns=['Outlier']) if 'Outlier' in data_imputed.columns else data_imputed\n",
    "    X_preprocessed = preprocessor.fit_transform(X)\n",
    "    return X_preprocessed\n",
    "\n",
    "def train_models(X_train, X_test):\n",
    "    # Define and fit Isolation Forest\n",
    "    iforest = IsolationForest(n_estimators=50, contamination='auto', random_state=42)\n",
    "    iforest.fit(X_train)\n",
    "    outlier_preds = iforest.predict(X_test)\n",
    "\n",
    "    # Apply DBSCAN\n",
    "    dbscan = DBSCAN(eps=0.5, min_samples=5)\n",
    "    predictions_dbscan = dbscan.fit_predict(X_test)\n",
    "\n",
    "    # Apply KMeans\n",
    "    kmeans = KMeans(n_clusters=2, random_state=42)\n",
    "    predictions_kmeans = kmeans.fit_predict(X_test)\n",
    "\n",
    "    # Apply Local Outlier Factor (LOF) with novelty=False\n",
    "    lof = LocalOutlierFactor(novelty=False, contamination='auto')\n",
    "    predictions_lof = lof.fit_predict(X_test)\n",
    "\n",
    "    # Apply One-Class SVM\n",
    "    svm = OneClassSVM(kernel='rbf', nu=0.05)\n",
    "    predictions_svm = svm.fit_predict(X_test)\n",
    "\n",
    "    return outlier_preds, predictions_dbscan, , predictions_kmeans, predictions_lof, predictions_svm\n",
    "\n",
    "def calculate_accuracies(outlier_preds, predictions_dbscan,  predictions_kmeans, predictions_lof, predictions_svm):\n",
    "    accuracy_dbscan = accuracy_score(outlier_preds, predictions_dbscan)\n",
    "    accuracy_kmeans = accuracy_score(outlier_preds, predictions_kmeans)\n",
    "    accuracy_lof = accuracy_score(outlier_preds, predictions_lof)\n",
    "    accuracy_svm = accuracy_score(outlier_preds, predictions_svm)\n",
    "    accuracy_iforest = accuracy_score(outlier_preds, outlier_preds)\n",
    "    return accuracy_dbscan, accuracy_hdbscan, accuracy_kmeans, accuracy_lof, accuracy_svm, accuracy_iforest\n",
    "\n",
    "# Streamlit App\n",
    "st.title('Outlier Detection Model Accuracy')\n",
    "\n",
    "# Load and preprocess data\n",
    "data = load_data()\n",
    "X_preprocessed = preprocess_data(data)\n",
    "\n",
    "# Separate the data into training and testing sets\n",
    "X_train, X_test, _, _ = train_test_split(X_preprocessed, X_preprocessed, test_size=0.3, random_state=42)\n",
    "\n",
    "# Train models and get predictions\n",
    "outlier_preds, predictions_dbscan,  predictions_kmeans, predictions_lof, predictions_svm = train_models(X_train, X_test)\n",
    "\n",
    "# Calculate accuracies\n",
    "accuracy_dbscan,  accuracy_kmeans, accuracy_lof, accuracy_svm, accuracy_iforest = calculate_accuracies(outlier_preds, predictions_dbscan,  predictions_kmeans, predictions_lof, predictions_svm)\n",
    "\n",
    "# Display accuracies\n",
    "st.write(f\"Accuracy for DBSCAN: {accuracy_dbscan}\")\n",
    "st.write(f\"Accuracy for KMeans: {accuracy_kmeans}\")\n",
    "st.write(f\"Accuracy for Local Outlier Factor: {accuracy_lof}\")\n",
    "st.write(f\"Accuracy for One-Class SVM: {accuracy_svm}\")\n",
    "st.write(f\"Accuracy for Isolation Forest: {accuracy_iforest}\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
