from typing import Dict, List

class PipelineAgent:
    def __init__(self):
        self.context_keywords: Dict[str, List[str]] = {'a': ['b']}

    def generate_concept(self, title, summary=""):
        text = "b"
        scores: Dict[str, int] = {k: 0 for k in self.context_keywords}
        for category, terms in self.context_keywords.items():
            for term in terms:
                if term in text:
                    scores[category] += 1
        return scores

print(PipelineAgent().generate_concept("b"))
