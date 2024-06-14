import spacy
from textblob import TextBlob
import csv

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install the 'en_core_web_sm' model by running:")
    print("python -m spacy download en_core_web_sm")
    exit()

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Function to extract key phrases using spaCy
def extract_key_phrases(text):
    doc = nlp(text)
    key_phrases = []
    for chunk in doc.noun_chunks:
        key_phrases.append(chunk.text)
    return key_phrases

# Read interview responses from file
with open('interview_responses.txt', 'r') as file:
    responses = file.readlines()

# Open a CSV file to write the output
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Response', 'Sentiment', 'Key Phrases', 'Quality Assessment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Process each response
    for idx, response in enumerate(responses):
        response = response.strip()
        
        # Analyze sentiment
        sentiment = analyze_sentiment(response)
        
        # Extract key phrases
        key_phrases = extract_key_phrases(response)
        
        # Determine quality assessment
        if sentiment == 'positive' and any(phrase in response.lower() for phrase in ['enjoyed', 'supportive', 'great results']):
            quality_assessment = "Positive response with relevant key phrases."
        elif sentiment == 'negative' and any(phrase in response.lower() for phrase in ['significant challenges', 'difficult', 'frustrating']):
            quality_assessment = "Negative response highlighting challenges."
        else:
            quality_assessment = "Neutral or mixed sentiment."
        
        # Write to CSV
        writer.writerow({
            'Response': response,
            'Sentiment': sentiment,
            'Key Phrases': ', '.join(key_phrases),
            'Quality Assessment': quality_assessment
        })

print("Output has been written to 'output.csv'")
