import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# -----------------------------
# FILE STORAGE
# -----------------------------
DATA_FILE = "lead_database.csv"

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

.gradient-text {
    font-size: 46px;
    font-weight: 900;
    background: linear-gradient(45deg, #06B6D4, #3B82F6, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.roadmap-card {
    background: rgba(30,41,59,0.45);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    margin: 18px 0;
}

.income-box {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.12));
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 14px;
    padding: 20px;
    margin: 18px 0;
    color: #10B981;
}

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

.glow-divider {
    height:2px;
    background:linear-gradient(90deg, transparent, rgba(6,182,212,.5), transparent);
    margin:28px 0;
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
    available_hours = st.slider("How many hours can you dedicate daily?", 1, 6, 2)

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
        "est_pay": "₹8,000 - ₹15,000 / month"
    },
    "💼 Business & Entrepreneurship": {
        "path": "Digital Business Building",
        "est_pay": "₹12,000 - ₹25,000 / month"
    },
    "💰 Finance & Money Management": {
        "path": "Financial Systems Design",
        "est_pay": "₹15,000 - ₹30,000 / project"
    },
    "📢 Marketing, Sales & Communication": {
        "path": "Digital Growth Marketing",
        "est_pay": "₹10,000 - ₹20,000 / month"
    },
    "👥 Lifestyle & Personal Growth": {
        "path": "Productivity Systems",
        "est_pay": "₹5,000 - ₹12,000 / setup"
    },
    "🎨 Creative Arts & Content Creation": {
        "path": "Content Design & Creation",
        "est_pay": "₹12,000 - ₹22,000 / month"
    },
    "🤝 Social Impact & Helping Others": {
        "path": "Community Coordination",
        "est_pay": "₹8,000 - ₹18,000 / month"
    },
    "🌐 Explore All Areas": {
        "path": "Universal Digital Foundations",
        "est_pay": "₹7,000 - ₹15,000 / month"
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

st.info(f"⏳ You have **{total_hours} focused hours** available.")

st.markdown(f"""
<div class="roadmap-card">
<h3>✨ Your Selected Track</h3>
<p><b>{selected['path']}</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="income-box">
<h4>💰 Estimated Side-Income Potential</h4>
<p style="font-size:22px;font-weight:800;">{selected['est_pay']}</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# STEP 3
# -----------------------------
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown("## 📥 Step 3: Get Your Free Skill Blueprint")

progress.progress(100)

st.write("""
Receive your custom beginner roadmap directly on WhatsApp.

Includes:
- 90-day checklist
- Free Earning resources
- Portfolio project suggestions
- Beginner-friendly earning paths
""")

# -----------------------------
# FORM
# -----------------------------
with st.form("lead_form", clear_on_submit=True):

    first_name = st.text_input("First Name")
    whatsapp_num = st.text_input("WhatsApp Number")

    consent = st.checkbox(
        "I agree to receive my roadmap and learning updates."
    )

    submit = st.form_submit_button("🚀 Get My Free Consultation")

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
        import requests

        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdt3gJJK4_SiivkMX5VGVxDljuSrzpbtADXh1DqUknuNcxkQw/formResponse"

        form_data = {
            "entry.42428905": first_name,
            "entry.1974958050": whatsapp_num,
            "entry.1294238968": str(available_hours),
            "entry.1711852881": user_interest,
            "entry.137205597": primary_goal
        }

        requests.post(form_url, data=form_data)

        st.success(f"""
🎉 Success, {first_name}!

Your personalized roadmap is being prepared.

You're officially on your way toward:
**{selected['path']}**
""")

        st.balloons()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

st.caption("Built for ambitious students who want practical digital career growth.")