import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from sklearn.svm import SVC
import pickle
import os

# 1. Configurações
FACENET_MODEL = 'modelo_facenet.h5'
CLASSIFIER = 'classificador.pkl'
TRAIN_DATA = 'fotos'

# 2. Detecção Facial
detector = MTCNN()

def detectar_rostos(img):
    return [rosto['box'] for rosto in detector.detect_faces(img)]

# 3. Extração de Features
modelo = load_model(FACENET_MODEL)

def extrair_features(rosto):
    rostro = cv2.resize(rosto, (160, 160))
    rostro = (rostro - rostro.mean()) / rostro.std()
    return modelo.predict(np.expand_dims(rostro, axis=0))[0]

# 4. Treinar Classificador (executar uma vez)
def treinar_classificador():
    features, labels = [], []
    
    for pessoa in os.listdir(TRAIN_DATA):
        for foto in os.listdir(f'{TRAIN_DATA}/{pessoa}'):
            img = cv2.imread(f'{TRAIN_DATA}/{pessoa}/{foto}')
            x,y,w,h = detectar_rostos(img)[0]
            features.append(extrair_features(img[y:y+h, x:x+w]))
            labels.append(pessoa)
    
    classificador = SVC(kernel='linear', probability=True)
    classificador.fit(features, labels)
    
    with open(CLASSIFIER, 'wb') as f:
        pickle.dump(classificador, f)

# 5. Reconhecimento em Tempo Real
def reconhecer():
    with open(CLASSIFIER, 'rb') as f:
        classificador = pickle.load(f)
    
    cap = cv2.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        rostos = detectar_rostos(frame)
        
        for (x,y,w,h) in rostos:
            features = extrair_features(frame[y:y+h, x:x+w])
            pessoa = classificador.predict([features])[0]
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, pessoa, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        
        cv2.imshow('Reconhecimento Facial', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if not os.path.exists(CLASSIFIER):
        treinar_classificador()
    reconhecer()
