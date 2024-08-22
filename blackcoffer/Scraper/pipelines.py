import os
import re
import string
import scrapy
from itemadapter import ItemAdapter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data files (only required once)
nltk.download('punkt')
nltk.download('stopwords')

class ScraperPipeline:
    def __init__(self):
        self.stop_words = self.load_words('StopWords')
        self.positive_words = self.load_words('MasterDictionary/positive-words.txt')
        self.negative_words = self.load_words('MasterDictionary/negative-words.txt')
        self.pronouns = set([
            'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'mine', 'yours', 'hers', 'ours', 'theirs',
            'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves'
        ])
        self.pronoun_pattern = re.compile(r'\b(?:(?!US\b)(?:' + '|'.join(self.pronouns) + r'))\b', re.IGNORECASE)
        self.url_pattern = re.compile(r'http\S+|www\S+')
        self.emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            "]+", flags=re.UNICODE
        )
        self.number_pattern = re.compile(r'\d+')
        self.nltk_stop_words = set(stopwords.words('english'))

    def load_words(self, path):
        words = set()
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', path))
        if os.path.isdir(full_path):
            for filename in os.listdir(full_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(full_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            words.update(word.lower() for word in file.read().splitlines())
                    except UnicodeDecodeError:
                        with open(file_path, 'r', encoding='latin1') as file:
                            words.update(word.lower() for word in file.read().splitlines())
        else:
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    words.update(word.lower() for word in file.read().splitlines())
            except UnicodeDecodeError:
                with open(full_path, 'r', encoding='latin1') as file:
                    words.update(word.lower() for word in file.read().splitlines())
        return words

    def preprocess_string(self, value):
        if isinstance(value, str):
            value = re.sub(r'[\u2028\u2029\n\r]+', ' ', value)  # Remove unusual line terminators
            value = re.sub(r'\s+', ' ', value).strip()  # Replace multiple spaces with single space and strip
        return value

    def remove_stop_words(self, text):
        if text:
            words = text.split()
            filtered_words = [word for word in words if word.lower() not in self.stop_words]
            return ' '.join(filtered_words), len(filtered_words)
        return '', 0

    def tokenize_text(self, text):
        return word_tokenize(text) if text else []

    def calculate_score(self, tokens, word_set):
        return sum(1 for token in tokens if token.lower() in word_set)

    def calculate_polarity_score(self, positive_score, negative_score):
        denominator = (positive_score + negative_score) + 0.000001
        return max(-1, min(1, (positive_score - negative_score) / denominator))

    def calculate_subjectivity_score(self, positive_score, negative_score, total_words):
        denominator = total_words + 0.000001
        return max(0, min(1, (positive_score + abs(negative_score)) / denominator))

    def remove_headings(self, text):
        return re.sub(r'\b[A-Z][a-zA-Z0-9]*\b\s*:', '', text).strip()

    def calculate_average_words_per_sentence(self, text):
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
        if not sentences:
            return 0
        total_words = sum(len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences)
        return total_words / len(sentences)

    def count_personal_pronouns(self, text):
        return len(self.pronoun_pattern.findall(text)) if text else 0

    def clean_text(self, text):
        text = self.url_pattern.sub('', text)
        text = self.emoji_pattern.sub('', text)
        text = self.number_pattern.sub('', text)
        text = text.lower()
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def count_cleaned_words(self, text):
        cleaned_text = self.clean_text(text)
        words = word_tokenize(cleaned_text)
        return [word for word in words if word not in self.nltk_stop_words]
    
    def syllable_count_per_word(self, word):
        word = word.lower()
        if word.endswith(('es', 'ed')):
            word = word[:-2]
        vowel_count = sum(1 for char in word if char in 'aeiou')
        return vowel_count
    
    def average_word_length(self, words):
        if not words:
            return 0
        total_characters = sum(len(word) for word in words)
        return total_characters / len(words)
    
    def syllable_count(self, words):
        return [self.syllable_count_per_word(word) for word in words]
    
    def avg_syllable_per_word(self, words):
        if not words:
            return 0
        total_syllables = sum(self.syllable_count_per_word(word) for word in words)
        return total_syllables / len(words)
    
    def complex_word_count(self, words):
        return sum(1 for count in self.syllable_count(words) if count > 2)
    
    def percentage_of_complex_words(self, words):
        total_words = len(words)
        if total_words == 0:
            return 0
        return (self.complex_word_count(words) / total_words) * 100

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'content' in adapter.field_names():
            # Preprocessing and basic calculations
            value = adapter.get('content')
            preprocessed_value = self.preprocess_string(value)
            adapter['content'] = preprocessed_value

            # Derived variables
            filtered_content, total_words = self.remove_stop_words(preprocessed_value)
            tokens = self.tokenize_text(preprocessed_value)
            
            positive_score = self.calculate_score(tokens, self.positive_words)
            negative_score = self.calculate_score(tokens, self.negative_words) * -1
            
            adapter['positive_score'] = positive_score
            adapter['negative_score'] = negative_score
            adapter['polarity_score'] = self.calculate_polarity_score(positive_score, negative_score)
            adapter['subjectivity_score'] = self.calculate_subjectivity_score(positive_score, negative_score, total_words)

            # Average words per sentence
            cleaned_value = self.remove_headings(preprocessed_value)
            avg_words_per_sentence = self.calculate_average_words_per_sentence(cleaned_value)
            adapter['avg_number_of_words_per_sentence'] = avg_words_per_sentence

            # Personal pronouns
            adapter['personal_pronouns'] = self.count_personal_pronouns(preprocessed_value)
            
            # Word statistics
            words = self.count_cleaned_words(preprocessed_value)
            
            adapter['word_count'] = len(words)
            adapter['avg_word_length'] = self.average_word_length(words)
            adapter['syllable_per_word'] = self.avg_syllable_per_word(words)
            adapter['complex_word_count'] = self.complex_word_count(words)
            adapter['percentage_of_complex_words'] = self.percentage_of_complex_words(words)
            
            # Fog index
            adapter['fog_index'] = 0.4 * (avg_words_per_sentence + adapter['percentage_of_complex_words'])
            adapter['avg_sentence_length'] = avg_words_per_sentence

        return item
