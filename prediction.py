import torch
from torchvision import models, transforms
from PIL import Image

class Prediction_Model():
    def __init__(self):
        self.model = models.resnet18(weights='IMAGENET1K_V1')
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 2) 
        self.model.load_state_dict(torch.load("resnet18_audio_classification.pth"))
        self.model.eval() 
        self.data_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    def Prediction(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image = self.data_transform(image).unsqueeze(0)  
        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
    
        classes = ["Music", "Ads"]
        predicted_class = classes[predicted.item()]
        return predicted_class
