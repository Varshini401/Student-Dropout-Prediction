import streamlit as st
import pandas as pd
import joblib
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Student Dropout Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= LOAD MODEL =================
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_PATH, "risk_prediction_model.pkl"))
le_dict = joblib.load(os.path.join(BASE_PATH, "encoders.pkl"))
le_target = joblib.load(os.path.join(BASE_PATH, "target_encoder.pkl"))

# ================= PREMIUM CSS OVERRIDES =================
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }

/* ---------- Overall Background ---------- */
.stApp {
    background: #FAF7F2;
}

/* ---------- Container Padding ---------- */
.main .block-container {
    padding: 2rem 5rem;
}

/* ---------- REMOVE ALL INTER-BLOCK VERTICAL MARGINS/PADDING ---------- */
div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    margin-top: 0px !important;
    padding-top: 0px !important;
}

/* ---------- Custom UI Cards Look ---------- */
.hero-card, .form-card, .result-card, .about-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(161, 92, 56, 0.05);
    margin-top: 10px;
    margin-bottom: 20px;
    border: 1px solid rgba(161, 92, 56, 0.08);
}

/* ---------- Title & Typography ---------- */
.title {
    font-size: 44px;
    font-weight: 800;
    color: #2D2D2D;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.brand-orange {
    color: #A15C38;
}
.subtitle {
    font-size: 16px;
    line-height: 1.7;
    color: #666;
    margin-top: 15px;
}

/* ---------- Badge Rows ---------- */
.feature-badge-container {
    display: flex;
    gap: 30px;
    margin-top: 25px;
}
.feature-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #333;
}

/* ---------- Section Title ---------- */
.section-header {
    font-size: 22px;
    font-weight: 700;
    color: #2D2D2D;
    margin-bottom: 25px;
}

/* ---------- Form Input Label Customization ---------- */
div[data-testid="stWidgetLabel"] p {
    font-weight: 600 !important;
    color: #444 !important;
}

/* ---------- Premium Form Button ---------- */
.stButton>button {
    width: 100%;
    height: 54px;
    background: #A15C38;
    color: white;
    font-size: 18px;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: 0.3s ease;
    box-shadow: 0px 4px 15px rgba(161, 92, 56, 0.2);
    margin-top: 20px;
}
.stButton>button:hover {
    background: #85492A;
    transform: translateY(-1px);
    box-shadow: 0px 6px 20px rgba(161, 92, 56, 0.3);
}

/* ---------- Multi Column Results Box ---------- */
.split-result-box {
    display: flex;
    background: #A15C38;
    border-radius: 15px;
    color: white;
    overflow: hidden;
    margin-top: 15px;
    box-shadow: 0px 10px 25px rgba(161, 92, 56, 0.15);
}
.result-left {
    flex: 1.2;
    padding: 30px;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.result-right {
    flex: 1;
    padding: 30px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.05);
}

/* ---------- Recommendations Panel ---------- */
.recommend-box {
    background: #FFF9F6;
    border-radius: 15px;
    padding: 30px;
    margin-top: 25px;
    border: 1px solid rgba(161, 92, 56, 0.1);
}
.rec-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-top: 15px;
}
.rec-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background: white;
    padding: 12px 18px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
    font-size: 15px;
    color: #444;
}

