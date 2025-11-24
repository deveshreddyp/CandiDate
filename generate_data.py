import csv
import random
from faker import Faker

fake = Faker()

# Expanded Skills Database
SKILLS_DB = [
    "Python", "Java", "React", "Node.js", "AWS", "Docker", "Kubernetes", 
    "SQL", "NoSQL", "Machine Learning", "TensorFlow", "PyTorch", "Git", 
    "CI/CD", "Agile", "Scrum", "Linux", "C++", "C#", "Go", "Rust",
    "TypeScript", "GraphQL", "MongoDB", "PostgreSQL", "Redis", "Kafka",
    "Microservices", "REST API", "System Design", "DevOps", "Azure", "GCP"
]

ROLES = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Cloud Architect"]
DEGREES = ["B.Sc", "M.Sc", "B.Tech", "M.Tech", "PhD", "Bachelor of Engineering", "Master of Computer Applications"]

def generate_resume(skills):
    return f"""
    {fake.name()}
    {fake.email()}
    
    SUMMARY
    Highly motivated {random.choice(ROLES)} with expertise in {random.choice(skills)} and {random.choice(skills)}.
    Proven track record of delivering high-quality software solutions.

    TECHNICAL SKILLS
    {', '.join(skills)}

    PROFESSIONAL EXPERIENCE
    {fake.job()} at {fake.company()} ({fake.year()}-Present)
    - Led the development of {random.choice(skills)} based applications.
    - Optimized system performance by {random.randint(10, 50)}%.
    - Mentored junior developers in {random.choice(skills)} best practices.
    
    {fake.job()} at {fake.company()} ({fake.year()}-2020)
    - Developed robust APIs using {random.choice(skills)}.
    - Collaborated with cross-functional teams to deliver projects on time.

    EDUCATION
    {random.choice(DEGREES)} in Computer Science, {fake.city()} University
    """

def generate_jd(required_skills):
    return f"""
    Job Title: {random.choice(ROLES)}
    
    About the Role:
    We are seeking a skilled engineer to join our dynamic team. You will be responsible for designing and implementing scalable solutions.
    
    Key Requirements:
    - 3+ years of experience with {', '.join(required_skills)}.
    - Deep understanding of cloud infrastructure (AWS/Azure).
    - Strong problem-solving skills and ability to work in an Agile environment.
    - Excellent communication and teamwork abilities.
    """

def calculate_mock_score(resume_skills, jd_skills):
    # Stricter scoring logic
    match_count = len(set(resume_skills).intersection(set(jd_skills)))
    total_needed = len(jd_skills)
    if total_needed == 0: return 0
    
    base_score = (match_count / total_needed) * 100
    
    # Add "Seniority" bias (randomly)
    if random.random() > 0.8: base_score += 10 
    
    # Cap at 100, floor at 0
    return max(0, min(100, round(base_score + random.uniform(-2, 2))))

print("Generating 500 Advanced Synthetic Resumes...")

with open('synthetic_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['resume_text', 'jd_text', 'human_score'])
    
    for _ in range(500): # Increased to 500
        jd_skills = random.sample(SKILLS_DB, k=random.randint(4, 8))
        # Resume might have 2-10 skills, creating variety in match quality
        resume_skills = random.sample(SKILLS_DB, k=random.randint(2, 10))
        
        resume_text = generate_resume(resume_skills)
        jd_text = generate_jd(jd_skills)
        score = calculate_mock_score(resume_skills, jd_skills)
        
        writer.writerow([resume_text.strip(), jd_text.strip(), score])

print("Done! Created 'synthetic_dataset.csv' with 500 samples.")