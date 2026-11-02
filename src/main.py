"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

def print_recommendations(recommendations) -> None:
    """Prints each (song, score, explanation) as a numbered block with one reason per line."""
    width = 50
    print()
    print("=" * width)
    print("TOP RECOMMENDATIONS".center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 1.00")
        print("    Reasons:")
        for reason in explanation.split(", "):
            print(f"      - {reason}")

    print()
    print("=" * width)


def main() -> None:
    songs = load_songs("data/songs.csv") 

    print(f'Loaded songs: {len(songs)}')

    # Starter example profile
    user_prefs = {"favorite_genre": "lofi",
                     "favorite_mood": "relaxed",
                     "target_energy": 0.55,
                     "target_valence": 0.8,
                     "target_acousticness": 0.5}

    chill_lofi_profile = {"favorite_genre": "lofi", "favorite_mood": "chill",
                 "target_energy": 0.40, "target_valence": 0.58, "target_acousticness": 0.80}
    intense_rock_profile = {"favorite_genre": "rock", "favorite_mood": "intense",
                 "target_energy": 0.92, "target_valence": 0.48, "target_acousticness": 0.10}
    high_energy_pop_profile = {"favorite_genre": "pop", "favorite_mood": "happy",
                 "target_energy": 0.90, "target_valence": 0.80, "target_acousticness": 0.10}

    ADVERSARIAL_PROFILES = {
        # 1. Conflicting signals: mood says "sad", numbers say "upbeat"
        "sad_but_hyper": {
            "favorite_genre": "pop", "favorite_mood": "sad",
            "target_energy": 0.95, "target_valence": 0.95, "target_acousticness": 0.05,
        },
        # 2. Labels that don't exist in the catalog
        "ghost_labels": {
            "favorite_genre": "k-pop", "favorite_mood": "nostalgia",
            "target_energy": 0.60, "target_valence": 0.60, "target_acousticness": 0.50,
        },
        # 3. Near-miss / formatting labels
        "label_near_miss": {
            "favorite_genre": "Lo-Fi ", "favorite_mood": "relaxed",   # vs "lofi", "chill"
            "target_energy": 0.40, "target_valence": 0.58, "target_acousticness": 0.80,
        },
        # 4. Dead-center user
        "all_midpoint": {
            "favorite_genre": "jazz", "favorite_mood": "happy",
            "target_energy": 0.5, "target_valence": 0.5, "target_acousticness": 0.5,
        },
        # 5. Genre trap: genre match but every numeric feature is opposite
        "genre_trap": {
            "favorite_genre": "lofi", "favorite_mood": "intense",
            "target_energy": 0.95, "target_valence": 0.2, "target_acousticness": 0.0,
        },
        # 6. Out-of-range targets
        "out_of_range": {
            "favorite_genre": "rock", "favorite_mood": "intense",
            "target_energy": 3.0, "target_valence": -1.0, "target_acousticness": 0.5,
        },
        # 7. Bad input shape
        "missing_key": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8},
        "string_number": {
            "favorite_genre": "pop", "favorite_mood": "happy",
            "target_energy": "0.8", "target_valence": 0.8, "target_acousticness": 0.2,
        },
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)

    print_recommendations(recommend_songs(chill_lofi_profile, songs, k=5))
    print_recommendations(recommend_songs(intense_rock_profile, songs, k=5))
    print_recommendations(recommend_songs(high_energy_pop_profile, songs, k=5))

    print_recommendations(recommend_songs(ADVERSARIAL_PROFILES.get("sad_but_hyper"), songs, k=5))
    print_recommendations(recommend_songs(ADVERSARIAL_PROFILES.get("ghost_labels"), songs, k=5))
    print_recommendations(recommend_songs(ADVERSARIAL_PROFILES.get("label_near_miss"), songs, k=5))

if __name__ == "__main__":
    main()
