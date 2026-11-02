import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(float(row["tempo_bpm"]))

            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    scores = {
        "energy": 1 - abs(song["energy"] - user_prefs["target_energy"]),
        "mood": 1.0 if song["mood"] == user_prefs["favorite_mood"] else 0.0,
        "valence": 1 - abs(song["valence"] - user_prefs["target_valence"]),
        "genre": 1.0 if song["genre"] == user_prefs["favorite_genre"] else 0.0,
        "acousticness": 1 - abs(song["acousticness"] - user_prefs["target_acousticness"]),
    }
    
    weights = {
        "energy": 0.30,
        "mood": 0.25,
        "valence": 0.20,
        "genre": 0.15,
        "acousticness": 0.10,
    }

    total = 0.0
    reasons = []

    for feature, weight in weights.items():
        contribution = weight * scores[feature]
        total += contribution

        if feature in ("mood", "genre"):
            label = f"{feature} match" if scores[feature] == 1.0 else f"{feature} mismatch"
        else:
            label = f"{feature} {'close' if scores[feature] >= 0.8 else 'far'}"
        reasons.append(f"{label} (+{contribution:.2f})")

    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
