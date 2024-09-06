# #abc new file
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split

# from autosklearn.classification import AutoSklearnClassifier
# import autosklearn.classification

key_path = "bq-key.json"
project_id = "taxigo-production"
dataset_id = "Tania"
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=project_id)


# Write the SQL query to filter by uid
query = f"""
    SELECT *
    FROM `{project_id}.{dataset_id}.driver_campaign_model_train_0617`
    """
# Run the query
query_job = client.query(query)

# Fetch and return the results
df = query_job.to_dataframe()


# Get features and target
df_select = df[df["test_week"] < pd.to_datetime("2024-06-10")]
x = df_select.drop(
    ["driver_id", "test_week", "time_period", "test_week_is_positive_reaction"], axis=1
)
y = df_select["test_week_is_positive_reaction"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, test_size=0.2, random_state=34, stratify=y
)

print(df.head(5))
