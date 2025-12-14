info("Enter your details and ask visa-related questions for personalized eligibility assessment.")
    st.markdown('</div>', unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🛂 SwiftVisa AI</h1>
    <p style="font-size: 18px; margin: 0;">Intelligent Visa Eligibility Assessment Powered by AI</p>
    <p style="font-size: 14px; opacity: 0.9;">Get authoritative visa decisions using advanced RAG technology</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------
if "response" not in st.session_state:
    st.session_state.response = None

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

if "progress" not in st.session_state:
    st.session_state.progress = 0

# -------------------------------------------------------
# FORM INPUT SECTION
# -------------------------------------------------------
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.subheader("📋 Applicant Information")

with st.form("visa_form"):
    # Basic Information
    st.markdown("### 👤 Basic Details")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=1, max_value=100, step=1, help="Your current age in years")
    
    with col2:
        nationality = st.text_input("Nationality", placeholder="e.g., Indian", help="Your country of citizenship")
    
    with col3:
        education_level = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD"], help="Highest level of education")

    # Visa Information
    st.markdown("### 🛂 Visa Details")
    col4, col5 = st.columns(2)
    
    with col4:
        visa_type = st.selectbox(
            "Visa Type",
            [
                "H1B", "H4", "F1", "B1/B2",
                "Canada PR", "Canada Visitor",
                "UK Skilled Worker", "UK Visitor",
                "Schengen Tourist", "Schengen Work"
            ],
            help="Select the visa category you're interested in"
        )
    
    with col5:
        # Country automatically derived
        visa_country_map = {
            "H1B": "United States",
            "H4": "United States",
            "F1": "United States",
            "B1/B2": "United States",
            "Canada PR": "Canada",
            "Canada Visitor": "Canada",
            "UK Skilled Worker": "United Kingdom",
            "UK Visitor": "United Kingdom",
            "Schengen Tourist": "Schengen (EU)",
            "Schengen Work": "Schengen (EU)",
        }
        selected_country = visa_country_map.get(visa_type)
        st.markdown(f"**📍 Target Country:** {selected_country}")
        st.markdown("---")

    # Dynamic Fields based on Visa Type
    if visa_type in ["H4"]:
        st.markdown("### 👫 Spouse Information (H4 Specific)")
        col6, col7 = st.columns(2)
        with col6:
            spouse_status = st.selectbox("Spouse on H1B?", ["Yes", "No"], help="Is your spouse currently on H1B visa?")
        with col7:
            has_i140 = st.selectbox("Approved I-140?", ["Yes", "No"], help="Does your spouse have an approved I-140 petition?")
    
    elif visa_type == "Canada PR":
        st.markdown("### 🎓 Canada PR Requirements")
        col8, col9, col10 = st.columns(3)
        with col8:
            education = st.selectbox("Education", ["Bachelor", "Master", "PhD"], help="Highest education level")
        with col9:
            experience_years = st.number_input("Work Experience (years)", min_value=0, max_value=40, help="Years of skilled work experience")
        with col10:
            ielts_score = st.number_input("IELTS Score", min_value=0.0, max_value=9.0, step=0.5, help="Overall IELTS band score")
    
    elif visa_type == "Schengen Tourist":
        st.markdown("### ✈️ Schengen Tourist Requirements")
        col11, col12 = st.columns(2)
        with col11:
            travel_history = st.selectbox("Travel History", ["Yes", "No"], help="Have you traveled internationally before?")
        with col12:
            bank_balance = st.number_input("Bank Balance", min_value=0, help="Current bank balance in local currency")

    # Question Section
    st.markdown("### ❓ Your Visa Question")
    user_question = st.text_area(
        "Ask a specific question about your visa eligibility:",
        placeholder="Example: Am I eligible for an H4 visa if my spouse has H1B with approved I-140?",
        height=100,
        help="Be specific about your situation for the best assessment"
    )

    # Submit Button
    col_submit, col_reset = st.columns([1, 1])
    with col_submit:
        submitted = st.form_submit_button("🔍 Analyze Eligibility", use_container_width=True)
    with col_reset:
        reset = st.form_submit_button("🔄 Reset Form", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# BACKEND CALL (Your RAG Pipeline)
# -------------------------------------------------------
def call_backend(query):
    return rag_pipeline(query)

# -------------------------------------------------------
# SUBMISSION HANDLER
# -------------------------------------------------------
if submitted:
    if user_question.strip() == "":
        st.error("❗ Please enter a visa-related question.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Initializing analysis...")
        progress_bar.progress(10)
        
        status_text.text("Retrieving relevant documents...")
        progress_bar.progress(30)
        
        status_text.text("Processing with AI model...")
        progress_bar.progress(60)
        
        with st.spinner("Finalizing decision..."):
            output = call_backend(user_question)
        
        progress_bar.progress(100)
        status_text.text("Analysis complete!")
        
        st.session_state.response = output["response"]
        
        # Collect form data
        form_data = {
            "age": age,
            "nationality": nationality,
            "education_level": education_level,
            "visa_type": visa_type,
            "country": selected_country,
            "user_question": user_question
        }
        
        # Add conditional fields
        if visa_type in ["H4"]:
            form_data.update({
                "spouse_on_h1b": spouse_status,
                "approved_i140": has_i140
            })
        elif visa_type == "Canada PR":
            form_data.update({
                "education": education,
                "work_experience_years": experience_years,
                "ielts_score": ielts_score
            })
        elif visa_type == "Schengen Tourist":
            form_data.update({
                "travel_history": travel_history,
                "bank_balance": bank_balance
            })
        
        st.session_state.form_data = form_data
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        st.success("✅ Eligibility analysis completed!")

if reset:
    st.session_state.response = None
    st.session_state.form_data = {}
    st.rerun()

# -------------------------------------------------------
# DISPLAY OUTPUT
# -------------------------------------------------------
if st.session_state.response:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader("🧾 Visa Officer Decision")
    
    # Parse the response to extract key information
    response_text = st.session_state.response
    
    # Display the full response in a styled box
    st.markdown(
        f"""
        <div style="
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            color: #333;
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
        ">
        <pre style="white-space: pre-wrap; font-size: 16px; margin: 0;">{response_text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional sections
    col_result1, col_result2 = st.columns(2)
    
    with col_result1:
        with st.expander("📊 Your Submitted Information"):
            st.json(st.session_state.form_data)
    
    with col_result2:
        with st.expander("💡 Tips for Next Steps"):
            st.markdown("""
            - Review the decision carefully
            - Consult with an immigration attorney for personalized advice
            - Ensure all documents are up-to-date
            - Check official government websites for latest requirements
            """)
    
    # Action buttons
    st.markdown("---")
    col_action1, col_action2, col_action3 = st.columns(3)
    with col_action1:
        if st.button("📤 Share Results", use_container_width=True):
            st.info("Sharing functionality coming soon!")
    with col_action2:
        if st.button("💾 Save to PDF", use_container_width=True):
            st.info("PDF export functionality coming soon!")
    with col_action3:
        if st.button("🔄 New Assessment", use_container_width=True):
            st.session_state.response = None
            st.session_state.form_data = {}
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>© 2025 SwiftVisa AI | Powered by Gemini & FAISS | For informational purposes only</p>
    <p style="font-size: 12px;">Not legal advice. Consult immigration professionals for official guidance.</p>
</div>

""", unsafe_allow_html=True)
