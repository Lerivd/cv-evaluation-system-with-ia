import streamlit as st
from models.cv_model import AnalisisCV
from services.pdf_processor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato

def main():
    st.set_page_config(
        page_title="CV Evaluation System",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📄 CV Evaluation System with AI")
    st.markdown("""
    **Analyze resumes and evaluate candidates objectively using AI**
    
    This system uses artificial intelligence to:
    - Extract key information from PDF resumes
    - Analyze candidate experience and skills
    - Evaluate fit for specific job positions
    - Provide objective hiring recommendations
    """)
    
    st.divider()
    
    input_col, result_col = st.columns([1, 1], gap="large")
    
    with input_col:
        process_input()
    
    with result_col:
        show_results_area()

def process_input():
    st.header("📋 Input Data")
    
    cv_file = st.file_uploader(
        "**1. Upload candidate CV (PDF)**",
        type=['pdf'],
        key="cv_uploader",
        help="Select a PDF file containing the resume to evaluate."
    )
    
    if cv_file is not None:
        st.success(f"✅ CV loaded: {cv_file.name}")
    
    st.markdown("---")
    
    st.markdown("**2. Job Description (PDF)**")
    job_file = st.file_uploader(
        "**Upload Job Requirements (PDF)**",
        type=['pdf'],
        key="job_uploader",
        help="Select a PDF file containing the job description and requirements."
    )
    
    if job_file is not None:
        st.success(f"✅ Job description loaded: {job_file.name}")
    
    st.markdown("---")
    
    btn_col1, btn_col2 = st.columns([1, 1])
    
    with btn_col1:
        analyze = st.button(
            "🔍 Analyze Candidate", 
            type="primary",
            use_container_width=True
        )
    
    with btn_col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()
    
    st.session_state['archivo_cv'] = cv_file
    st.session_state['archivo_puesto'] = job_file
    st.session_state['analizar'] = analyze

def show_results_area():
    st.header("📊 Analysis Results")
    
    if st.session_state.get('analizar', False):
        cv_file = st.session_state.get('archivo_cv')
        job_file = st.session_state.get('archivo_puesto')
        
        if cv_file is None:
            st.error("⚠️ Please upload the candidate's CV (PDF)")
            return
            
        if job_file is None:
            st.error("⚠️ Please upload the job requirements (PDF)")
            return
        
        execute_analysis(cv_file, job_file)
    else:
        st.info("""
        👆 **Instructions:**
        
        1. Upload the candidate's CV in PDF format
        2. Upload the Job Requirements in PDF format
        3. Click "Analyze Candidate"
        4. The complete candidate analysis will appear here
        """)

def execute_analysis(cv_file, job_file):
    with st.spinner("🔄 Processing documents..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📄 Extracting text from Job Description...")
        progress_bar.progress(20)
        job_text = extraer_texto_pdf(job_file)
        
        if job_text.startswith("Error"):
            st.error(f"❌ Job PDF Error: {job_text}")
            return

        status_text.text("📄 Extracting text from CV...")
        progress_bar.progress(40)
        cv_text = extraer_texto_pdf(cv_file)
        
        if cv_text.startswith("Error"):
            st.error(f"❌ CV PDF Error: {cv_text}")
            return
        
        status_text.text("🤖 Preparing AI analysis...")
        progress_bar.progress(60)
        
        status_text.text("📊 Analyzing candidate fit...")
        progress_bar.progress(80)
        
        result = evaluar_candidato(cv_text, job_text)
        
        status_text.text("✅ Analysis completed")
        progress_bar.progress(100)
        
        progress_bar.empty()
        status_text.empty()
        
        display_results(result)

def display_results(result: AnalisisCV):
    st.subheader("🎯 Main Evaluation")
    
    if result.porcentaje_ajuste >= 80:
        color = "🟢"
        level = "EXCELLENT"
        message = "Highly recommended candidate"
    elif result.porcentaje_ajuste >= 60:
        color = "🟡"
        level = "GOOD"
        message = "Recommended candidate with reservations"
    elif result.porcentaje_ajuste >= 40:
        color = "🟠"
        level = "AVERAGE"
        message = "Candidate requires additional evaluation"
    else:
        color = "🔴"
        level = "LOW"
        message = "Candidate not recommended"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Job Fit Percentage",
            value=f"{result.porcentaje_ajuste}%",
            delta=f"{color} {level}"
        )
        st.markdown(f"**{message}**")
    
    st.divider()
    
    st.subheader("👤 Candidate Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**👨‍💼 Name:** {result.nombre_candidato}")
        st.info(f"**⏱️ Experience:** {result.experiencia_años} years")
    
    with col2:
        st.info(f"**🎓 Education:** {result.education}")
    
    st.subheader("💼 Relevant Experience")
    st.info(f"📋 **Experience Summary:**\n\n{result.experiencia_relevante}")
    
    st.divider()
    
    st.subheader("🛠️ Key Technical Skills")
    if result.habilidades_clave:
        cols = st.columns(min(len(result.habilidades_clave), 4))
        for i, skill in enumerate(result.habilidades_clave):
            with cols[i % 4]:
                st.success(f"✅ {skill}")
    else:
        st.warning("No specific technical skills identified")
    
    st.divider()
    
    fortress_col, improvement_col = st.columns(2)
    
    with fortress_col:
        st.subheader("💪 Main Strengths")
        if result.fortalezas:
            for i, strength in enumerate(result.fortalezas, 1):
                st.markdown(f"**{i}.** {strength}")
        else:
            st.info("No specific strengths identified")
    
    with improvement_col:
        st.subheader("📈 Development Areas")
        if result.areas_mejora:
            for i, area in enumerate(result.areas_mejora, 1):
                st.markdown(f"**{i}.** {area}")
        else:
            st.info("No specific development areas identified")
    
    st.divider()
    
    st.subheader("📋 Final Recommendation")
    
    if result.porcentaje_ajuste >= 70:
        st.success("""
        ✅ **RECOMMENDED CANDIDATE**
        
        The candidate's profile is well-aligned with the job requirements. 
        It is recommended to proceed with the next stages of the selection process.
        """)
    elif result.porcentaje_ajuste >= 50:
        st.warning("""
        ⚠️ **CANDIDATE WITH POTENTIAL**
        
        The candidate shows potential but requires additional evaluation. 
        A technical interview is recommended to validate specific competencies.
        """)
    else:
        st.error("""
        ❌ **NOT RECOMMENDED CANDIDATE**
        
        The profile does not align sufficiently with the job requirements. 
        It is recommended to continue searching for more suitable candidates.
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save Analysis", use_container_width=True):
            st.info("Save functionality - In development")