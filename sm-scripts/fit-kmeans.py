import os, shutil, pathlib, joblib
import pandas as pd
from sklearn.cluster import KMeans

if __name__ == "__main__":
    input_file = os.path.join(os.environ['SM_CHANNEL_TRAIN'], os.environ['SM_INPUT_DATA_FILE'])
    model_file = os.path.join(os.environ['SM_MODEL_DIR'], os.environ['SM_MODEL_FILE'])

    # The files will be copied from S3 by SageMaker. Just read one of them.
    csv = pd.read_csv(input_file)

    # Drop profession string
    csv.drop(['Profession'], axis=1, inplace=True)

    model = KMeans(n_clusters=6).fit(csv)

    joblib.dump(model, model_file)

    # If the input file also has scaler weights, keep them close to the model too
    # So if the input training file is named "records-2022.csv", the scaler should be named "records-2022.scaler.joblib"
    # And the copied weights for the scaler will be "my-kmeans-model.scaler.joblib" for model named "my-kmeans-model.joblib
    scaler_source = os.path.join(os.environ['SM_CHANNEL_TRAIN'], pathlib.Path(os.environ['SM_INPUT_DATA_FILE']).stem + ".scaler.joblib")
    if os.path.exists( scaler_source ):
        scaler_dest = os.path.join(os.environ['SM_MODEL_DIR'], pathlib.Path(os.environ['SM_MODEL_FILE']).stem + ".scaler.joblib")
        shutil.copy(scaler_source, scaler_dest)