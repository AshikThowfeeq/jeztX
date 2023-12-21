import shutil
import pandas as pd
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging 
import json

from myapp.models import EmployeeCameraAssignment


def list_all_cameras():
    # Fetch all unique cameras from EmployeeCameraAssignment
    camera_assignments = EmployeeCameraAssignment.objects.all()
    unique_camera_names = set()
    for assignment in camera_assignments:
        unique_camera_names.add(assignment.cam.cam_name)
    print(unique_camera_names)
    return list(unique_camera_names)

list_all_cameras()


def list(camera_name):
    # Query for all assignments for the specified camera
    assignments = EmployeeCameraAssignment.objects.filter(cam__cam_name=camera_name)
    # Extract employee IDs from these assignments
    employee_ids = [assignment.employee.employee_id for assignment in assignments]

    print(employee_ids)
    return employee_ids

list("109d")



logging.basicConfig(filename='face_recognition.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

outresult = 'results'
if not os.path.exists(outresult):
    os.makedirs(outresult)



def face_recognition_process(json_file, input_dataframe,cpid):

        
    def read_json(path):
        try:
            df = pd.read_json(path)
            return df
        except FileNotFoundError as e:
            print(f"Error reading JSON file: {e}")
            logging.critical(f"Error reading JSON file: {e}")
            return None

    def merge_and_save(dataframe, filename):
        if os.path.exists(filename):
            existing_df = pd.read_json(filename)
            merged_df = pd.concat([existing_df, dataframe], ignore_index=True)
        else:
            merged_df = dataframe

        try:
            merged_df.to_json(filename, orient='records')
        except Exception as e:
            print(f"Error saving to JSON file: {e}")
            logging.critical(f"Error saving to JSON file: {e}")
            return None

        return filename

    unknown = []

    df = read_json(json_file)
    if df is None:
        return None

    X_list = df['Facial_Features'].tolist()
    similarity_threshold = 38.00

    for index, row in input_dataframe.iterrows():
        y = row['Facial_Features']
        y_2d = np.array(y).reshape(1, -1)
        X = np.asarray(X_list)
        embeddings_2d = X.reshape(-1, X.shape[-1])
        try:
            cosine_similarities = cosine_similarity(embeddings_2d, y_2d)
            similarity_percentages = cosine_similarities * 100
        except Exception as e:
            print(f"Error calculating cosine similarities: {e}")
            logging.critical(f"Error calculating cosine similarities: {e}")
            return None

        df['similarity_percentage'] = similarity_percentages.flatten()

        try:
            df_sorted = df.sort_values(by='similarity_percentage', ascending=False)
            df_value_counts = df_sorted.head(5)
            name_counts = df_value_counts['image_path'].value_counts()
            most_frequent_name = name_counts.idxmax()
            filtered_df = df_value_counts[df_value_counts['image_path'] == most_frequent_name]
            filtered_df_sorted = filtered_df.sort_values(by='similarity_percentage', ascending=False)
            top_match = filtered_df_sorted.iloc[0]
        except Exception as e:
            print(f"Error sorting DataFrame: {e}")
            logging.critical(f"Error sorting DataFrame: {e}")
            return None

        if top_match['similarity_percentage'] < similarity_threshold:
            unknown.append("Unknown face")
        else:
            unknown.append(top_match['image_path'])

    input_dataframe["face_recognition"] = unknown
    input_dataframe.drop(["Facial_Features"], inplace=True, axis=1)

    # Create a copy of unknown_faces and known_faces
    unknown_faces = input_dataframe[input_dataframe["face_recognition"] == "Unknown face"].copy()
    known_faces = input_dataframe[input_dataframe["face_recognition"] != "Unknown face"].copy()

    # Drop columns from the copied DataFrames
    unknown_faces.drop(["bbox", "Kps"], axis=1, inplace=True)
    known_faces.drop(["bbox", "Kps"], axis=1, inplace=True)

    # print(results)
    # if not os.path.exists(results):
    #     os.makedirs(results)
    unknown_file = merge_and_save(unknown_faces, f'{outresult}/{cpid}.json')
    known_file = merge_and_save(known_faces, f'{outresult}/{cpid}.json')
    return unknown_file, known_file

def results(ipjs,cmpfolder):

    dataframes=[]
    df = pd.read_json(ipjs)
    pose = df.iloc[0]['Pose']
    cmpnyid = df.iloc[0]['Company_id']
    print(cmpnyid)

    df_straight = None
    df_down = None
    df_side = None

    if df['Pose'].isin(['STRAIGHT']).any():
        df_straight = df.loc[df['Pose'] == "STRAIGHT"]

    if df['Pose'].isin(['DOWN']).any():
        df_down = df.loc[df["Pose"] == "DOWN"]
        
    if df['Pose'].isin(['SIDE']).any():
        df_side = df.loc[df["Pose"] == "SIDE"]

    # Only append the DataFrames that are not None
    if df_straight is not None:
        dataframes.append(df_straight)

    if df_down is not None:
        dataframes.append(df_down)

    if df_side is not None:
        dataframes.append(df_side)
    try:
        jsons=os.listdir(f'{cmpfolder}/{str(cmpnyid)}/New')
        for json in jsons:
            dir = os.path.basename(json).lower()
            if 'forward' in dir:
                json_fwd=json
                print(json_fwd)
            elif 'down' in dir:
                json_down=json
                print(json_down)
            elif 'side' in dir:
                json_side=json
                print(json_side)
    except Exception as e:
        print(f'{cmpnyid} not in reference folder{ipjs}')
        logging.critical(f'{cmpnyid} not in reference folder{ipjs}{e}')

    for df in dataframes:
        try:
            pose = df.iloc[0]['Pose']
            if pose=='STRAIGHT':
                face_recognition_process(f'{cmpfolder}/{cmpnyid}/New/{json_fwd}',df,cmpnyid)
                print(f'{pose}_completed')
            elif pose=='SIDE':
                face_recognition_process(f'{cmpfolder}/{cmpnyid}/New/{json_down}',df,cmpnyid)
                print(f'{pose}_completed')
            elif pose=='DOWN':
                face_recognition_process(f'{cmpfolder}/{cmpnyid}/New/{json_side}',df,cmpnyid)
                print(f'{pose}_completed')
        except IndexError:
            print("Index out of bounds. DataFrame may not have enough rows.")
            logging.critical("Index out of bounds. DataFrame may not have enough rows.")
        except Exception as e:
            logging.critical(f'final log error, line 156 {e}')


    processed_json='processed_json'
    if not os.path.exists(processed_json):
        os.makedirs(processed_json)
        
    shutil.move(ipjs,processed_json)
    print('move completed')



def final(filepath,ref_folder):
    files = os.listdir(f'{filepath}')
    for cmpid in files:
        print(cmpid)
        id_path = os.path.join(filepath,cmpid,'New')
        jsons = os.listdir(id_path)
        for json in jsons:
            if json.lower().endswith('.json'):
                path=os.path.join(id_path,json)
                results(path,ref_folder)
                # process_json_data(path, cmpid)
                print(path)
                print('completeddd')
            else:
                print(f'else {json}')








# final(r'C:\Users\user\Desktop\API_IN\API_IN\uploads\From-Local',r'C:\Users\user\Desktop\API_IN\API_IN\uploads\Spider-Man')

