import os, joblib, pathlib
import pandas as pd
from sklearn.preprocessing import StandardScaler

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def with_scaling(csv):
    scaler_file = os.path.join("/opt/ml/processing/output", pathlib.Path(os.environ['SM_PROCESS_FILE']).stem + ".scaler.joblib")
    # Remove string profession
    csv = csv.astype(dtype='double')

    gold_spent = csv['Gold_Spent']
    csv.drop(['Gold_Spent'], axis=1, inplace=True)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(csv[csv.columns])
    csv[csv.columns] = scaled

    # Add profession string back after scaling
    csv['Gold_Spent'] = gold_spent

    joblib.dump(scaler, scaler_file)

    return csv

if __name__ == "__main__":
    stem = pathlib.Path(os.environ['SM_PROCESS_FILE']).stem
    input_file = os.path.join("/opt/ml/processing/input", os.environ['SM_PROCESS_FILE'])
    mkdirs("/opt/ml/processing/output/train")
    training_file = os.path.join("/opt/ml/processing/output/train", f"{stem}.training.csv")
    mkdirs("/opt/ml/processing/output/val")
    validation_file = os.path.join("/opt/ml/processing/output/val", f"{stem}.validation.csv")
    mkdirs("/opt/ml/processing/output/test")
    testing_file = os.path.join("/opt/ml/processing/output/test", f"{stem}.testing.csv")

    # The files will be copied from S3 by SageMaker.
    csv = pd.read_csv(input_file)

    # To preserve ordering and completeness
    csv['Profession'] = pd.Categorical(csv['Profession'], categories=['Wizard', 'Knight', 'Rogue', 'Cleric'], ordered=True)
    professions = pd.get_dummies(csv['Profession'], dtype=int)
    csv = pd.concat([csv, professions], axis=1)
    csv.drop(['Profession'], axis=1, inplace=True)
    
    if 'SM_SCALER_ENABLE' in os.environ and os.environ['SM_SCALER_ENABLE'] == '1':
        csv = with_scaling(csv)

    # Move Gold_Spent to the front - this is the prediction for XGBoost
    gold_spent = csv['Gold_Spent']
    csv.drop(['Gold_Spent'], axis=1, inplace=True)
    csv.insert(0, 'Gold_Spent', gold_spent)

    # Split the data
    training = csv.sample(frac=0.75, random_state=200)
    csv.drop(training.index, inplace=True)
    validation = csv.sample(frac=0.6, random_state=200)
    csv.drop(validation.index, inplace=True)
    testing = csv

    training.to_csv(training_file, header=False, index=False)
    validation.to_csv(validation_file, header=False, index=False)
    testing.to_csv(testing_file, header=False, index=False)
    
    header_file = os.path.join("/opt/ml/processing/output", f"{stem}.header.csv")
    header = pd.DataFrame(csv.columns)
    header.to_csv(header_file, header=False, index=False)

