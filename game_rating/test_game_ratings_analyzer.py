from game_ratings_analyzer import normalize_path, is_valid_rating, read_ratings, generate_report, is_tie
from tempfile import NamedTemporaryFile


def test_bug1_path_normalization():
    fileName = "/home/user/\\data\\game_ratings.csv"
    assert "/home/user/data/game_ratings.csv" == normalize_path(fileName)



def test_bug2_rating_validity():
    assert is_valid_rating("9")



def test_bug3_file_not_exist():
    read_ratings("not_existing_file.csv")



def test_bug4_nan_rating():
    csv_data = """title,genre,rating,comments
Fake Game,RPG,not_a_number"""
    tmp = NamedTemporaryFile()
    with open(tmp.name, "w") as f:
        f.write(csv_data)
    read_ratings(tmp.name)



def test_bug5_empty_title():
    csv_data = """title,genre,rating,comments,RPG,8"""
    tmp = NamedTemporaryFile()
    with open(tmp.name, "w") as f:
        f.write(csv_data)
    # No empty dictionary keys should be allowed.
    assert len(read_ratings(tmp.name)) == 0



def test_bug6_div_zero():
    ratings = {"Empty Game": []}
    # Div by zero should be avoided.
    generate_report(ratings, 1)



def test_bug7_less_ratings():
    ratings = {"Game A": [10], "Game B": [9]}

    # No IndexError should be raised.
    generate_report(ratings, 5)



def test_bug8_wrong_tie_detection():
    ratings = [("Game A", 9), ("Game B", 8), ("Game C", 9)]

    assert is_tie(ratings) == False



def test_bug9_top_n_too_high():
    ratings = {"Game A": [10]}

    # No IndexError should be raised
    generate_report(ratings, 10)
