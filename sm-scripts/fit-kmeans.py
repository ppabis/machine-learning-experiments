import os
import pandas as pd
from sklearn.cluster import KMeans
import joblib

if __name__ == "__main__":
    input_file = os.path.join(os.environ['SM_CHANNEL_TRAIN'], os.environ['SM_INPUT_DATA_FILE'])
    model_file = os.path.join(os.environ['SM_MODEL_DIR'], os.environ['SM_MODEL_FILE'])

    # The files will be copied from S3 by SageMaker. Just read one of them.
    csv = pd.read_csv(input_file)

    # Drop profession string
    csv.drop(['Profession'], axis=1, inplace=True)

    model = KMeans(n_clusters=6).fit(csv)

    joblib.dump(model, model_file)