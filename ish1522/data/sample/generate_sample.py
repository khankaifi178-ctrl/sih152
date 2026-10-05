import json
import random
import os
from datetime import datetime, timezone, timedelta

def generate_data():
    os.makedirs('data/sample', exist_ok=True)
    out_file = 'data/sample/sample_dataset.json'
    
    print("Generating synthetic dataset with 125,000+ posts and 38,000+ users...")
    
    platforms = ['X', 'Telegram', 'Instagram', 'Facebook', 'Reddit', 'YouTube']
    topics = [
        {"id": "t1", "label": "AI Regulation", "growth_pct": 340, "first_seen": "2026-10-05T12:00:00Z"},
        {"id": "t2", "label": "New Product", "growth_pct": 280, "first_seen": "2026-10-05T10:30:00Z"},
        {"id": "t3", "label": "Data Privacy", "growth_pct": 190, "first_seen": "2026-10-05T08:15:00Z"},
        {"id": "t4", "label": "Cyber Defense", "growth_pct": 120, "first_seen": "2026-10-04T14:00:00Z"},
        {"id": "t5", "label": "5G Infrastructure", "growth_pct": 85, "first_seen": "2026-10-04T09:00:00Z"}
    ]
    
    users = []
    seeded_influencers = [
        {"id": "u_user_a", "platform": "X", "hashed_handle": "@user_a_tech", "followers": 450000, "influence_score": 94, "community": "Community A"},
        {"id": "u_user_b", "platform": "Telegram", "hashed_handle": "@user_b_intel", "followers": 280000, "influence_score": 89, "community": "Community B"},
        {"id": "u_user_c", "platform": "X", "hashed_handle": "@user_c_analyst", "followers": 195000, "influence_score": 84, "community": "Community C"}
    ]
    
    locations = ["India", "USA", "UK", "Germany", "Canada", "Singapore", "Australia"]
    location_weights = [0.65, 0.15, 0.08, 0.04, 0.03, 0.03, 0.02]
    
    interests = ["technology", "government", "education", "media", "finance", "defense"]
    languages = ["English", "Hindi", "Hinglish"]
    
    for inf in seeded_influencers:
        users.append({
            "id": inf["id"],
            "platform": inf["platform"],
            "hashed_handle": inf["hashed_handle"],
            "bio_text": "Senior Tech Analyst & Strategic Researcher. Focus on AI & Data Governance.",
            "followers": inf["followers"],
            "activity_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            "language": "English",
            "location": "India",
            "interest": "technology",
            "age_bracket": "25-34",
            "influence_score": inf["influence_score"],
            "community": inf["community"]
        })
        
    for i in range(4, 38421):
        u_id = f"u_{i}"
        plat = random.choice(platforms)
        age = random.choices(["18-24", "25-34", "35-44", "45-54", "55+"], weights=[0.42, 0.31, 0.15, 0.08, 0.04])[0]
        loc = random.choices(locations, weights=location_weights)[0]
        lang = random.choices(languages, weights=[0.50, 0.30, 0.20])[0]
        interest = random.choice(interests)
        
        users.append({
            "id": u_id,
            "platform": plat,
            "hashed_handle": f"@user_{i}_{plat.lower()}",
            "bio_text": f"Social media user interested in {interest} and news updates.",
            "followers": random.randint(50, 15000),
            "activity_hours": random.sample(range(24), 8),
            "language": lang,
            "location": loc,
            "interest": interest,
            "age_bracket": age,
            "influence_score": random.randint(10, 75),
            "community": random.choice(["Community A", "Community B", "Community C", "Community D"])
        })
        
    posts = []
    base_time = datetime(2026, 10, 5, 12, 0, 0, tzinfo=timezone.utc)
    
    sample_texts = [
        ("AI Regulation frameworks announced for national safety.", "positive", "excitement", 0.05, "t1"),
        ("New Product security baseline standards released today.", "positive", "supportive", 0.02, "t2"),
        ("Data Privacy policies are being updated across platforms.", "neutral", "supportive", 0.08, "t3"),
        ("Sarcasm sample: Wow, another policy change, absolutely groundbreaking... not.", "negative", "sarcasm", 0.88, "t1"),
        ("Hinglish sample: Yeh AI Regulation bahot zaroori tha, cybersecurity strong hogi.", "positive", "excitement", 0.04, "t1"),
        ("Anxiety regarding cyber vulnerability in infrastructure.", "negative", "anxiety", 0.12, "t4"),
        ("Anger regarding data breach concerns on third party apps.", "negative", "anger", 0.15, "t3")
    ]

    total_posts = 124560
    print(f"Generating {total_posts} realistic posts...")
    
    for i in range(total_posts):
        text_tuple = random.choice(sample_texts)
        u = random.choice(users)
        
        minutes_offset = random.randint(0, 48 * 60)
        post_time = base_time - timedelta(minutes=minutes_offset)
        
        posts.append({
            "id": f"p_{i}",
            "platform": u["platform"],
            "platform_post_id": f"post_ext_{i}",
            "author_id": u["id"],
            "author_handle": u["hashed_handle"],
            "text": text_tuple[0],
            "lang": u["language"],
            "created_at": post_time.isoformat(),
            "parent_id": f"p_{i-1}" if (i % 7 == 0 and i > 0) else None,
            "likes": random.randint(0, 450),
            "shares": random.randint(0, 120),
            "replies": random.randint(0, 45),
            "polarity": text_tuple[1],
            "emotion": text_tuple[2],
            "sarcasm_prob": text_tuple[3],
            "topic_id": text_tuple[4]
        })
        
    dataset = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_posts": len(posts),
            "active_users": len(users),
            "trending_topics_count": 17,
            "sentiment_summary": {"positive": 0.58, "negative": 0.27, "neutral": 0.15}
        },
        "topics": topics,
        "users": users[:1000],
        "posts_sample": posts[:2000],
        "total_posts_count": 124560,
        "total_users_count": 38420
    }
    
    with open(out_file, 'w') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Dataset successfully created at {out_file}")

if __name__ == '__main__':
    generate_data()
