import os
import io
import re
import socket
import pygame
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import google.generativeai as genai
from gtts import gTTS
from torchvision.models import resnet18, ResNet18_Weights

class PredictService:
    def __init__(self):
        self.target_classes = [
            "FreshApple", "FreshBanana", "FreshMango", "FreshOrange", "FreshStrawberry",
            "RottenApple", "RottenBanana", "RottenMango", "RottenOrange", "RottenStrawberry",
            "FreshCarrot", "FreshPotato", "FreshTomato", "FreshCucumber", "FreshBellpepper",
            "RottenCarrot", "RottenPotato", "RottenTomato", "RottenCucumber", "RottenBellpepper"
        ]
        self.upload_folder = 'static/uploads'
        self.model = self.load_model()
        self.gemini_api_key = "AIzaSyDPWdijox2LjOj9p5sUeoB190Ht-DN5MF4"
        pygame.mixer.init()

    def load_model(self):
        weights = ResNet18_Weights.DEFAULT
        model = resnet18(weights=weights)
        model.fc = nn.Linear(model.fc.in_features, len(self.target_classes))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        model.load_state_dict(torch.load("Model/best_model.pth", map_location=device))
        model.eval()
        return model

    def has_internet(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception:
            return False

    def predict_local(self, image_path):
        if not os.path.exists(image_path):
            return "Error", 0, True

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            max_prob, predicted = torch.max(probabilities, 1)
            confidence = max_prob.item()

        predicted_class = self.target_classes[predicted.item()]

        # Play audio based on prediction
        try:
            if confidence < 0.6:
                pygame.mixer.music.load("audio/error.mp3")
                predicted_class = "Other Item"
            else:
                audio_path = f"audio/{predicted_class}.mp3"
                pygame.mixer.music.load(audio_path)
        except Exception as e:
            print(f"Error loading audio: {e}")
            pygame.mixer.music.load("audio/Error.mp3")

        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        return predicted_class, confidence, False

    def predict_gemini(self, image_path):
        try:
            genai.configure(api_key=self.gemini_api_key)
            model_gemini = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

            img = Image.open(image_path)
            prompt = ("What do you see in this image?, describe it in Arabic only, only mention the object and its name, "
                    "and if it is fruits or vegetables, if it is one of the following: apple, banana, mango, orange, strawberry, carrot, potato, tomato, cucumber, bellpepper you must tell me if it is fresh or rotten, if there is more than one main object in the image, mention all of them.")
            
            response = model_gemini.generate_content([prompt, img], generation_config={"temperature": 0.4})
            caption = response.text.strip()

            # Extract Arabic text
            arabic_only = re.findall(r'[\u0600-\u06FF\s،؟]+', caption)
            arabic_text = ''.join(arabic_only).strip()

            # Convert to speech
            mp3_fp = io.BytesIO()
            tts = gTTS(text=arabic_text, lang='ar')
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            # Play the Arabic speech
            pygame.mixer.music.load(mp3_fp, 'mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Map Arabic description to our categories
            arabic_text_lower = arabic_text.lower()
            
            # Check for freshness
            is_fresh = "طازج" in arabic_text or "طازجة" in arabic_text
            is_rotten = "فاسد" in arabic_text or "فاسدة" in arabic_text or "متعفن" in arabic_text or "متعفنة" in arabic_text
            
            # Check for specific items
            has_apple = "تفاح" in arabic_text
            has_banana = "موز" in arabic_text
            has_mango = "مانجو" in arabic_text
            has_orange = "برتقال" in arabic_text
            has_strawberry = "فراولة" in arabic_text
            has_carrot = "جزر" in arabic_text
            has_potato = "بطاطس" in arabic_text or "بطاطا" in arabic_text
            has_tomato = "طماطم" in arabic_text
            has_cucumber = "خيار" in arabic_text
            has_bellpepper = "فلفل" in arabic_text

            # Map to specific categories
            if has_apple:
                item = "Apple"
            elif has_banana:
                item = "Banana"
            elif has_mango:
                item = "Mango"
            elif has_orange:
                item = "Orange"
            elif has_strawberry:
                item = "Strawberry"
            elif has_carrot:
                item = "Carrot"
            elif has_potato:
                item = "Potato"
            elif has_tomato:
                item = "Tomato"
            elif has_cucumber:
                item = "Cucumber"
            elif has_bellpepper:
                item = "Bellpepper"
            else:
                return "Other Item", 0.7, False

            # Combine freshness with item
            if is_fresh:
                predicted_class = f"Fresh{item}"
            elif is_rotten:
                predicted_class = f"Rotten{item}"
            else:
                return "Other Item", 0.7, False

            # Validate the predicted class
            if predicted_class in self.target_classes:
                return predicted_class, 0.9, False
            else:
                return "Other Item", 0.7, False

        except Exception as e:
            print(f"Gemini API error: {e}")
            return None

    def predict(self, image_path):
        if not os.path.exists(image_path):
            return "Error", 0, True

        if self.has_internet():
            # Try Gemini API first
            result = self.predict_gemini(image_path)
            if result is not None:
                return result

        # Fall back to local model if Gemini fails or no internet
        return self.predict_local(image_path)