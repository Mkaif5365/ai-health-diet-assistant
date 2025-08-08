# AI Health & Diet Assistant

A Flask web application that provides personalized diet plans and health advice using Google's Gemini AI.

## Features

- **Personalized Diet Plans**: Generate customized meal plans based on age, gender, weight, and height
- **Health Advice**: Get AI-powered health recommendations for symptoms or wellness goals
- **Modern UI**: Clean, responsive web interface
- **Real-time AI Responses**: Powered by Google Gemini 2.5 Flash

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key**:
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set the environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key-here"
     ```
   - Or the app will use a default key (not recommended for production)

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the app**:
   Open your browser and go to `http://localhost:5000`

## Usage

1. Enter your personal information (age, gender, weight, height)
2. Optionally add health symptoms or wellness goals
3. Click "Generate Plan" to get personalized diet and health advice
4. View the formatted results with proper styling

## Technologies Used

- **Backend**: Flask (Python)
- **AI**: Google Gemini 2.5 Flash
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with modern design

## Project Structure

```
my-app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main web interface
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## API Endpoints

- `GET/POST /`: Main application page with diet plan and health advice generation

## Security Notes

- The API key is currently hardcoded for development
- For production, use environment variables
- This is a demo application and should not be used for actual medical advice

## License

This project is for educational purposes only. 