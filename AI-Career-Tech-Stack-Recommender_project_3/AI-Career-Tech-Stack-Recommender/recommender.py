import re
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


LEVEL_ORDER = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}


def clean_text(text: str) -> str:
    """Normalize text for safer matching."""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9+#.\s,-]", " ", text)
    text = text.replace(",", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_skills(text: str) -> List[str]:
    """Split comma-separated skills into normalized skill tokens."""
    if not isinstance(text, str):
        return []
    raw = [s.strip().lower() for s in text.split(",")]
    return [s for s in raw if s]


def difficulty_score(user_level: str, role_level: str) -> float:
    """
    Score difficulty alignment.
    Exact match gets 1.0.
    One-level gap gets 0.6.
    Two-level gap gets 0.25.
    """
    u = LEVEL_ORDER.get(str(user_level).lower(), 2)
    r = LEVEL_ORDER.get(str(role_level).lower(), 2)
    gap = abs(u - r)
    if gap == 0:
        return 1.0
    if gap == 1:
        return 0.6
    return 0.25


def keyword_overlap_score(user_text: str, role_text: str) -> float:
    """Simple explainable overlap score between user words and role words."""
    user_set = set(clean_text(user_text).split())
    role_set = set(clean_text(role_text).split())
    if not user_set or not role_set:
        return 0.0
    return len(user_set.intersection(role_set)) / max(len(user_set), 1)


class CareerRecommender:
    """
    Explainable Hybrid Career Recommender.

    Method:
    1. TF-IDF + Cosine Similarity for skill matching.
    2. Goal similarity for career direction.
    3. Difficulty alignment for user level.
    4. Interest overlap for extra personalization.
    """

    def __init__(self, dataset_path: str):
        self.df = pd.read_csv(dataset_path)
        required_columns = {
            "role", "required_skills", "career_goal",
            "difficulty", "tools", "roadmap"
        }
        missing = required_columns - set(self.df.columns)
        if missing:
            raise ValueError(f"Dataset is missing columns: {missing}")

        self.df = self.df.fillna("")
        self.df["skill_text"] = self.df["required_skills"].apply(clean_text)
        self.df["goal_text"] = self.df["career_goal"].apply(clean_text)

        self.skill_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.skill_matrix = self.skill_vectorizer.fit_transform(self.df["skill_text"])

        self.goal_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.goal_matrix = self.goal_vectorizer.fit_transform(self.df["goal_text"])

    def recommend(
        self,
        skills: str,
        career_goal: str = "",
        level: str = "intermediate",
        interests: str = "",
        top_n: int = 3,
        weights: Dict[str, float] = None
    ) -> pd.DataFrame:
        if weights is None:
            weights = {
                "skill": 0.65,
                "goal": 0.20,
                "difficulty": 0.10,
                "interest": 0.05
            }

        skills_clean = clean_text(skills)
        goal_clean = clean_text(career_goal)
        interests_clean = clean_text(interests)

        if len(skills_clean.split()) < 1:
            raise ValueError("Please enter at least one skill. For better results, enter 3 or more skills.")

        user_skill_vec = self.skill_vectorizer.transform([skills_clean])
        skill_scores = cosine_similarity(user_skill_vec, self.skill_matrix).flatten()

        if goal_clean:
            user_goal_vec = self.goal_vectorizer.transform([goal_clean])
            goal_scores = cosine_similarity(user_goal_vec, self.goal_matrix).flatten()
        else:
            goal_scores = np.zeros(len(self.df))

        difficulty_scores = np.array([
            difficulty_score(level, role_level)
            for role_level in self.df["difficulty"]
        ])

        if interests_clean:
            interest_scores = np.array([
                keyword_overlap_score(interests_clean, row["required_skills"] + " " + row["career_goal"])
                for _, row in self.df.iterrows()
            ])
        else:
            interest_scores = np.zeros(len(self.df))

        final_scores = (
            weights["skill"] * skill_scores +
            weights["goal"] * goal_scores +
            weights["difficulty"] * difficulty_scores +
            weights["interest"] * interest_scores
        )

        results = self.df.copy()
        results["skill_similarity"] = skill_scores
        results["goal_similarity"] = goal_scores
        results["difficulty_alignment"] = difficulty_scores
        results["interest_overlap"] = interest_scores
        results["final_score"] = final_scores
        results["match_percentage"] = (final_scores * 100).round(2)

        user_skill_list = split_skills(skills)

        explanations = []
        matched_skills_list = []
        missing_skills_list = []

        for _, row in results.iterrows():
            role_skills = split_skills(row["required_skills"])
            matched = [s for s in role_skills if any(s in us or us in s for us in user_skill_list)]
            missing = [s for s in role_skills if s not in matched][:5]

            matched_skills_list.append(", ".join(matched) if matched else "General profile alignment")
            missing_skills_list.append(", ".join(missing) if missing else "No major gap found")

            explanation = (
                f"Recommended because your profile aligns with {row['role']} skills. "
                f"Skill similarity: {row.get('skill_similarity', 0):.2f}, "
                f"goal similarity: {row.get('goal_similarity', 0):.2f}, "
                f"difficulty alignment: {row.get('difficulty_alignment', 0):.2f}."
            )
            explanations.append(explanation)

        results["matched_skills"] = matched_skills_list
        results["missing_skills"] = missing_skills_list
        results["explanation"] = explanations

        results = results.sort_values("final_score", ascending=False).head(top_n)
        return results[
            [
                "role", "match_percentage", "difficulty", "tools",
                "matched_skills", "missing_skills", "roadmap",
                "skill_similarity", "goal_similarity", "difficulty_alignment",
                "interest_overlap", "final_score", "explanation"
            ]
        ].reset_index(drop=True)


if __name__ == "__main__":
    recommender = CareerRecommender("career_dataset.csv")
    skills = input("Enter your skills separated by commas: ")
    goal = input("Enter your career goal: ")
    level = input("Enter your level (beginner/intermediate/advanced): ")
    results = recommender.recommend(skills, goal, level, top_n=3)
    print("\nTop Recommendations\n")
    for i, row in results.iterrows():
        print(f"{i+1}. {row['role']} — {row['match_percentage']}% match")
        print(f"   Matched Skills: {row['matched_skills']}")
        print(f"   Missing Skills: {row['missing_skills']}")
        print(f"   Tools: {row['tools']}")
        print(f"   Roadmap: {row['roadmap']}\n")
