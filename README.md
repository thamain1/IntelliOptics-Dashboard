🌟 IntelliOptics Dashboard
A web-based AI-powered dashboard using Groundlight AI for real-time object detection and analytics.

🚀 Features
📡 WebSocket Integration for real-time AI updates
🎨 Modern UI with Radix UI & TailwindCSS
📊 Interactive Graphs using Recharts.js
🔐 Secure API Communication with FastAPI & Socket.io
🖥 Deployment Ready (Azure, Docker, GitHub Actions)
🛠 Setup & Installation
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/IntelliOptics-Dashboard.git
cd IntelliOptics-Dashboard
2️⃣ Install Backend Dependencies
bash
Copy
Edit
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Install Frontend Dependencies
bash
Copy
Edit
cd ../frontend
npm install
4️⃣ Start Backend Server
bash
Copy
Edit
cd backend
uvicorn main:app --reload --host=0.0.0.0 --port=8000
5️⃣ Start Frontend
bash
Copy
Edit
cd ../frontend
npm run dev
📡 API Endpoints
Method	Endpoint	Description
GET	/api/detectors	Fetch all AI detectors
POST	/api/submit	Submit an image for analysis
WebSocket	/socket.io/	Live AI model updates
🎨 UI Preview

💡 Contributing
Fork the repository 🍴
Create a feature branch git checkout -b feature-name
Commit changes git commit -m "Added new feature"
Push and open a Pull Request
📝 License
MIT License - See LICENSE for details.

📧 Contact
👤 Jesse Morgan
📧 jmorgan@4wardmotion.co
🌐 thamain1

