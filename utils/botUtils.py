import os


def prepareAtStart():
    if not os.path.exists("temp"):
        os.makedirs("temp")
