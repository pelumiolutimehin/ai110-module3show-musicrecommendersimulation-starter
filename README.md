# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a content-based recommender. A user gives a favorite genre, a favorite mood, and target energy, positivity, and acoustic levels. It scores all 20 songs in `data/songs.csv` and returns the top 5, each with reasons like "mood match (+0.25)".

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

Terminal output from `python -m src.main` for each profile (top 5 songs).

### Standard profiles

#### `chill_lofi_profile`

favorite_genre=lofi, favorite_mood=chill, target_energy=0.40, target_valence=0.58, target_acousticness=0.80

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

#### `intense_rock_profile`

favorite_genre=rock, favorite_mood=intense, target_energy=0.92, target_valence=0.48, target_acousticness=0.10

```
==================================================
               TOP RECOMMENDATIONS
==================================================

#1  Storm Runner by Voltline
    Score: 1.00 / 1.00
    Reasons:
      - energy close (+0.30)
      - mood match (+0.25)
      - valence close (+0.20)
      - genre match (+0.15)
      - acousticness close (+0.10)

#2  Gym Hero by Max Pulse
    Score: 0.78 / 1.00
    Reasons:
      - energy close (+0.30)
      - mood match (+0.25)
      - valence far (+0.14)
      - genre mismatch (+0.00)
      - acousticness close (+0.10)

#3  Night Drive Loop by Neon Echo
    Score: 0.53 / 1.00
    Reasons:
      - energy close (+0.25)
      - mood mismatch (+0.00)
      - valence close (+0.20)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

#4  Concrete Crown by Verse Alchemy
    Score: 0.53 / 1.00
    Reasons:
      - energy close (+0.26)
      - mood mismatch (+0.00)
      - valence close (+0.17)
      - genre mismatch (+0.00)
      - acousticness close (+0.10)

#5  Iron Cathedral by Black Meridian
    Score: 0.53 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence far (+0.15)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

==================================================
```

#### `high_energy_pop_profile`

favorite_genre=pop, favorite_mood=happy, target_energy=0.90, target_valence=0.80, target_acousticness=0.10

```
==================================================
               TOP RECOMMENDATIONS
==================================================

#1  Sunrise City by Neon Echo
    Score: 0.96 / 1.00
    Reasons:
      - energy close (+0.28)
      - mood match (+0.25)
      - valence close (+0.19)
      - genre match (+0.15)
      - acousticness close (+0.09)

#2  Rooftop Lights by Indigo Parade
    Score: 0.78 / 1.00
    Reasons:
      - energy close (+0.26)
      - mood match (+0.25)
      - valence close (+0.20)
      - genre mismatch (+0.00)
      - acousticness far (+0.08)

#3  Gym Hero by Max Pulse
    Score: 0.73 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence close (+0.19)
      - genre match (+0.15)
      - acousticness close (+0.10)

#4  Neon Pulse Festival by Drop Theory
    Score: 0.56 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence close (+0.18)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

#5  Calle Sol by Los Marea
    Score: 0.55 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence close (+0.18)
      - genre mismatch (+0.00)
      - acousticness close (+0.08)

==================================================
```

### Adversarial profiles

#### `sad_but_hyper`

favorite_genre=pop, favorite_mood=sad, target_energy=0.95, target_valence=0.95, target_acousticness=0.05. Mood conflicts with the numeric targets.

```
==================================================
               TOP RECOMMENDATIONS
==================================================

#1  Gym Hero by Max Pulse
    Score: 0.71 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence close (+0.16)
      - genre match (+0.15)
      - acousticness close (+0.10)

#2  Sunrise City by Neon Echo
    Score: 0.68 / 1.00
    Reasons:
      - energy close (+0.26)
      - mood mismatch (+0.00)
      - valence close (+0.18)
      - genre match (+0.15)
      - acousticness close (+0.09)

#3  Neon Pulse Festival by Drop Theory
    Score: 0.58 / 1.00
    Reasons:
      - energy close (+0.30)
      - mood mismatch (+0.00)
      - valence close (+0.19)
      - genre mismatch (+0.00)
      - acousticness close (+0.10)

#4  Calle Sol by Los Marea
    Score: 0.54 / 1.00
    Reasons:
      - energy close (+0.27)
      - mood mismatch (+0.00)
      - valence close (+0.19)
      - genre mismatch (+0.00)
      - acousticness far (+0.08)

#5  Delta Midnight by Old Man Hayes
    Score: 0.51 / 1.00
    Reasons:
      - energy far (+0.16)
      - mood match (+0.25)
      - valence far (+0.07)
      - genre mismatch (+0.00)
      - acousticness far (+0.03)

==================================================
```

