import csv
import sys


def normalize_path(path):
    return path.replace("\\", "/")


def is_valid_rating(r):
    return 0 <= r <= 10


def is_tie(games):
    games[0][1] == games[-1][1]


def read_ratings(file_path):
    ratings = {}
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["title"]
            rating = int(row["rating"])
            if title in ratings:
                ratings[title].append(rating)
            else:
                ratings[title] = [rating]
    return ratings


def generate_report(ratings, top_n):
    averages = {}
    for title, scores in ratings.items():
        averages[title] = sum(scores) / len(scores)

    sorted_games = sorted(averages.items(), key=lambda x: x[1], reverse=True)

    for i in range(top_n):
        title, avg = sorted_games[i]
        print(f"{i+1}. {title} - Avg Rating: {avg:.2f}")

    if is_tie(sorted_games):
        print("All games have the same average rating.")


def main(path):
    file_path = normalize_path(path)
    ratings = read_ratings(file_path)
    generate_report(ratings, 10)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print(f"사용법: {sys.argv[0]} <입력 CSV 파일>")
