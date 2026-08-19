# ml_engine/lead_scoring.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
def train_and_predict_lead(email_opens, website_visits, demo_request):
# Sample training dataset
data = {
"Email_Open": [12, 5, 15, 2, 8, 19],
"Website_Visit": [20, 6, 18, 3, 10, 25],
"Demo_Request": [1, 0, 1, 0, 1, 1],
"Converted": [1, 0, 1, 0, 1, 1]
}
df = pd.DataFrame(data)
X = df[["Email_Open", "Website_Visit", "Demo_Request"]]
y = df["Converted"]
model = RandomForestClassifier(random_state=42)
model.fit(X, y)
new_lead = [[email_opens, website_visits, demo_request]]
probability = model.predict_proba(new_lead)[0][1]
score = round(probability * 100, 2)
return score