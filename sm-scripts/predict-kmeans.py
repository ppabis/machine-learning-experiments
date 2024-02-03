import os, joblib, pathlib
import pandas as pd
from io import StringIO, BytesIO

def convert_professions(df):
    """
    Converts professions to one-hot encoding
    """
    df['Profession'] = pd.Categorical(df['Profession'], categories=['Wizard', 'Knight', 'Rogue', 'Cleric'])
    professions = pd.get_dummies(df['Profession'], dtype=int)
    df = pd.concat([df, professions], axis=1)
    return df

def input_fn(input_data, content_type):
    # Create a reader depending on incoming data type
    buffer = StringIO(input_data) if isinstance(input_data, str) else BytesIO(input_data)

    if content_type == 'text/csv':
        df = pd.read_csv(buffer)
    elif content_type == 'application/json' or content_type == 'text/json':
        df = pd.read_json(buffer, orient='records')
    else:
        raise ValueError(f'Content type {content_type} not supported.')
    
    df = convert_professions(df)

    return df

    
def model_fn(model_dir):
    model_file = os.path.join(model_dir, os.environ['SM_MODEL_FILE'])
    model = joblib.load(model_file)

    scaler = None
    scaler_file = os.path.join(model_dir, pathlib.Path(os.environ['SM_MODEL_FILE']).stem + ".scaler.joblib")
    if os.path.exists(scaler_file):
        scaler = joblib.load(scaler_file)
    
    return (model, scaler)

def predict_fn(input_data, model):
    # This expects a tuple
    model, scaler = model

    profession_str = input_data['Profession']
    input_data.drop(['Profession'], axis=1, inplace=True)

    # SKLearn algorithms are horrible - they know column names but can't into sorting
    # them from DataFrame thus we have to sort them in pandas before feeding in.
    if scaler:
        input_data[scaler.feature_names_in_] = scaler.transform(input_data[scaler.feature_names_in_])
    
    prediction = model.predict(input_data[model.feature_names_in_])
    
    return pd.DataFrame(prediction, columns=['Cluster'])

def output_fn(prediction, accept):
    if accept == 'application/json' or accept == 'text/json':
        return prediction.to_json(orient='records')
    elif accept == 'text/csv':
        return prediction.to_csv(index=False, header=True)
    else:
        raise ValueError(f'Accept type {accept} not supported.')