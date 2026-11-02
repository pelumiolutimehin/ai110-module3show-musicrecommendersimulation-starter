# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real-world recommendations work

Platforms like Spotify and YouTube predict what you'll like next with a pipeline: they narrow millions of items to a few hundred candidates, score each one with a model, then re-rank the results for variety. They learn from two kinds of data. **Collaborative filtering** uses other users' behavior ("people who listen like you also liked X"). **Content-based filtering** uses the attributes of the songs themselves (tempo, energy, mood). Collaborative filtering is good at surprising discoveries but struggles with brand-new songs. Content-based filtering handles new songs well but tends to keep recommending more of the same.

### What my version prioritizes

My simulation is **content-based**, because the dataset has only song attributes and no listening history from other users. It prioritizes **closeness to the user's taste**, not "higher is better": a user who wants calm music should get songs with low energy, not high energy. Mood counts for slightly more than genre. Mood describes how a song feels, and the catalog is too small for many songs to share a genre.

### Features

**`Song` features** (from `songs.csv`):

- `genre`
- `mood`
- `energy` (0 to 1)
- `valence` (0 to 1, how positive the song sounds)
- `acousticness` (0 to 1)

Left out on purpose: `tempo_bpm` and `danceability` mostly repeat what energy already shows, and `id`, `title`, and `artist` are only labels.

**`UserProfile` features** (the user's targets):

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_valence`
- `target_acousticness`

### Scoring Rule (one song)

Each numeric feature gets a closeness score: `1 - |song value - user target|`, so a perfect match scores 1. Genre and mood score 1 for a match and 0 otherwise. The total is a weighted sum:

| Feature | Weight |
|---|---|
| energy | 0.30 |
| mood | 0.25 |
| valence | 0.20 |
| genre | 0.15 |
| acousticness | 0.10 |

### Ranking Rule (list of songs)

The recommender scores every song in the catalog, sorts them from highest to lowest score, and returns the top K (for example, 5).

### Data Flow

```
INPUT                      PROCESS (loop over every song)           OUTPUT
-----                      ------------------------------           ------
UserProfile  ─┐            for each song in the catalog:             sort by score,
  genre       │              score_song(user, song)                  highest first
  mood        ├──────────►     categorical: mood, genre (1 or 0)       │
  energy      │                numeric: 1 - |song - target|            ▼
  valence     │                weighted sum -> total score          keep top K
  acousticness│              append (song, score, reasons)             │
songs.csv ────┘                                                        ▼
  load_songs() -> list of songs                                    K recommendations
k (e.g. 5) ────────────────────────────────────────────────────────► (title, score, why)
```

| Stage | Function | Job |
|---|---|---|
| Input | `load_songs(path)` and `UserProfile` | Read the CSV and convert numeric columns to floats |
| Process | `score_song(user, song)` | One song in, one score and a per-feature breakdown out |
| Output | `recommend_songs(user, songs, k)` | Run the loop, sort once after it finishes, return the first K |

### Algorithm Recipe

1. **Load** every song from `data/songs.csv`.
2. **For each song**, compute five feature scores, each between 0 and 1:
   - `mood_score` = 1 if `song.mood == favorite_mood`, else 0
   - `genre_score` = 1 if `song.genre == favorite_genre`, else 0
   - `energy_score` = `1 - |song.energy - target_energy|`
   - `valence_score` = `1 - |song.valence - target_valence|`
   - `acousticness_score` = `1 - |song.acousticness - target_acousticness|`
3. **Combine** them into one total with the weights in the table above:
   `total = 0.30*energy + 0.25*mood + 0.20*valence + 0.15*genre + 0.10*acousticness`
   The weights sum to 1.0, so the total is also between 0 and 1.
4. **Explain**: keep each feature's contribution so every result can say why it ranked where it did (for example, "mood match, energy close").
5. **Rank**: sort all songs by total score, highest first. Break ties by the higher mood score, then by CSV order.
6. **Return** the top K songs with their scores and explanations.

### Expected Biases

- **Exact-match labels:** genre and mood are all-or-nothing, so a near-miss like "relaxed" vs "chill" gets zero credit.
- **Genre in a small catalog:** if the user's genre has only a few songs, a genre match can outrank better mood and energy matches.
- **Compressed numeric scores:** `1 - |diff|` keeps most songs between 0.6 and 0.95, so the numeric features separate songs less than their weights suggest.
- **One taste per user:** a single target per feature averages out users who like very different kinds of songs.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output for the chill lofi profile (`favorite_genre=lofi`, `favorite_mood=chill`, `target_energy=0.40`, `target_valence=0.58`, `target_acousticness=0.80`):

```
==================================================
               TOP RECOMMENDATIONS
==================================================

#1  Midnight Coding by LoRoom
    Score: 0.98 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood match (+0.25)
      - valence close (+0.20)
      - genre match (+0.15)
      - acousticness close (+0.09)

#2  Library Rain by Paper Lanterns
    Score: 0.97 / 1.00
    Reasons:
      - energy close (+0.28)
      - mood match (+0.25)
      - valence close (+0.20)
      - genre match (+0.15)
      - acousticness close (+0.09)

#3  Spacewalk Thoughts by Orbit Bloom
    Score: 0.79 / 1.00
    Reasons:
      - energy close (+0.26)
      - mood match (+0.25)
      - valence close (+0.19)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

#4  Focus Flow by LoRoom
    Score: 0.75 / 1.00
    Reasons:
      - energy close (+0.30)
      - mood mismatch (+0.00)
      - valence close (+0.20)
      - genre match (+0.15)
      - acousticness close (+0.10)

#5  Dusty Porch Swing by Willow Creek Band
    Score: 0.56 / 1.00
    Reasons:
      - energy close (+0.28)
      - mood mismatch (+0.00)
      - valence close (+0.18)
      - genre mismatch (+0.00)
      - acousticness close (+0.10)

==================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



