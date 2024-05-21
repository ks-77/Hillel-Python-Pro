import random
import numpy as np
import nltk
from faker import Faker
from nltk.corpus import words


def generate_random_unique_words(quantity):
    if quantity > 10000:
        raise ValueError('Quantity must be less than 10000')
    nltk.download('words')
    unique_words = list({word.lower() for word in words.words()})
    for word in unique_words[:quantity]:
        yield word
