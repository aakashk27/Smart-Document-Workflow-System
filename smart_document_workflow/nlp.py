import spacy
from fastapi import HTTPException

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str) -> dict:
    try:
        doc = nlp(text)
        entity_dict = {}
        
        for i, ent in enumerate(doc.ents):
            entity_dict[str(i)] = [ent.label_, ent.text]

        return entity_dict
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in NLP processing for text '{text}': {str(e)}",
        )
