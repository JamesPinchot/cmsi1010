import unittest
import math
import io
from contextlib import redirect_stdout


# test cases for rectangle, circle, song, and playlist
class TestClassesCardio(unittest.TestCase):
    def test_rectangle(self):
        rect = Rectangle(3, 4)
        self.assertEqual(rect.area(), 12)
        self.assertEqual(rect.perimeter(), 14)
        self.assertEqual(str(rect), "Rectangle(3 x 4)")

    def test_circle(self):
        circle = Circle(5)
        self.assertAlmostEqual(circle.area(), 25*math.pi, places=5)
        self.assertAlmostEqual(circle.circumference(), 10*math.pi, places=5)
        self.assertEqual(str(circle), "Circle(radius=5)")

    def test_song(self):
        song = Song("Night Shift", "Lucy Dacus", 391)
        self.assertEqual(str(song), "Night Shift by Lucy Dacus (391s)")
        with io.StringIO() as captured_output:
            with redirect_stdout(captured_output):
                song.play()
            self.assertEqual(
                captured_output.getvalue(),
                "Playing Night Shift by Lucy Dacus (391s)\n")

    def test_playlist(self):
        playlist = Playlist()
        song1 = Song("Night Shift", "Lucy Dacus", 391)
        song2 = Song("I Was Neon", "Julia Jacklin", 243)
        song3 = Song("Forgiveness", "Alice Glass", 191)
        playlist.add_song(song1)
        playlist.add_song(song2)
        playlist.add_song(song3)
        self.assertEqual(
            str(playlist),
            "Night Shift by Lucy Dacus (391s)|"
            "I Was Neon by Julia Jacklin (243s)|"
            "Forgiveness by Alice Glass (191s)")
        with io.StringIO() as captured_output:
            with redirect_stdout(captured_output):
                playlist.play_all()
            self.assertEqual(
                captured_output.getvalue(),
                "Playing Night Shift by Lucy Dacus (391s)\n"
                "Playing I Was Neon by Julia Jacklin (243s)\n"
                "Playing Forgiveness by Alice Glass (191s)\n")


# rectangle class with area and perimeter
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle({self.width} x {self.height})"


# circle class with area and circumference
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def circumference(self):
        return 2 * math.pi * self.radius

    def __str__(self):
        return f"Circle(radius={self.radius})"


# song class with title, artist, and duration
class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.duration}s)"

    def play(self):
        print(f"Playing {self}")


# playlist class holds multiple songs
class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __str__(self):
        return "|".join(str(song) for song in self.songs)

    def play_all(self):
        for song in self.songs:
            song.play()



if __name__ == '__main__':
    unittest.main()
