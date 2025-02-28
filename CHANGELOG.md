# Changelog

All notable changes to this project will be documented in this file.

## [0.0.5] - 2025-02-28

- Rearranging code

## [0.0.4] - 2025-02-13

- `Persistence` layer added `MongoDB Atlas`
- Improvements in `UI`:
  - Divide page into sections: `YouTube Video Info`, `Generate Quiz`, `Quiz`
  - Renamed Streamlit `app.py` into `generator.py`
  - Added Streamlit `quiz.py` with the Quiz-Answering Engine

## [0.0.3] - 2025-02-08

### Changed

- `utils` folder added with `helpers.py` file, including `convert_seconds_to_text` function to convert number of seconds to a human-readed text
- `engine` filder added with first draft of Quizzer Engine
- `jupyther notebook` added, in order to do some NLP experiments `experiments.ipynb` with the YT transcribed text
- Moved `Streamlit` UI into `ui-streamlit` folder
- Created `ui-reflex` folder, but now without any code

## [0.0.2] - 2025-02-08

### Changed

- First draft of general idea how the app will work was sketched
- Added first structure of catalogues
- `README.md`, `CHANGELOG.md` were created
- Created `transcript_extractor.py` to get the transcript of YT video
- Stub of UI in `Streamlit` added `(UI\app.py)`

## [0.0.1] - 2025-02-06

### Changed

- Hello World!

### Fixed
