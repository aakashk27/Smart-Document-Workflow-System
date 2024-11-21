import spacy
from fastapi import HTTPException

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    """
    Extract structured data (entities) from text using spaCy.
    """
    try:
        doc = nlp(text)
        entities = {ent.label_: ent.text for ent in doc.ents}
        return entities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in NLP processing: {str(e)}")
