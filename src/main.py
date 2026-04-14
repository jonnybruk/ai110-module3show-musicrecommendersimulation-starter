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

    # Test profile: Lo-fi, Chill, Low Energy
    user_prefs = {
        "fav_genre": "lofi",
        "fav_mood": "chill",
        "target_energy": 0.3,
        "likes_acoustic": False
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # Each rec is now a song dict with added 'score' and 'reasons'
        score = rec['score']
        reasons = rec['reasons']
        print(f"{rec['title']} - Score: {score:.3f}")
        print(f"Because: {' | '.join(reasons)}")
        print()


if __name__ == "__main__":
    main()
