import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

# -----------------------------
# FILE STORAGE
# -----------------------------
DATA_FILE = "leads.csv"

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Skill Growth Navigator",
    page_icon="🧭",
    layout="centered"
)

# -----------------------------
# PREMIUM CSS
# -----------------------------
st.markdown("""
<style>
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 850px;
}

/* Gradient Header */
.gradient-text {
    font-size: 46px;
    font-weight: 900;
    background: linear-gradient(45deg, #06B6D4, #3B82F6, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

/* Card */
.roadmap-card {
    background: rgba(30,41,59,0.45);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    margin: 18px 0;
}

/* Income Highlight Box */
.income-box {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(5, 150, 105, 0.12));
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 14px;
    padding: 20px;
    margin: 18px 0;
    color: #10B981;
}

/* Tags */
.direction-tag {
    display:inline-block;
    padding:8px 16px;
    margin:6px;
    border-radius:30px;
    background:linear-gradient(135deg, rgba(6,182,212,.15), rgba(59,130,246,.15));
    color:#22D3EE;
    font-size:14px;
    font-weight:600;
    border:1px solid rgba(34,211,238,.25);
}

/* Divider */
.glow-divider {
    height:2px;
    background:linear-gradient(90deg, transparent, rgba(6,182,212,.5), transparent);
    margin:28px 0;
}

/* Progress card */
.progress-box {
    background: rgba(15,23,42,0.6);
    padding:16px;
    border-radius:14px;
    border:1px solid rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<h1 class="gradient-text">🧭 Student Skill Growth Navigator</h1>', unsafe_allow_html=True)

st.markdown("""
Discover practical future-ready skills, personalized growth roadmaps, and beginner-friendly remote income paths based on your available schedule.
""")

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# -----------------------------
# STEP 1
# -----------------------------
st.markdown("## 📋 Step 1: Build Your Profile")

progress = st.progress(33)

col1, col2 = st.columns(2)

with col1:
    available_hours = st.slider(
        "How many hours can you dedicate daily?",
        1, 6, 2
    )

    current_skills = st.selectbox(
        "Your current skill level",
        [
            "Complete Beginner",
            "Basic Creative",
            "Business/Analytical",
            "Technical Foundations"
        ]
    )

with col2:
    user_interest = st.selectbox(
        "Choose your growth area",
        [
            "🎯 Career & Skill Development",
            "💼 Business & Entrepreneurship",
            "💰 Finance & Money Management",
            "📢 Marketing, Sales & Communication",
            "👥 Lifestyle & Personal Growth",
            "🎨 Creative Arts & Content Creation",
            "🤝 Social Impact & Helping Others",
            "🌐 Explore All Areas"
        ]
    )

    primary_goal = st.selectbox(
        "Your next 90-day goal",
        [
            "Build a portfolio",
            "Start earning online",
            "Learn modern digital skills"
        ]
    )

# -----------------------------
# DATA ENGINE
# -----------------------------
direction_data = {
    "🎯 Career & Skill Development": {
        "path": "Professional Career Scaling",
        "est_pay": "₹8,000 - ₹15,000 / month per project",
        "gig_breakdown": "Local startups and growing agencies actively pay per-project rates for running basic remote coordination, handling task backlogs, and formatting internal operational documents.",
        "stages": [
            "🏆 Month 1: Learn workplace tools & workflow systems",
            "📈 Month 2: Build project management structures",
            "✨ Month 3: Create portfolio case studies"
        ],
        "directions": [
            "Project Coordination",
            "Research Assistance",
            "Documentation Systems",
            "Remote Operations"
        ]
    },

    "💼 Business & Entrepreneurship": {
        "path": "Digital Business Building",
        "est_pay": "₹12,000 - ₹25,000 / month",
        "gig_breakdown": "Independent e-commerce shops, course creators, and service providers hire remote assistants to securely organize incoming orders, track databases, and follow up with digital customer leads.",
        "stages": [
            "🏆 Month 1: Learn business models",
            "📈 Month 2: Build landing funnels",
            "✨ Month 3: Launch your first offer"
        ],
        "directions": [
            "Lead Generation",
            "Business Operations",
            "Workflow Setup",
            "Client Acquisition"
        ]
    },

    "💰 Finance & Money Management": {
        "path": "Financial Systems Design",
        "est_pay": "₹15,000 - ₹30,000 / custom dashboard setup",
        "gig_breakdown": "Small business owners, retail outlets, and online creators pay great premiums for clean, customized spreadsheets to log daily expenditures, monitor product inventory, and view monthly sales profiles.",
        "stages": [
            "🏆 Month 1: Spreadsheet mastery",
            "📈 Month 2: Dashboard systems",
            "✨ Month 3: Build finance templates"
        ],
        "directions": [
            "Budget Tracking",
            "Financial Dashboards",
            "Data Reporting",
            "Automation Sheets"
        ]
    },

    "📢 Marketing, Sales & Communication": {
        "path": "Digital Growth Marketing",
        "est_pay": "₹10,000 - ₹20,000 / month per client",
        "gig_breakdown": "Budding brands and local consulting businesses look for digital support to write clean email copy, build outreach lists, structure sales pitches, and manage promotional campaign sequences.",
        "stages": [
            "🏆 Month 1: Copywriting basics",
            "📈 Month 2: Funnel systems",
            "✨ Month 3: Campaign analytics"
        ],
        "directions": [
            "Email Marketing",
            "Content Funnels",
            "Brand Outreach",
            "Campaign Metrics"
        ]
    },

    "👥 Lifestyle & Personal Growth": {
        "path": "Productivity Systems",
        "est_pay": "₹5,000 - ₹12,000 / tailored dashboard setup",
        "gig_breakdown": "Busy founders, creative directors, and fast-paced teams commission remote assistance to configure customized daily planners, structure collaborative calendars, and clean up digital work hubs.",
        "stages": [
            "🏆 Month 1: Digital planning",
            "📈 Month 2: Habit systems",
            "✨ Month 3: Build optimization templates"
        ],
        "directions": [
            "Planner Design",
            "Routine Optimization",
            "Schedule Systems",
            "Productivity Templates"
        ]
    },

    "🎨 Creative Arts & Content Creation": {
        "path": "Content Design & Creation",
        "est_pay": "₹12,000 - ₹22,000 / month per account",
        "gig_breakdown": "Local companies (cafes, boutique gyms, realtors) pay monthly retainers for remote managers to design social graphics, draft video captions, schedule posts, and reply to inbound comments.",
        "stages": [
            "🏆 Month 1: Design fundamentals",
            "📈 Month 2: Content workflows",
            "✨ Month 3: Portfolio creation"
        ],
        "directions": [
            "Graphic Design",
            "Video Editing",
            "Social Content",
            "Visual Branding"
        ]
    },

    "🤝 Social Impact & Helping Others": {
        "path": "Community Coordination",
        "est_pay": "₹8,000 - ₹18,000 / month part-time",
        "gig_breakdown": "Training platforms, NGOs, and professional student networks pay remote coordinators to keep their group chats organized, answer basic customer FAQs, and run online event operations.",
        "stages": [
            "🏆 Month 1: Community systems",
            "📈 Month 2: Event workflows",
            "✨ Month 3: Resource coordination"
        ],
        "directions": [
            "Community Moderation",
            "Newsletter Systems",
            "Event Coordination",
            "Volunteer Ops"
        ]
    },

    "🌐 Explore All Areas": {
        "path": "Universal Digital Foundations",
        "est_pay": "₹7,000 - ₹15,000 / month baseline",
        "gig_breakdown": "General remote gigs rely on simple digital flexibility: inputting clear inventory data, proofreading written copy drafts, organizing file structures, and handling routine business updates.",
        "stages": [
            "🏆 Month 1: Learn core tools",
            "📈 Month 2: Connect systems",
            "✨ Month 3: Pick specialization"
        ],
        "directions": [
            "Virtual Assistance",
            "Basic Data Work",
            "Content Support",
            "Digital Operations"
        ]
    }
}

selected = direction_data[user_interest]
total_hours = available_hours * 90

# -----------------------------
# STEP 2
# -----------------------------
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown("## 📊 Step 2: Your 90-Day Roadmap")

progress.progress(66)

st.info(f"⏳ You have **{total_hours} focused hours** available over the next 90 days.")

st.markdown(f"""
<div class="roadmap-card">
<h3>✨ Your Selected Track</h3>
<p><b>{selected['path']}</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="income-box">
    <h4 style="margin-top: 0;">💰 Estimated Side-Income Potential</h4>
    <p style="font-size: 22px; font-weight: 800;">{selected['est_pay']}</p>
    <p>{selected['gig_breakdown']}</p>
</div>
""", unsafe_allow_html=True)

for stage in selected["stages"]:
    st.markdown(stage)

st.markdown("### 🚀 Career Directions")

tags = "".join(
    [f'<span class="direction-tag">{d}</span>' for d in selected["directions"]]
)

st.markdown(tags, unsafe_allow_html=True)

if current_skills == "Complete Beginner":
    st.warning("Start with one foundational tool and focus on consistency.")
elif current_skills == "Technical Foundations":
    st.success("You can accelerate faster by building portfolio projects immediately.")

# -----------------------------
# STEP 3
# -----------------------------
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown("## 📥 Step 3: Get Your Free Skill Blueprint")

progress.progress(100)

with st.form("lead_form", clear_on_submit=True):
    first_name = st.text_input("First Name")
    whatsapp_num = st.text_input("WhatsApp Number")

    consent = st.checkbox(
        "I agree to receive my custom roadmap and occasional learning updates."
    )

    submit = st.form_submit_button("🚀 Get my Free Consultation")

# -----------------------------
# VALIDATION
# -----------------------------
def valid_phone(phone):
    cleaned = re.sub(r"\D", "", phone)
    return len(cleaned) >= 10

# -----------------------------
# SAVE DATA
# -----------------------------
if submit:

    if not first_name.strip():
        st.error("Please enter your name.")
    elif not valid_phone(whatsapp_num):
        st.error("Enter a valid WhatsApp number.")
    elif not consent:
        st.error("Please give consent.")
    else:
        payload = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": first_name.strip(),
            "WhatsApp": whatsapp_num,
            "Hours": available_hours,
            "Skill Level": current_skills,
            "Interest": user_interest,
            "Goal": primary_goal
        }

        new_df = pd.DataFrame([payload])

        if os.path.exists(DATA_FILE):
            existing = pd.read_csv(DATA_FILE)
            updated = pd.concat([existing, new_df], ignore_index=True)
        else:
            updated = new_df

        updated.to_csv(DATA_FILE, index=False)

        st.success(f"""
🎉 Success, {first_name}!

Your personalized roadmap is being prepared.

You’re officially on your way toward building:
**{selected['path']}**
""")

        st.balloons()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.caption("Built for ambitious students who want practical digital career growth.")