/* ---------- Project Details Split Layout ---------- */
.about-grid {
    display: flex;
    gap: 40px;
}
.about-desc {
    flex: 1.2;
    font-size: 15px;
    line-height: 1.7;
    color: #555;
}
.metadata-table {
    flex: 1;
    background: #FDFCFB;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(0,0,0,0.04);
}
.meta-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px dashed #EEE;
    font-size: 14px;
}
.meta-row:last-child { border-bottom: none; }
.meta-label { font-weight: 600; color: #666; }
.meta-value { font-weight: 700; color: #2D2D2D; }

/* ---------- Branded Bottom Footer ---------- */
.footer-container {
    text-align: center;
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid #EAEAEA;
}
.footer-dev {
    font-size: 14px;
    color: #666;
}
.footer-links {
    display: flex;
    justify-content: center;
    gap: 25px;
    margin-top: 15px;
}
.footer-links a {
    text-decoration: none;
    font-weight: 600;
    color: #444;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border: 1px solid #DDD;
    border-radius: 8px;
    background: white;
    transition: 0.2s ease;
}
.footer-links a:hover { 
    color: #A15C38; 
    border-color: #A15C38;
    box-shadow: 0px 4px 10px rgba(161, 92, 56, 0.08);
}
.footer-links svg {
    width: 18px;
    height: 18px;
    fill: currentColor;
}
</style>
""", unsafe_allow_html=True)

# ================= HERO SECTION =================
left, right = st.columns([1.2, 1])

with left:
    st.markdown("""
    <div style="padding-top: 20px;">
        <div class="title">
            STUDENT DROPOUT<br><span class="brand-orange">PREDICTION SYSTEM</span>
        </div>
        <div class="subtitle">
            Predict student dropout risk using Machine Learning based on academic performance and behavioural factors. 
            Receive personalized recommendations that help improve student success and support timely academic intervention.
        </div>
        <div class="feature-badge-container">
            <div class="feature-badge">🎓 AI Powered Prediction</div>
            <div class="feature-badge">📊 Smart Recommendations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    banner_path = os.path.join(BASE_PATH, "images", "banner.jpg")
    st.image(banner_path, use_container_width=True)

# ================= STUDENT INFORMATION CARD =================
st.markdown("<div class='form-card'><div class='section-header'>📋 STUDENT INFORMATION</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Enter Your Name", placeholder="Enter your full name")
    age = st.number_input("Age", min_value=17, max_value=25, value=None, placeholder="Enter age")
    gender = st.selectbox("Gender", ["Select", "Male", "Female"])
    location = st.selectbox("Location", ["Select", "Urban", "Rural"])
    twelfth = st.number_input("12th Percentage", min_value=0.0, max_value=100.0, value=None, placeholder="Enter percentage")
    course = st.selectbox("Course Type", ["Select", "Engineering", "Science", "Arts"])
    cgpa = st.number_input("Current Semester CGPA", min_value=0.0, max_value=10.0, value=None, placeholder="Enter CGPA")
    overall = st.number_input("Overall CGPA", min_value=0.0, max_value=10.0, value=None, placeholder="Enter Overall CGPA")
    prev_result = st.selectbox("Previous Semester Result", ["Select", "Pass", "Fail"])

with col2:
    arrears = st.number_input("Arrears Count", min_value=0, max_value=15, value=None, placeholder="Enter arrears")
    attendance = st.number_input("Attendance Percentage", min_value=0.0, max_value=100.0, value=None, placeholder="Enter attendance")
    participation = st.selectbox("Class Participation", ["Select", "High", "Medium", "Low"])
    stress = st.selectbox("Stress Level", ["Select", "Low", "Medium", "High"])
    motivation = st.selectbox("Motivation Level", ["Select", "Low", "Medium", "High"])
    interest = st.selectbox("Interest in Course", ["Select", "Low", "Medium", "High"])
    income = st.selectbox("Family Income", ["Select", "Low", "Medium", "High"])
    scholarship = st.selectbox("Scholarship Status", ["Select", "Yes", "No"])
    discipline = st.selectbox("Disciplinary Action", ["Select", "No", "Yes"])

submitted = st.button("🔍 ANALYZE DROPOUT RISK")
st.markdown("</div>", unsafe_allow_html=True)

# ================= VALIDATION & EXECUTION LOGIC =================
if submitted:
    if (
        name.strip() == "" or age is None or twelfth is None or cgpa is None or 
        overall is None or arrears is None or attendance is None or 
        gender == "Select" or location == "Select" or course == "Select" or 
        prev_result == "Select" or participation == "Select" or stress == "Select" or 
        motivation == "Select" or interest == "Select" or income == "Select" or 
        scholarship == "Select" or discipline == "Select"
    ):
        st.error("⚠ Please complete all fields before analyzing the dropout risk.")
        st.stop()

    with st.spinner("🤖 AI is analyzing the student profile..."):
        input_dict = {
            "age": age, "gender": gender, "location": location, "12th_percentage": twelfth,
            "course_type": course, "current_sem_cgpa": cgpa, "overall_cgpa": overall,
            "prev_sem_result": prev_result, "arrears_count": arrears, "attendance_percentage": attendance,
            "class_participation": participation, "stress_level": stress, "motivation_level": motivation,
            "interest_in_course": interest, "family_income": income, "scholarship_status": scholarship,
            "disciplinary_action": discipline
        }

        input_df = pd.DataFrame([input_dict])

        for col in input_df.columns:
            if col in le_dict:
                input_df[col] = le_dict[col].transform(input_df[col])

        input_df = input_df.reindex(columns=model.feature_names_in_)

        prediction = model.predict(input_df)
        probabilities = model.predict_proba(input_df)[0]
        predicted_class = le_target.inverse_transform(prediction)[0]
        probability_dict = dict(zip(le_target.classes_, probabilities))

        risk_percentage = probability_dict.get("At Risk", 0) * 100

        # --- RISK BOOST ENGINE ---
        risk_boost = 0
        if twelfth < 50: risk_boost += 8
        elif twelfth < 70: risk_boost += 3
        if cgpa < 5: risk_boost += 15
        elif cgpa < 6: risk_boost += 8
        if overall < 5: risk_boost += 12
        elif overall < 6: risk_boost += 6
        if attendance < 50: risk_boost += 15
        elif attendance < 75: risk_boost += 8
        if prev_result == "Fail": risk_boost += 10
        if arrears >= 8: risk_boost += 18
        elif arrears >= 5: risk_boost += 12
        elif arrears >= 3: risk_boost += 6
        elif arrears >= 1: risk_boost += 3
        if participation == "Low": risk_boost += 6
        if motivation == "Low": risk_boost += 8
        if interest == "Low": risk_boost += 6
        if stress == "High": risk_boost += 6
        if discipline == "Yes": risk_boost += 8
        if scholarship == "No": risk_boost += 2

        risk_percentage = min(risk_percentage + risk_boost, 99)

        if risk_percentage < 30:
            risk_label = "LOW"
            result_color = "#2E8B57"
            emoji = "🟢"
        elif risk_percentage < 60:
            risk_label = "MODERATE"
            result_color = "#D48C2B"
            emoji = "🟡"
        else:
            risk_label = "HIGH"
            result_color = "#C0392B"
            emoji = "🔴"

        # --- RECOMMENDATION COMPILER ---
        recommendations = []
        if attendance < 75: recommendations.append("Improve attendance consistency")
        if cgpa < 6: recommendations.append("Enhance academic performance (CGPA)")
        if arrears > 0: recommendations.append("Clear pending arrears")
        if participation == "Low": recommendations.append("Increase class participation")
        if stress == "High": recommendations.append("Manage stress levels effectively")
        if discipline == "Yes": recommendations.append("Maintain academic discipline")

        if len(recommendations) == 0:
            recommendations.append("Excellent performance. Continue maintaining your academic consistency.")

        # --- BUILD PREDICTION SECTION MANUALLY AS A CONSOLIDATED TAG ---
        # NOTE: Fixed Markdown codeblock glitch by removing multi-line indentation spaces from string lines
        result_content = f"""<div class='result-card'>
<div class='section-header'>📊 PREDICTION RESULT</div>
<div class="split-result-box" style="background: {result_color}; color: white;">
<div class="result-left">
<div style="font-size: 13px; font-weight: 700; opacity: 0.85; letter-spacing: 1px;">DROPOUT RISK LEVEL</div>
<div style="font-size: 38px; font-weight: 800; margin-top: 5px;">{emoji} {risk_label}</div>
</div>
<div class="result-right">
<div style="font-size: 13px; font-weight: 700; opacity: 0.85; letter-spacing: 1px;">RISK SCORE</div>
<div style="font-size: 38px; font-weight: 800; margin-top: 5px;">{risk_percentage:.2f}%</div>
<div style="font-size: 12px; opacity: 0.8; margin-top: 2px;">Probability of dropout risk</div>
</div>
</div>
<div class="recommend-box" style="text-align: left;">
<div style="font-weight: 700; color: #A15C38; font-size: 16px; margin-bottom: 10px;">💡 RECOMMENDED FOCUS AREAS</div>
<div class="rec-grid">"""

        for item in recommendations:
            result_content += f"""<div class="rec-item"><span style="color: #A15C38; font-weight: bold;">✔</span> {item}</div>"""

        result_content += "</div></div></div>"
        st.markdown(result_content, unsafe_allow_html=True)

# ================= ABOUT PROJECT SECTION =================
st.markdown("""
<div class='about-card'>
    <div class='section-header'>ℹ ABOUT THIS PROJECT</div>
    <div class="about-grid">
        <div class="about-desc">
            This Student Dropout Prediction System uses Machine Learning to identify students who may be at risk of dropping out based on academic performance and behavioural factors. The system provides early risk prediction along with personalized recommendations to support timely academic intervention and improve student success.
        </div>
        <div class="metadata-table">
            <div class="meta-row">
                <span class="meta-label">🎓 Algorithm</span>
                <span class="meta-value">Random Forest Classifier</span>
            </div>
            <div class="meta-row">
                <span class="meta-label">📊 Model Accuracy</span>
                <span class="meta-value">94%</span>
            </div>
            <div class="meta-row">
                <span class="meta-label">🗃 Dataset</span>
                <span class="meta-value">Student Academic Dataset</span>
            </div>
            <div class="meta-row">
                <span class="meta-label">👤 Input Features</span>
                <span class="meta-value">17 Academic & Behavioural Attributes</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<div class="footer-container">
    <div class="footer-dev">Developed by <strong style="color: #A15C38;">Varshini V</strong><br>AI & Data Science Graduate</div>
    <div class="footer-links">
        <a href="https://github.com/Varshini401" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub
        </a>
        <a href="https://www.linkedin.com/in/YOUR-LINKEDIN-USERNAME/" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            LinkedIn
        </a>
    </div>
    <div style="margin-top: 15px; color: #999; font-size: 12px;">© 2026 Student Dropout Prediction System. All rights reserved.</div>
</div>
""", unsafe_allow_html=True)
