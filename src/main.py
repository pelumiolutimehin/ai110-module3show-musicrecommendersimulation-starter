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


    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)
    print_recommendations(recommend_songs(chill_lofi_profile, songs, k=5))

if __name__ == "__main__":
    main()