#### `ghost_labels`

favorite_genre=k-pop, favorite_mood=nostalgia, target_energy=0.60, target_valence=0.60, target_acousticness=0.50. Neither label exists in the catalog.

```
==================================================
               TOP RECOMMENDATIONS
==================================================

#1  Velvet Hours by Sade Monroe
    Score: 0.55 / 1.00
    Reasons:
      - energy close (+0.28)
      - mood mismatch (+0.00)
      - valence close (+0.19)
      - genre mismatch (+0.00)
      - acousticness close (+0.08)

#2  Island Breeze by Rootsy Tide
    Score: 0.54 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence far (+0.16)
      - genre mismatch (+0.00)
      - acousticness close (+0.10)

#3  Midnight Coding by LoRoom
    Score: 0.52 / 1.00
    Reasons:
      - energy close (+0.25)
      - mood mismatch (+0.00)
      - valence close (+0.19)
      - genre mismatch (+0.00)
      - acousticness far (+0.08)

#4  Focus Flow by LoRoom
    Score: 0.51 / 1.00
    Reasons:
      - energy close (+0.24)
      - mood mismatch (+0.00)
      - valence close (+0.20)
      - genre mismatch (+0.00)
      - acousticness far (+0.07)

#5  Dusty Porch Swing by Willow Creek Band
    Score: 0.51 / 1.00
    Reasons:
      - energy close (+0.26)
      - mood mismatch (+0.00)
      - valence close (+0.18)
      - genre mismatch (+0.00)
      - acousticness far (+0.07)

==================================================
```

#### `label_near_miss`

favorite_genre="Lo-Fi ", favorite_mood=relaxed, target_energy=0.40, target_valence=0.58, target_acousticness=0.80. Near-miss labels (the catalog uses `lofi`).

```
==================================================
               TOP RECOMMENDATIONS
==================================================

#1  Coffee Shop Stories by Slow Stereo
    Score: 0.81 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood match (+0.25)
      - valence close (+0.17)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

#2  Focus Flow by LoRoom
    Score: 0.60 / 1.00
    Reasons:
      - energy close (+0.30)
      - mood mismatch (+0.00)
      - valence close (+0.20)
      - genre mismatch (+0.00)
      - acousticness close (+0.10)

#3  Midnight Coding by LoRoom
    Score: 0.58 / 1.00
    Reasons:
      - energy close (+0.29)
      - mood mismatch (+0.00)
      - valence close (+0.20)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

#4  Library Rain by Paper Lanterns
    Score: 0.57 / 1.00
    Reasons:
      - energy close (+0.28)
      - mood mismatch (+0.00)
      - valence close (+0.20)
      - genre mismatch (+0.00)
      - acousticness close (+0.09)

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

- **Removed the mood check.** The #1 song for the chill lofi profile changed from Midnight Coding to Focus Flow, a "focused" song, and scores topped out at 0.75. I restored it afterward.
- **Different types of users.** Chill lofi, intense rock, and high-energy pop each got sensible, different lists (see the sample output above).
- **Stress-test profiles.**
  - `sad_but_hyper` got upbeat pop, because energy outvoted the "sad" mood.
  - `ghost_labels` got a near-random list scored 0.55 to 0.51.
  - `label_near_miss` lost every genre match to a stray capital letter and space.
- **Self-match check.** Each of the 20 songs ranks #1 for a profile built from its own traits.

I did not try changing the weights or adding tempo.

---

## Limitations and Risks

- It only works on a tiny catalog: 20 songs, and 14 of the 17 genres have just one.
- Genre and mood are exact matches, so "relaxed" gets no credit for "chill" and typos break matches.
- It ignores tempo, danceability, lyrics, and language.
- It assumes one taste per user.
- Pop songs like Gym Hero can show up for a "happy pop" user because genre and energy outweigh a mismatched mood.

See the [model card](model_card.md) for more.

---

## Reflection

[**Model Card**](model_card.md)

A recommender turns data into predictions by comparing a user's stated taste to each item's traits, scoring each trait, and adding the scores up. Mine only adds five numbers, yet the results felt like real recommendations, especially with the reasons shown next to each song.

Bias shows up in small choices. Genre and mood are all-or-nothing labels worth 40% of the score, so users whose tastes match the catalog are served better than everyone else. One label can change the top pick. In a bigger system, the same kind of choice would shape what millions of people see.



