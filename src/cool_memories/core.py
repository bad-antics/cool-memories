"""Cool Memories Analysis Engine"""
import json,random

class FragmentEngine:
    THEMES={
        "america":{"description":"America as hyperreal utopia","key_works":["America (1986)"],
                   "fragments":["America is the original version of modernity.",
                                "The desert is a sublime form of disappearance."]},
        "media":{"description":"Media as simulation machine","key_works":["The Gulf War Did Not Take Place"],
                 "fragments":["Information devours its own content.",
                              "The medium is not the message, it is the disappearance of the message."]},
        "technology":{"description":"Technology and the loss of the real","key_works":["The System of Objects"],
                      "fragments":["Technology creates a world of objects without subjects.",
                                   "We are screens for the absorption of information."]},
        "desire":{"description":"Desire in consumer society","key_works":["The Consumer Society"],
                  "fragments":["We consume signs, not things.",
                               "Objects are not consumed for their use value but for their sign value."]},
    }
    
    def get_theme(self,theme):
        return self.THEMES.get(theme,{})
    
    def generate_fragment(self,theme=None):
        if theme and theme in self.THEMES:
            return random.choice(self.THEMES[theme]["fragments"])
        all_frags=[f for t in self.THEMES.values() for f in t["fragments"]]
        return random.choice(all_frags)
    
    def analyze_fragment(self,text):
        word_count=len(text.split())
        themes_detected=[]
        for theme,data in self.THEMES.items():
            if any(kw in text.lower() for kw in theme.split("_")+[theme]):
                themes_detected.append(theme)
        return {"text":text,"word_count":word_count,"themes":themes_detected,
                "style":"aphoristic" if word_count<20 else "reflective" if word_count<50 else "essay"}
    
    def chronology(self):
        return [
            {"year":1929,"event":"Born in Reims, France"},
            {"year":1966,"event":"The System of Objects"},
            {"year":1981,"event":"Simulacra and Simulation"},
            {"year":1986,"event":"America"},
            {"year":1990,"event":"Cool Memories I"},
            {"year":1995,"event":"Cool Memories II"},
            {"year":2000,"event":"Cool Memories III"},
            {"year":2007,"event":"Died in Paris"},
        ]
