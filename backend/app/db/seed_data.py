"""
Database Seeding Script
Populates default questionnaires (PHQ-9, GAD-7, PSS, WHO-5), curated resources,
verified crisis helplines, sample professional listings, and default admin account.
"""
import logging
import datetime
from app.db.mongodb import get_database
from app.core.security import hash_password

logger = logging.getLogger("mindcare.seed")

async def seed_initial_data():
    db = get_database()
    logger.info("Checking initial database seed requirements...")

    # 1. Seed Assessments
    existing_assessments = await db.assessments.count_documents({})
    if existing_assessments == 0:
        logger.info("Seeding standard screening questionnaires (PHQ-9, GAD-7, PSS, WHO-5)...")

        phq_options = [
            {"label": "Not at all", "score": 0},
            {"label": "Several days", "score": 1},
            {"label": "More than half the days", "score": 2},
            {"label": "Nearly every day", "score": 3}
        ]

        gad_options = [
            {"label": "Not at all", "score": 0},
            {"label": "Several days", "score": 1},
            {"label": "More than half the days", "score": 2},
            {"label": "Nearly every day", "score": 3}
        ]

        pss_options = [
            {"label": "Never", "score": 0},
            {"label": "Almost Never", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Fairly Often", "score": 3},
            {"label": "Very Often", "score": 4}
        ]

        who_options = [
            {"label": "All of the time", "score": 5},
            {"label": "Most of the time", "score": 4},
            {"label": "More than half of the time", "score": 3},
            {"label": "Less than half of the time", "score": 2},
            {"label": "Some of the time", "score": 1},
            {"label": "At no time", "score": 0}
        ]

        assessments = [
            {
                "_id": "phq-9",
                "name": "PHQ-9",
                "description": "Patient Health Questionnaire for depressive symptom screening over the past 2 weeks.",
                "version": "1.0",
                "type": "screening",
                "active": True,
                "questions": [
                    {"questionId": 1, "text": "Little interest or pleasure in doing things", "order": 1, "options": phq_options},
                    {"questionId": 2, "text": "Feeling down, depressed, or hopeless", "order": 2, "options": phq_options},
                    {"questionId": 3, "text": "Trouble falling or staying asleep, or sleeping too much", "order": 3, "options": phq_options},
                    {"questionId": 4, "text": "Feeling tired or having little energy", "order": 4, "options": phq_options},
                    {"questionId": 5, "text": "Poor appetite or overeating", "order": 5, "options": phq_options},
                    {"questionId": 6, "text": "Feeling bad about yourself — or that you are a failure or have let yourself or your family down", "order": 6, "options": phq_options},
                    {"questionId": 7, "text": "Trouble concentrating on things, such as reading the newspaper or watching television", "order": 7, "options": phq_options},
                    {"questionId": 8, "text": "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual", "order": 8, "options": phq_options},
                    {"questionId": 9, "text": "Thoughts that you would be better off dead or of hurting yourself in some way", "order": 9, "options": phq_options}
                ]
            },
            {
                "_id": "gad-7",
                "name": "GAD-7",
                "description": "Generalized Anxiety Disorder 7-item scale for anxiety symptom screening over the past 2 weeks.",
                "version": "1.0",
                "type": "screening",
                "active": True,
                "questions": [
                    {"questionId": 1, "text": "Feeling nervous, anxious, or on edge", "order": 1, "options": gad_options},
                    {"questionId": 2, "text": "Not being able to stop or control worrying", "order": 2, "options": gad_options},
                    {"questionId": 3, "text": "Worrying too much about different things", "order": 3, "options": gad_options},
                    {"questionId": 4, "text": "Trouble relaxing", "order": 4, "options": gad_options},
                    {"questionId": 5, "text": "Being so restless that it is hard to sit still", "order": 5, "options": gad_options},
                    {"questionId": 6, "text": "Becoming easily annoyed or irritable", "order": 6, "options": gad_options},
                    {"questionId": 7, "text": "Feeling afraid, as if something awful might happen", "order": 7, "options": gad_options}
                ]
            },
            {
                "_id": "pss-10",
                "name": "PSS-10",
                "description": "Perceived Stress Scale measuring the degree to which situations in life are appraised as stressful.",
                "version": "1.0",
                "type": "screening",
                "active": True,
                "questions": [
                    {"questionId": 1, "text": "In the last month, how often have you been upset because of something that happened unexpectedly?", "order": 1, "options": pss_options},
                    {"questionId": 2, "text": "In the last month, how often have you felt that you were unable to control the important things in your life?", "order": 2, "options": pss_options},
                    {"questionId": 3, "text": "In the last month, how often have you felt nervous and stressed?", "order": 3, "options": pss_options},
                    {"questionId": 4, "text": "In the last month, how often have you felt confident about your ability to handle your personal problems?", "order": 4, "options": pss_options},
                    {"questionId": 5, "text": "In the last month, how often have you felt that things were going your way?", "order": 5, "options": pss_options},
                    {"questionId": 6, "text": "In the last month, how often have you found that you could not cope with all the things that you had to do?", "order": 6, "options": pss_options},
                    {"questionId": 7, "text": "In the last month, how often have you been able to control irritations in your life?", "order": 7, "options": pss_options},
                    {"questionId": 8, "text": "In the last month, how often have you felt that you were on top of things?", "order": 8, "options": pss_options},
                    {"questionId": 9, "text": "In the last month, how often have you been angered because of things that were outside of your control?", "order": 9, "options": pss_options},
                    {"questionId": 10, "text": "In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?", "order": 10, "options": pss_options}
                ]
            },
            {
                "_id": "who-5",
                "name": "WHO-5",
                "description": "WHO-5 Well-Being Index evaluating subjective emotional well-being over the past 2 weeks.",
                "version": "1.0",
                "type": "screening",
                "active": True,
                "questions": [
                    {"questionId": 1, "text": "I have felt cheerful and in good spirits", "order": 1, "options": who_options},
                    {"questionId": 2, "text": "I have felt calm and relaxed", "order": 2, "options": who_options},
                    {"questionId": 3, "text": "I have felt active and vigorous", "order": 3, "options": who_options},
                    {"questionId": 4, "text": "I woke up feeling fresh and rested", "order": 4, "options": who_options},
                    {"questionId": 5, "text": "My daily life has been filled with things that interest me", "order": 5, "options": who_options}
                ]
            }
        ]

        for a in assessments:
            await db.assessments.update_one({"_id": a["_id"]}, {"$set": a}, upsert=True)

    # 2. Seed Crisis Resources
    existing_crisis = await db.crisis_resources.count_documents({})
    if existing_crisis == 0:
        logger.info("Seeding verified crisis helplines...")
        crisis_data = [
            {
                "_id": "crisis-1",
                "name": "988 Suicide & Crisis Lifeline",
                "description": "Free, confidential 24/7 support for anyone in suicidal crisis or emotional distress.",
                "phone": "988",
                "website": "https://988lifeline.org",
                "country": "United States / Canada",
                "availability": "24/7",
                "source": "Official SAMHSA / Lifeline",
                "active": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "_id": "crisis-2",
                "name": "Crisis Text Line",
                "description": "Free 24/7 text line connecting you with a trained crisis counselor.",
                "phone": "Text HOME to 741741",
                "website": "https://www.crisistextline.org",
                "country": "Global",
                "availability": "24/7",
                "source": "Crisis Text Line Organization",
                "active": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "_id": "crisis-3",
                "name": "International Association for Suicide Prevention (IASP)",
                "description": "Global directory of emergency crisis centers and mental health support helplines worldwide.",
                "phone": "Visit website for country directory",
                "website": "https://www.iasp.info/resources/Crisis_Centres",
                "country": "Global",
                "availability": "24/7",
                "source": "IASP Global Network",
                "active": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "_id": "crisis-4",
                "name": "Kiran Mental Health Helpline (India)",
                "description": "24/7 toll-free mental health rehabilitation helpline launched by Ministry of Social Justice.",
                "phone": "1800-599-0019",
                "website": "https://socialjustice.gov.in",
                "country": "India",
                "availability": "24/7",
                "source": "Government of India",
                "active": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]
        for c in crisis_data:
            await db.crisis_resources.update_one({"_id": c["_id"]}, {"$set": c}, upsert=True)

    # 3. Seed Resources
    logger.info("Ensuring comprehensive mental health resource library for all categories...")
    res_data = [
        {
            "title": "Understanding & Managing Stress",
            "description": "Evidence-informed techniques to identify stress triggers and build coping mechanisms.",
            "content": (
                "Stress is the body's natural reaction to challenges or demands. While acute stress can boost performance, "
                "chronic stress affects both mental and physical health. Key strategies for stress management include:\n"
                "1. Identifying primary stress triggers.\n"
                "2. Practicing daily deep breathing and progressive muscle relaxation.\n"
                "3. Setting healthy boundaries between work and personal life."
            ),
            "category": "Stress",
            "tags": ["stress", "relaxation", "coping", "management", "mental-health"],
            "source": "World Health Organization Well-being Guides",
            "url": "https://www.who.int/news-room/questions-and-answers/item/stress",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Sleep Hygiene Guidelines for Recovery",
            "description": "Practical steps to optimize bedtime routines, reduce night stress, and improve sleep quality.",
            "content": (
                "Quality sleep is foundational for emotional regulation and cognitive function. Practice these sleep hygiene habits:\n"
                "- Maintain a consistent sleep-wake schedule 7 days a week.\n"
                "- Keep your bedroom temperature cool and room dark.\n"
                "- Avoid blue-light screens at least 45 minutes before sleep.\n"
                "- Limit caffeine consumption after 2:00 PM."
            ),
            "category": "Sleep",
            "tags": ["sleep", "hygiene", "rest", "recovery", "stress-relief"],
            "source": "Sleep Research Foundation",
            "url": "https://www.sleepfoundation.org",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Mindfulness & Grounding Techniques for Anxiety",
            "description": "Quick grounding exercises to manage sudden feelings of anxiety, stress, or panic.",
            "content": (
                "When experiencing heightened anxiety, grounding brings attention back to the present moment:\n"
                "• The 5-4-3-2-1 Technique: Acknowledge 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.\n"
                "• Box Breathing: Breathe in for 4 seconds, hold for 4 seconds, exhale for 4 seconds, and hold for 4 seconds."
            ),
            "category": "Anxiety",
            "tags": ["anxiety", "mindfulness", "grounding", "stress-relief"],
            "source": "Mindfulness & Anxiety Support",
            "url": "https://www.apa.org/topics/anxiety",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Academic Pressure & Exam Coping Strategies",
            "description": "Structured approaches to managing exam stress, study anxiety, and avoiding academic burnout.",
            "content": (
                "Academic stress is common among students. Strategies to maintain well-being while studying:\n"
                "- Break study sessions into manageable intervals using the Pomodoro technique.\n"
                "- Schedule daily physical activity and outdoor breaks.\n"
                "- Avoid all-night cramming, which impairs cognitive retention and increases stress."
            ),
            "category": "Academic Pressure",
            "tags": ["academic", "study", "exams", "student-stress", "burnout"],
            "source": "Student Mental Health Network",
            "url": "https://www.jedfoundation.org",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Managing Workplace Burnout & Boundaries",
            "description": "Strategies to prevent emotional exhaustion, manage workloads, and reduce occupational stress.",
            "content": (
                "Workplace burnout manifests as physical and emotional exhaustion, cynicism, and reduced efficacy.\n"
                "1. Communicate realistic capacity limits with supervisors.\n"
                "2. Turn off work notifications outside duty hours.\n"
                "3. Incorporate short 5-minute movement breaks during long sedentary work blocks."
            ),
            "category": "Work Pressure",
            "tags": ["workplace", "burnout", "boundaries", "work-stress", "balance"],
            "source": "Workplace Mental Health Alliance",
            "url": "https://www.apa.org/topics/healthy-workplaces",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Daily Mindfulness Exercises for Stress & Clarity",
            "description": "Simple 3 to 10 minute non-judgmental awareness practices to center your thoughts and calm stress.",
            "content": (
                "Mindfulness involves staying present without judgment.\n"
                "- Mindful Breathing: Focus solely on the sensation of air entering and leaving your nostrils for 3 minutes.\n"
                "- Body Scan: Bring non-critical awareness to sensations starting from your toes up to your scalp."
            ),
            "category": "Mindfulness",
            "tags": ["mindfulness", "meditation", "awareness", "clarity", "stress"],
            "source": "Mindful Science Initiative",
            "url": "https://www.mindful.org",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Progressive Muscle Relaxation Protocol",
            "description": "Systematically tense and release muscle groups to discharge physical tension and stress.",
            "content": (
                "Progressive Muscle Relaxation (PMR) reduces physiological arousal:\n"
                "1. Sit comfortably and close your eyes.\n"
                "2. Tense your feet muscles for 5 seconds, then release for 10 seconds noticing the relaxation.\n"
                "3. Move sequentially up through calves, thighs, abdomen, chest, shoulders, and jaw."
            ),
            "category": "Relaxation",
            "tags": ["relaxation", "pmr", "tension-relief", "stress", "calm"],
            "source": "Clinical Relaxation Practice Manual",
            "url": "https://www.health.harvard.edu",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "Building Emotional Resilience & Stress Management",
            "description": "Transforming negative self-talk into supportive, constructive internal dialogue and managing emotional stress.",
            "content": (
                "Self-compassion entails treating yourself with the same kindness you would offer a friend.\n"
                "- Reframe harsh self-criticism into encouraging growth statements.\n"
                "- Recognize that emotional stress and struggles are a universal human experience, not isolated personal failures."
            ),
            "category": "Emotional Well-being",
            "tags": ["resilience", "self-compassion", "positivity", "stress", "well-being"],
            "source": "Center for Compassionate Living",
            "url": "https://self-compassion.org",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "title": "When & How to Seek Professional Therapy & Support",
            "description": "Understanding therapy modalities, what to expect in initial consultations, and demystifying mental health care.",
            "content": (
                "Seeking therapy is a proactive step toward mental well-being and managing chronic stress or emotional difficulties.\n"
                "- Cognitive Behavioral Therapy (CBT) focuses on identifying unhelpful thought patterns.\n"
                "- Psychodynamic Therapy explores how past experiences shape present reactions.\n"
                "- Initial sessions typically involve an intake evaluation of your goals and symptoms."
            ),
            "category": "Professional Support",
            "tags": ["therapy", "counseling", "professional-care", "support", "mental-health"],
            "source": "National Alliance on Mental Illness (NAMI)",
            "url": "https://www.nami.org",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    ]
    for r in res_data:
        await db.resources.update_one({"title": r["title"]}, {"$set": r}, upsert=True)

    # 4. Seed Professionals Directory (Mock Data clearly labeled)
    existing_profs = await db.professionals.count_documents({})
    if existing_profs == 0:
        logger.info("Seeding sample professional support directory...")
        profs_data = [
            {
                "name": "Dr. Sarah Jenkins, Psy.D.",
                "qualification": "Licensed Clinical Psychologist (Psy.D.)",
                "specialization": "Anxiety, Stress Management, CBT",
                "experience": "12 Years",
                "location": "Boston, MA / Online",
                "consultation_mode": "Online & In-Person",
                "availability": "Mon - Thu (9:00 AM - 5:00 PM)",
                "contact_email": "dr.jenkins@example-mindcare.org",
                "contact_phone": "+1 (555) 234-5678",
                "bio": "Specializes in cognitive-behavioral therapy for stress, academic performance anxiety, and mindfulness.",
                "is_mock": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "name": "Michael Rivera, LMFT",
                "qualification": "Licensed Marriage & Family Therapist",
                "specialization": "Relationships, Academic Stress, Young Adults",
                "experience": "8 Years",
                "location": "San Francisco, CA / Online",
                "consultation_mode": "Online Only",
                "availability": "Tue - Sat (10:00 AM - 6:00 PM)",
                "contact_email": "mrivera.lmft@example-mindcare.org",
                "contact_phone": "+1 (555) 876-5432",
                "bio": "Empathetic counselor focusing on life transitions, emotional well-being, and work-life balance.",
                "is_mock": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "name": "Dr. Ananya Sharma, MD",
                "qualification": "Consultant Psychiatrist (MD)",
                "specialization": "Mood Disorders, Anxiety, Holistic Psychiatry",
                "experience": "15 Years",
                "location": "New Delhi / Tele-consultation",
                "consultation_mode": "Online & In-Person",
                "availability": "Mon - Fri (11:00 AM - 7:00 PM)",
                "contact_email": "dr.sharma@example-mindcare.org",
                "contact_phone": "+91 98765 43210",
                "bio": "Experienced consultant offering comprehensive evaluation and well-being consultation.",
                "is_mock": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]
        for p in profs_data:
            await db.professionals.insert_one(p)

    # 5. Seed Default Admin User & Demo User
    logger.info("Upserting default admin account (admin@mindcare.org)...")
    admin_doc = {
        "name": "System Administrator",
        "email": "admin@mindcare.org",
        "password_hash": hash_password("AdminPass123!"),
        "role": "ADMIN",
        "age_range": "35-44",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    await db.users.update_one({"email": "admin@mindcare.org"}, {"$set": admin_doc, "$setOnInsert": {"created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}}, upsert=True)

    logger.info("Upserting demo user account (user@mindcare.org)...")
    demo_doc = {
        "name": "Alex Demo User",
        "email": "user@mindcare.org",
        "password_hash": hash_password("UserPass123!"),
        "role": "USER",
        "age_range": "25-34",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    await db.users.update_one({"email": "user@mindcare.org"}, {"$set": demo_doc, "$setOnInsert": {"created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}}, upsert=True)
    
    demo_user = await db.users.find_one({"email": "user@mindcare.org"})
    if demo_user:
        uid = str(demo_user["_id"])
        existing_moods = await db.mood_entries.count_documents({"user_id": uid})
        if existing_moods == 0:
            now = datetime.datetime.now(datetime.timezone.utc)
            sample_moods = [
                {"user_id": uid, "mood": 4, "stress_level": 2, "energy_level": 4, "sleep_hours": 7.5, "note": "Felt calm after morning exercise", "created_at": (now - datetime.timedelta(days=4)).isoformat()},
                {"user_id": uid, "mood": 3, "stress_level": 3, "energy_level": 3, "sleep_hours": 6.5, "note": "Busy work schedule", "created_at": (now - datetime.timedelta(days=3)).isoformat()},
                {"user_id": uid, "mood": 2, "stress_level": 4, "energy_level": 2, "sleep_hours": 5.5, "note": "Late night studying", "created_at": (now - datetime.timedelta(days=2)).isoformat()},
                {"user_id": uid, "mood": 4, "stress_level": 2, "energy_level": 4, "sleep_hours": 8.0, "note": "Slept well and meditated", "created_at": (now - datetime.timedelta(days=1)).isoformat()}
            ]
            for sm in sample_moods:
                await db.mood_entries.insert_one(sm)

    logger.info("Database seeding completed successfully.")
