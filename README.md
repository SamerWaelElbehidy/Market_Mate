# 🥬 MarketMate - AI-powered Produce Quality Scanner

**MarketMate** is a sophisticated Flask-based web API and admin dashboard that leverages advanced deep learning models to identify and assess the feshness and the quality of fruits and vegetables. The system combines ResNet18 and Google's Gemini AI for robust image classification and detailed Arabic analysis.

---

## 📌 Author

- **Name**: Samer Wael
- **Email**: [samer.wael.2003@gmail.com](mailto:samer.wael.2003@gmail.com)

---

## 🌟 Key Features

### 🤖 Advanced AI System
- **Dual Model Architecture**:
  - **ResNet18 Model**: Primary classification model trained on fresh/rotten produce
    - 20 distinct produce categories
    - High-precision fresh/rotten classification
    - Real-time performance optimization
    - Confidence scoring system
  - **Gemini AI Integration**:
    - Intelligent Arabic descriptions
    - Fallback analysis system
    - Natural language insights
    - Contextual understanding

### 🎯 Smart Classification
- **Supported Categories**:
  ```
  Fresh: Apple, Banana, Mango, Orange, Strawberry, 
         Carrot, Potato, Tomato, Cucumber, Bellpepper
  Rotten: Apple, Banana, Mango, Orange, Strawberry,
          Carrot, Potato, Tomato, Cucumber, Bellpepper
  ```
- Automatic categorization into specific folders (e.g., "FreshApple", "RottenBanana")
- Special handling for unrecognized items ("Other Item" category)
- Error detection and handling system

### 🔊 Intelligent Audio System
- Arabic voice feedback for predictions
- Text-to-speech integration
- Custom audio responses for:
  - Each produce category
  - Quality assessments
  - Error conditions
- Accessibility-focused design

### 📊 Enhanced Admin Dashboard & Analytics
- **Real-time Monitoring**:
  - Live prediction tracking
  - Device activity monitoring
  - System performance metrics
  - Error rate analysis
- **Data Management**:
  - Bulk image downloads
  - CSV export functionality
  - Category-wise data organization
  - Custom date range filtering
- **Interactive Data Visualization**:
  - Quality Distribution (Doughnut Chart):
    - Fresh vs Rotten vs Other items breakdown
    - Interactive segments with hover effects
    - Total predictions counter
  - Most Common Items (Horizontal Bar Chart):
    - Top 5 frequently scanned items
    - Color-coded categories
    - Responsive bar animations
  - Daily Activity (Line Chart):
    - 7-day activity timeline
    - Smooth curve interpolation
    - Point-based interaction
  - Prediction Confidence Levels (Bar Chart):
    - Confidence range distribution
    - Color-graded confidence bands
    - Average confidence indicator
  - Model Performance by Category (Wide Bar Chart):
    - Category-wise accuracy metrics
    - Detailed confidence analysis
    - Interactive tooltips
  - Usage Time Distribution (Line Chart):
    - 24-hour activity pattern
    - Peak usage identification
    - Time-based insights
- **Chart Features**:
  - Modern UI with smooth animations
  - Interactive tooltips with detailed data
  - Responsive design for all screen sizes
  - Custom color schemes for better visualization
  - Hover effects for enhanced user interaction
  - Legend customization for clarity
  - Automatic data updates
  - Cross-chart consistency in styling
- **Admin Interface**:
  - Admin account management
  - Device tracking and management
  - Image upload monitoring
  - Prediction result analysis
  - Feedback review system
- **Export Functionality**:
  - One-click download of all training data for model retraining
  - CSV exports of prediction history and statistics
  - Batch export of classified images by category
  - Feedback data exports for analysis

### 📱 Device Management
- Secure device registration system
- Unique device ID generation for API authentication
- Device activity tracking
- Usage analytics and reporting
- Cross-platform compatibility

### 🗣️ User Feedback System
- Voice message submission
- Feedback categorization
- Admin review interface
- Response tracking
- Analytics and reporting

### 💾 Data Organization
- **Automated File Management**:
  - Category-specific folders
  - Systematic naming conventions
  - Metadata preservation
  - Easy retrieval system
- **Database Integration**:
  - MongoDB optimization
  - Real-time updates
  - Data integrity checks
  - Backup mechanisms

### 🔐 Security Features
- Secure admin authentication
- Role-based access control
- API request validation
- Data encryption
- Activity logging

---

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **AI Models**: 
  - PyTorch (ResNet18)
  - Google Gemini AI
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Session-based
- **Image Processing**: PIL, OpenCV
- **Audio Processing**: pygame, gTTS

---

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/SamerWaelElbehidy/Market_Mate>
   cd flask
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Configuration & Usage

1. **Environment Setup**:
   ```bash
   # Configure MongoDB
   MONGO_URI=your_mongodb_uri
   
   # Set Gemini AI API Key
   GEMINI_API_KEY=your_api_key
   ```

2. **Initialize the Application**:
   ```bash
   python main.py
   ```

3. **Access Points**:
   - Admin Dashboard: `http://127.0.0.1:5000`
   - API Documentation: `http://127.0.0.1:5000/apidocs`

## 📱 Mobile App Integration

1. **API Endpoints**:
   - `/upload-image`: Image upload and analysis
   - `/feedback`: Voice feedback submission
   - `/device/register`: Device registration

2. **Response Format**:
   ```json
   {
     "prediction": "FreshApple",
     "confidence": 0.95,
     "audio_feedback": "url_to_audio"
   }
   ```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ResNet18 architecture
- Google Gemini AI
- Flask community
- MongoDB team
- Open-source contributors