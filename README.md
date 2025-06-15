# PopcornPicks

PopcornPicks is a movie recommender web app built with Streamlit. Select a movie you like and get personalized recommendations with detailed information and posters.

## Features

- Movie selection from a curated list
- Top 5 similar movie recommendations
- Movie details: overview, genres, rating, release date, runtime, and poster
- Direct links to TMDb pages

## Project Structure

```
.
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── setup.sh              # Heroku setup script
├── procfile              # Heroku process file
├── .slugignore           # Heroku slugignore file
├── assets/
│   └── more_info.jpg     # Fallback image
├── models/
│   ├── movies_dict.pkl   # Movie metadata
│   └── similarity.pkl    # Similarity matrix
└── ml-model-training/    # Model training notebooks and data (not deployed)
```

## Getting Started

### Local Development

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd movie-recommender-app
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```sh
   streamlit run app.py
   ```

### Deploy on Heroku

1. **Ensure you have a Heroku account and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed.**

2. **Login to Heroku**
   ```sh
   heroku login
   ```

3. **Create a new Heroku app**
   ```sh
   heroku create your-app-name
   ```

4. **Deploy**
   ```sh
   git push heroku main
   ```

## Notes

- The `ml-model-training` folder contains Jupyter notebooks and raw data for model building. It is excluded from deployment.
- The app uses precomputed model files in the `models/` directory.

## License

This project is for educational purposes.

