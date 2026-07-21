<div align="center">

# Mother's Day Poem Generator - GJU AI Club

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-8E75B2?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> Built with love by **Basel Al-Dwairi** for the **GJU AI Club**'s Mother's Day event at **German Jordanian University (GJU)**.

</div>
---

## About the Project

This project was created for the **Mother's Day event** hosted by the **GJU AI Club**. It's a two-part Streamlit application designed to turn heartfelt words into AI-generated poetry and celebrate them live, on-screen, in front of an audience.

The system works as a simple pipeline:

1. Attendees visit the **Poem Generator App**, enter their mother's name, pick a few traits (or write their own), choose a language, and generate a short, personalized poem powered by **Google's Gemini API**.
2. Each poem is saved to a shared **MongoDB Atlas** database.
3. The **Grand Ceremony App**, displayed on the event's main screen, automatically polls that same database and renders every new poem in a live, auto-refreshing gallery of glassmorphism-styled cards. Complete with a QR code so guests can jump straight into the generator from their phones.

The result: a live wall of love, growing in real time as the event unfolds.

---

## Features

### Poem Generator App
- Input a mother's name and choose up to 5 traits from a curated list (or add custom ones)
- Supports **4 languages**: English, Arabic, German, Russian
- Adjustable poem length and typing/animation speed via sidebar sliders
- AI-generated poems powered by `gemini-3-flash-preview`
- Smooth **typewriter-style animation** as the poem appears
- One-click **"Copy Poem to Clipboard"** button
- Poems are automatically saved to MongoDB Atlas with name, traits, language, prompt, and timestamp
- Custom Streamlit theming (styled buttons, hidden menu bar, branded background)

### Grand Ceremony App (Live Gallery)
- Real-time, **auto-refreshing dashboard** (every 10 seconds) built for a ceremony display screen
- Pulls the latest poems live from MongoDB Atlas, newest first
- **Glassmorphism-styled cards** showing the mother's name, poem, and local submission time
- Optimized MongoDB connection pooling (`maxPoolSize`, `minPoolSize`, fast timeouts) for stable performance under event-day traffic
- Built-in **QR code popover** so attendees can scan and generate their own poem instantly
- Clean, distraction-free full-screen layout ideal for projecting on stage

---

## Project Structure

```
.
├── data
│   ├── bg.jpeg
│   ├── black.jpg
│   ├── club_logo.PNG
│   ├── letter.jpg
│   ├── pink.jpg
│   ├── pink_texture.jpg
│   └── qr_code.png
├── notebook
│   └── prototype.ipynb
├── requirements.txt
└── src
    ├── atlas_db_delete.py
    ├── atlas.py
    ├── ceremony_app.py
    ├── configs.py
    ├── database_control.py
    ├── poem_generator_app.py
    ├── prompt_generator.py
    ├── testing.py
    └── utils.py
```

### Key files inside `src/`

| File | Purpose |
|---|---|
| `poem_generator_app.py` | Main Streamlit app - collects user input, calls the Gemini API, animates and displays the poem, and saves it to MongoDB. |
| `ceremony_app.py` | The live gallery/dashboard app for the ceremony screen, fetching and rendering poems in real time. |
| `prompt_generator.py` | Builds the structured prompt sent to Gemini based on selected traits, language, and desired poem length. |
| `utils.py` | Shared helper functions - MongoDB connection handling (`connect_atlas`), custom CSS/styling, background images, footer, logo/title rendering, and typewriter animation. |
| `configs.py` | Centralized configuration constants (Gemini model name, image filenames). |
| `atlas.py` | Lightweight helper for resolving the MongoDB Atlas connection URI from Streamlit secrets or environment variables. |
| `atlas_db_delete.py` | Standalone utility script for manually deleting specific documents from the database (used for cleanup/testing). |
| `database_control.py` | Simple script for direct MongoDB collection access, useful for ad hoc queries or debugging. |
| `testing.py` | Scratch file used for testing poem formatting/output during development. |

---

## Environment Variables & Configuration

Create a `.env` file in the project root (or configure equivalent **Streamlit secrets**) with the following variables:

| Variable | Description | Default |
|---|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key | - *(required)* |
| `ATLASDB_URI` | MongoDB Atlas connection URI | - *(required)* |
| `MONGO_DB` | Name of the MongoDB database to use | `mothers_day_db` |
| `MONGO_COLLECTION` | Name of the MongoDB collection to store poems in | `poems` |

**Example `.env` file:**

```env
GEMINI_API_KEY=your_gemini_api_key_here
ATLASDB_URI=your_mongodb_atlas_uri_here
MONGO_DB=mothers_day_db
MONGO_COLLECTION=poems
```

> If you're deploying on Streamlit Community Cloud, you can instead define these same keys in your app's `secrets.toml` file - the code automatically checks Streamlit secrets first, then falls back to `.env`.

---

## Installation & Local Setup

Follow these steps to run both apps locally:

### 1. Clone the repository

```bash
git clone https://github.com/Basel-Aldwairi/Mothers-Letter.git
cd mothers-day-poem-generator
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your environment variables

Create a `.env` file in the project root as described in the [Environment Variables](#️-environment-variables--configuration) section above, and add your own Gemini API key and MongoDB Atlas URI.

### 5. Run the Poem Generator App

```bash
streamlit run src/poem_generator_app.py
```

### 6. Run the Grand Ceremony App (in a separate terminal)

```bash
streamlit run src/ceremony_app.py
```

Once both apps are running, open the Poem Generator locally to create poems, and pull up the Ceremony App on a second screen/projector to watch them appear live.

---

## Note on Inactive Live Demo Links

> The original hosted apps - `mothers-day-poem.streamlit.app` and `mothers-day-ceremony.streamlit.app` - were used live during the GJU AI Club's Mother's Day event and are currently **offline/inactive**, since the original Gemini API key powering them has since been deactivated. To use the project today, please clone the repository and run both apps locally by supplying your **own** Gemini API key and MongoDB Atlas URI as described above.

---

## Credits

Developed with care by **Basel Al-Dwairi**, for the **GJU AI Club** at **German Jordanian University**, in celebration of Mother's Day.
