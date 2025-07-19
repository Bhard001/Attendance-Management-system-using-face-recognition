import os
import cv2
import numpy as np

def get_images_and_labels():
    # Folder with images
    path = 'TrainingImage'

    # Initialize lists to hold the face images and corresponding labels
    faces = []
    labels = []

    # Load face cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Loop through all subdirectories in the folder
    for label_name in os.listdir(path):
        label_path = os.path.join(path, label_name)

        # Ensure we're processing only directories (subdirectories for each label)
        if os.path.isdir(label_path):
            print(f"Processing folder: {label_name}")

            # Extract label (numeric part) from the folder name (e.g., '053_premdubey' -> '053')
            label = label_name.split('_')[0]  # This will give you '053' from '053_premdubey'
            print(f"Label extracted: {label}")

            # Process each image file inside the subfolder
            for image_file in os.listdir(label_path):
                # Only process image files (jpg or png)
                if image_file.endswith('.jpg') or image_file.endswith('.png'):
                    img_path = os.path.join(label_path, image_file)

                    # Read the image
                    img = cv2.imread(img_path)

                    if img is None:
                        print(f"Failed to load image {image_file}")
                        continue

                    # Convert to grayscale (LBPH face recognizer requires grayscale images)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # Detect faces in the image
                    faces_detected = face_cascade.detectMultiScale(gray, 1.1, 4)

                    # Check if faces are detected
                    if len(faces_detected) == 0:
                        print(f"No faces detected in {image_file}.")
                        continue
                    else:
                        print(f"Faces detected in {image_file}.")

                    # Assuming that the first face detected is the one we want
                    for (x, y, w, h) in faces_detected:
                        # Crop the face out of the image
                        face = gray[y:y+h, x:x+w]

                        # Append the face and corresponding label to the lists
                        faces.append(face)
                        labels.append(int(label))  # Use the label as an integer

    # Check if we have faces and labels
    if len(faces) == 0:
        print("No faces found. Make sure you have images with faces in the 'TrainingImage' folder.")
        return None, None

    return faces, labels

def train_model():
    # Get the images and labels
    faces, labels = get_images_and_labels()

    # If we don't have faces and labels, exit
    if faces is None or labels is None:
        return

    # Create a recognizer (LBPH - Local Binary Patterns Histograms)
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Train the recognizer with the faces and labels
    recognizer.train(faces, np.array(labels))

    # Set the path to save the trained model in the 'TrainingImageLabel' folder
    save_path = 'TrainingImageLabel/Trainner.yml'  # Full path to save the model

    # Save the trained model to the specified path
    recognizer.save(save_path)
    print(f"Model trained and saved to '{save_path}'.")

# Call the train_model function to start training
train_model()
