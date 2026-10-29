# WearableLens AI - Premium Wearable Tech Identification Website

A fully functional, modern, responsive website that helps users identify wearable electronic devices from photos with AI-powered analysis and detailed information.

## Features

- AI-powered device identification from uploaded photos
- Detailed device information including category, functions, typical users, and price
- Manual search fallback when AI analysis is unavailable
- Device comparison tool with side-by-side feature comparison
- Premium dark theme with cyan accents and elegant UI
- Fully responsive design for mobile and desktop
- Privacy-focused with no mandatory accounts or data storage

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (React not used - vanilla JS for simplicity)
- **Backend**: Python Flask
- **AI Integration**: Configurable AI providers (OpenAI, Google Gemini, custom)
- **Database**: In-memory device database (can be extended to SQLite/PostgreSQL)
- **Deployment**: Free-tier hosting options (Heroku, Render, Railway)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/wearable-lens-ai.git
cd wearable-lens-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env to configure your settings
```

### 4. Run the application
```bash
python app.py
```

### 5. Access the website
Open your browser and go to: http://localhost:5000

## Deployment Options

### Heroku
1. Create a new app on Heroku
2. Connect your GitHub repository
3. Set environment variables in Heroku dashboard
4. Deploy

### Render.com
1. Create a new Web Service
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Add environment variables

### Docker
```bash
docker build -t wearable-lens-ai .
docker run -p 5000:5000 --env-file .env wearable-lens-ai
```

## Key Features

### AI Device Identifier
- Upload or capture device photo
- Display uploaded image before analysis
- Analyze design, shape, placement, and features
- Return possible matches with confidence estimates
- Clear distinction between verified facts and AI guesses
- Manual search fallback option

### Device Information
- Product name and manufacturer
- Product category
- Main functions
- Typical users
- Common use cases
- Compatibility and requirements
- Advantages and limitations
- Approximate price and official purchase links

### Is This Device Right for Me?
- Ask users about intended purpose, budget, and preferred features
- Generate neutral comparison and recommendation without assuming necessity

### Product Comparison
- Compare multiple devices by price, features, compatibility, battery life, and privacy features
- Display unknown specifications as "Not verified" instead of inventing values

## Backend and AI Integration

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Image-analysis API integration through configurable provider
- Server-side API key management using environment variables
- Input validation, upload-size limits, file-type validation, and rate limiting
- Safe error handling and logging without exposing API keys or sensitive user data

## Privacy and Security

- No mandatory account or sign-in
- No permanent storage of uploaded images by default
- Never expose secret API keys in frontend JavaScript, HTML, or public repositories
- Validate uploaded files and reject unsupported formats
- Explain how images are processed and whether an external AI provider receives them
- Do not upload private photos without user consent

## Required Pages

1. Home
2. Identify a Device
3. Explore Wearable Technology
4. Compare Devices
5. Privacy and Security
6. About

## Technical Requirements

- Build a complete working project, not just a static mockup
- Include all frontend and backend source files
- Provide requirements.txt, .env.example, and a README with Android-friendly setup instructions
- Include loading indicators, empty states, error messages, and accessible controls
- Make the project deployable using a suitable free-tier hosting service where available
- Use modular, maintainable code and test the major user flows

## Final Deliverable

Deliver the complete project structure, working source code, setup instructions, API configuration guide, security notes, and deployment steps. Prioritize factual device identification, privacy, mobile usability, and a polished premium experience.