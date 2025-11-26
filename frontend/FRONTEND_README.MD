# Semantic Search Mobile App 📱

A beautiful, modern Flutter application that demonstrates the power of vector semantic search. This app connects to our FastAPI backend to provide real-time, AI-powered search results.

## ✨ Features

- **🎨 Modern Article-Style UI**: Clean, minimalist design using the "Outfit" font family.
- **⚡ Real-Time Semantic Search**: Connects directly to the Pinecone-powered backend.
- **🎬 Smooth Animations**: Staggered entry animations for a premium user experience.
- **🏆 Smart Relevance**: Highlights the top match and displays similarity scores.
- **📱 Cross-Platform**: Runs smoothly on both iOS and Android.

## 🛠️ Tech Stack

- **Framework**: Flutter (Dart)
- **State Management**: `setState` (Simple & Effective for this demo)
- **Networking**: `http` package
- **Typography**: `google_fonts`
- **Animations**: `flutter_animate`

## 🚀 Getting Started

### Prerequisites

- Flutter SDK installed (version 3.0.0 or higher)
- Dart SDK
- An Android Emulator or iOS Simulator (or physical device)

### Installation

1. **Navigate to the app directory:**

   ```bash
   cd frontend/v_mobile_app
   ```

2. **Install dependencies:**

   ```bash
   flutter pub get
   ```

3. **Run the application:**
   ```bash
   flutter run
   ```

## 📱 Application Structure

```
lib/
├── main.dart           # Entry point and main application logic
└── ...
```

### Key Components

- **`SearchService`**: Handles API communication with the backend.
- **`SearchResult`**: Data model for parsing JSON responses.
- **`SemanticSearchPage`**: The main screen containing the UI logic.
- **`HeaderWidget`**: Displays the "Discover" title.
- **`SearchBarWidget`**: The floating search input field.
- **`ResultsListWidget`**: Displays the list of search results.
- **`ResultCardWidget`**: Individual card for each search result.

## 🔌 API Integration

The app connects to the deployed backend at:
`https://devfest-abeokuta-2025-vector-semantic-q0w3.onrender.com`

It sends a POST request to `/api/search` with the following body:

```json
{
  "query": "your search query",
  "top_k": 10,
  "index_name": "embedding-search"
}
```

## 🤝 Contributing

Feel free to fork this repository and submit pull requests to improve the UI or add new features!
