"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    print(f'Loaded songs: {len(songs)}')

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    sample_taste_profile = {"favorite_genre": "lofi",
                     "favorite_mood": "relaxed",
                     "target_energy": 0.55,
                     "target_valence": 0.8,
                     "target_acousticness": 0.5}

    chill_lofi_profile = {"favorite_genre": "lofi", "favorite_mood": "chill",
                 "target_energy": 0.40, "target_valence": 0.58, "target_acousticness": 0.80}
    intense_rock_profile = {"favorite_genre": "rock", "favorite_mood": "intense",
                 "target_energy": 0.92, "target_valence": 0.48, "target_acousticness": 0.10}


    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
