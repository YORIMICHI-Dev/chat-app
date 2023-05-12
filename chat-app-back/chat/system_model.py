from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, root_validator


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    undefined = "undefined"

    @classmethod
    def get_value(cls, name: str) -> str:
        return cls[name].value


class LanguageEnum(str, Enum):
    en = "English"
    ja = "Japanese"

    @classmethod
    def get_value(cls, name: str) -> str:
        return cls[name].value


class CharacterEnum(str, Enum):
    mysteriousness = "Enigmatic and intriguing, drawing people in"
    elegance = "Possesses grace and sophistication in her demeanor"
    shyness = "Bashful and hesitant to assert herself"
    good_taste = "Has a strong aesthetic sense and pays attention to fashion and interior design"
    passion = "Emotionally expressive and dedicated to her pursuits"
    maternal = "Enjoys taking care of others and nurturing"
    calm_collected = "Remains composed and level-headed, no matter how tense the situation"
    sensitive = "Highly affected by the emotions and feelings of those around her"

    @classmethod
    def get_value(cls, name: str) -> str:
        return cls[name].value


class SystemModel(BaseModel):
    gender: GenderEnum = GenderEnum.female
    language: LanguageEnum = LanguageEnum.ja
    character: CharacterEnum = CharacterEnum.mysteriousness
    other_setting: Optional[str] = None
    system: Optional[Dict[str, str]] = None

    @classmethod
    def system_factory(cls, gender_str: str, language_str: str, character_str: str, other_setting: str):
        gender = GenderEnum.get_value(gender_str)
        language = LanguageEnum.get_value(language_str)
        character = CharacterEnum.get_value(character_str)
        return cls(
            gender=gender, 
            language=language, 
            character=character, 
            other_setting=other_setting,
        )

    @root_validator()
    def make_system(cls, values):
        gender = values.get("gender", GenderEnum.female)
        language = values.get("language", LanguageEnum.ja)
        character = values.get("character", CharacterEnum.mysteriousness)

        your_gender = f"You are {gender.value}."
        your_language = f"You talk with {language.value}."
        your_character = f"Your are that {character.value}."

        system_contents = [your_gender, your_language, your_character]
        if values.get("other_settings") is not None:
            other_settings = values.get("other_settings")
            your_other_settings = f"Finally, you are {[setting for setting in other_settings]}"
            system_contents.append(your_other_settings)

        values["system"] = {"role": "system", "content": " ".join(system_contents)}

        return values
