from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import math

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
    """Load songs from a CSV file into dictionaries and parse numeric fields."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to float
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'].lower(),
                    'mood': row['mood'].lower(),
                    'energy': float(row['energy']),
                    'tempo_bpm': int(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found")
        return []
    print(f"Loaded {len(songs)} songs\n")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a weighted song score from genre match and energy similarity."""
    score = 0.0
    reasons = []
    
    # Genre match: +2.0 points
    if song['genre'].lower() == user_prefs.get('fav_genre', '').lower():
        score += 2.0
        reasons.append('genre match (+2.0)')
    
    # Energy similarity: 1.0 - |difference|, minimum 0
    energy_diff = abs(user_prefs.get('target_energy', 0.5) - song['energy'])
    energy_score = max(0.0, 1.0 - energy_diff)
    score += energy_score
    reasons.append(f'energy similarity (+{energy_score:.2f})')
    
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Dict]:
    """Score all songs, sort them by score, and return the top k recommendations."""
    recommendations = []
    
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        song_copy = song.copy()  # Avoid modifying original song dict
        song_copy['score'] = score
        song_copy['reasons'] = reasons
        recommendations.append(song_copy)
    
    # Sort by score descending using lambda
    recommendations.sort(key=lambda s: s['score'], reverse=True)
    
    # Return top k
    return recommendations[:k]
