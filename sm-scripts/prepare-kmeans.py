import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    input_file = os.path.join("/opt/ml/processing/input", os.environ['SM_PROCESS_FILE'])
    output_file = os.path.join("/opt/ml/processing/output", os.environ['SM_PROCESS_FILE'])

    # The files will be copied from S3 by SageMaker.
    csv = pd.read_csv(input_file)

    professions_str = csv['Profession']
    professions = pd.get_dummies(csv['Profession'], dtype=int)
    csv = pd.concat([csv, professions], axis=1)
    # Remove string profession
    csv.drop(['Profession'], axis=1, inplace=True)
    csv = csv.astype(dtype='double')

    scaler = StandardScaler()
    scaled = scaler.fit_transform(csv[csv.columns])
    csv[csv.columns] = scaled

    # Add profession string back after scaling
    csv['Profession'] = professions_str

    csv.to_csv(output_file, header=True, index=False)