# AI Career Path & Tech Stack Recommender

## Project Overview

This project is an explainable AI recommendation system that recommends suitable career paths and technology stacks based on a user's skills, career goal, experience level, and interests.

It is based on content-based filtering using TF-IDF vectorization and cosine similarity. To make the system more useful and portfolio-ready, it also includes hybrid scoring, skill-gap analysis, match percentage, and personalized learning roadmaps.

## Problem Statement

Students and beginners often know some skills, but they are unsure which career path fits them best. Random suggestions are not useful because they do not explain why a role is recommended or what skills are missing.

## Solution

The system compares the user's profile with multiple career role profiles and recommends the top matching career paths.

Example:

Input:
- Skills: Python, SQL, Machine Learning
- Career Goal: Artificial Intelligence
- Level: Intermediate

Output:
- Data Scientist
- Machine Learning Engineer
- AI Engineer

Each recommendation includes:
- Match percentage
- Matched skills
- Missing skills
- Recommended tools
- Learning roadmap

## Methodology

The system follows this pipeline:

1. **Input/Ingestion**  
   The user enters skills, goal, level, and interests.

2. **Vector Mapping**  
   Text data is converted into numerical vectors using TF-IDF.

3. **Similarity Calculation**  
   Cosine similarity compares the user profile with each career role.

4. **Hybrid Scoring**  
   Final score is calculated using:

   `Final Score = 65% Skill Similarity + 20% Goal Similarity + 10% Difficulty Alignment + 5% Interest Match`

5. **Ranking and Filtering**  
   Roles are sorted by score and the top recommendations are displayed.

6. **Explanation Layer**  
   The system displays why each role matched, missing skills, and a roadmap.

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity

## Project Structure

```text
AI-Career-Tech-Stack-Recommender/
│
├── app.py
├── recommender.py
├── career_dataset.csv
├── requirements.txt
└── README.md
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit app

```bash
streamlit run app.py
```

### 3. Open the app in your browser

Streamlit will show a local URL such as:

```text
http://localhost:8501
```

## Sample Input

```text
Skills: Python, SQL, Machine Learning
Career Goal: Artificial Intelligence
Level: Intermediate
Interests: AI projects, real-world applications
```

## Sample Output

```text
1. Data Scientist — 88% Match
2. Machine Learning Engineer — 84% Match
3. AI Engineer — 82% Match
```

## What Makes This Project Different

Most beginner recommendation systems only display a recommended item. This project adds:

- Explainable recommendations
- Hybrid scoring
- Skill-gap analysis
- Personalized roadmap
- Adjustable score weights
- Streamlit user interface

## Future Improvements

- Add login system
- Add larger dataset
- Add course recommendation links
- Add resume skill extraction
- Add LinkedIn profile analysis
- Deploy using Streamlit Cloud

## Author

Sanjula Supunthaka
