import logging
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from torchvision import transforms
from PIL import Image
from scipy.spatial.distance import cosine
import numpy as np

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger('facenet')

class Facenet:
    def __init__(self, gate):
        self.gate = gate

        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        log.info('Running on device: {}'.format(self.device))

        self.mtcnn = MTCNN(
            image_size=160, margin=20, min_face_size=20,
            thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
            device=self.device
        ).eval()

        self.resnet = InceptionResnetV1(pretrained='vggface2', device=self.device).eval().to(self.device)
        self.loader = transforms.Compose([
            transforms.Resize((224, 224)), transforms.ToTensor()])

        self.people_database = []

    def detect_faces(self, frame):
        # Detect faces
        boxes, _ = self.mtcnn.detect(frame)
        if boxes is None:
            return []  # No faces detected
        return boxes

    def recognize_face(self, face):
        # Embed face
        embedded_face = self.resnet(face.unsqueeze(0))
        return embedded_face

    def compare_faces(self, new_feature_vector):
        threshold = 0.5  
        for person in self.people_database:
            dist = cosine(new_feature_vector, person['feature_vector'])
            if dist < threshold:
                return True, person  # Return True and the person if a similar face is found
        return False, None  # Return False if no similar face is found

    def detect_and_compare_faces(self, image):
        boxes, _ = self.mtcnn.detect(image)
        if boxes is not None:
            # For simplicity, consider only the first detected face
            box = boxes[0]
            face = image[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
            face = Image.fromarray(face)
            face_tensor = self.loader(face).unsqueeze(0).to(self.device)

            with torch.no_grad():
                feature_vector = self.resnet(face_tensor).flatten().cpu().numpy()

            is_known, person = self.compare_faces(feature_vector)
            return is_known, person, box, feature_vector
        return False, None, None, None