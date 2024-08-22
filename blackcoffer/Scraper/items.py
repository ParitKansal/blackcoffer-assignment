# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

import scrapy

class WebItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()  # Added to store main text content
    url_id= scrapy.Field()
    positive_score = scrapy.Field()  # For sentiment analysis score
    negative_score = scrapy.Field()  # For sentiment analysis score
    polarity_score = scrapy.Field()  # Sentiment polarity score
    subjectivity_score = scrapy.Field()  # Sentiment subjectivity score
    avg_number_of_words_per_sentence = scrapy.Field()
    personal_pronouns = scrapy.Field()  # Count of personal pronouns
    complex_word_count = scrapy.Field()  # Count of complex words
    percentage_of_complex_words = scrapy.Field()  # Percentage of complex words
    word_count = scrapy.Field()  # Total number of words
    avg_word_length = scrapy.Field()  # Average length of words
    syllable_per_word = scrapy.Field()
    fog_index = scrapy.Field()  # Fog index score
    avg_sentence_length = scrapy.Field() 
    