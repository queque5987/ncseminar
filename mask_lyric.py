import get_lyric
import os
import random
import time
groups = get_lyric.groups

if __name__ == "__main__":
    random.seed(time.ctime())

    for group in groups:
        # print(group)
        directory = f"output\\{group}"
        for dir in os.listdir(directory):
            full_dir = os.path.join(directory, dir)
            with open(full_dir, "r", encoding="utf-8") as f:
                lyric = [line.strip() for line in f.readlines()]
                r = random.randint(1, len(lyric)-2)
                mask = lyric[r]
                masked_lyric = lyric[:r-1] + ["<mask>"] + lyric[r:]
                