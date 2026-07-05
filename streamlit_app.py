import streamlit as st
from graph.graph_builder import build_graph
from database.database import SessionLocal
from database.models import Employee
from security_guardrails.input_guard import validate_input
from security_guardrails.output_guard import validate_output

# Initialize Graph
graph = build_graph()

st.set_page_config(
    page_title="Employee Intelligence Platform",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .agent-trace {
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.8rem;
        background-color: #1e1e1e;
        color: #dcdcdc;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #4caf50;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    .agent-name {
        color: #569cd6;
        font-weight: bold;
    }
    .agent-action {
        color: #ce9178;
    }
    </style>
""", unsafe_allow_html=True)

# Helper to verify credentials
def verify_login(email, password):
    db = SessionLocal()
    try:
        user = db.query(Employee).filter(Employee.email == email, Employee.password == password).first()
        if user:
            return {
                "employee_id": user.employee_id,
                "name": user.name,
                "role": user.role,
                "department": user.department
            }
        return None
    finally:
        db.close()

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Logout Function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.messages = []
    if "last_trace" in st.session_state:
        del st.session_state.last_trace
    st.rerun()

# Login Page
def login_page():
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #2e7bcf;'>🏢 Employee Intelligence Platform</h1>
            <p style='color: #666;'>Secure Enterprise Access</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                user_info = verify_login(email, password)
                if user_info:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_info
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")

# Main Application Logic
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar - User Info & Trace
    with st.sidebar:
        st.markdown(f"""
            <div style='background-color: #f1f3f9; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid #2e7bcf;'>
                <h4 style='margin:0; color: #1e3a8a;'>👤 {st.session_state.current_user['name']}</h4>
                <p style='margin:0; font-size: 0.9rem; color: #4b5563;'><b>Role:</b> {st.session_state.current_user['role']}</p>
                <p style='margin:0; font-size: 0.9rem; color: #4b5563;'><b>Dept:</b> {st.session_state.current_user['department']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.divider()
        st.subheader("🕵️ Agent Communication Trace")
        trace_container = st.container()
        
        # Persistent trace display
        if "last_trace" in st.session_state:
            for step in st.session_state.last_trace:
                if "→" in step:
                    parts = step.split("→")
                    formatted_step = f"<span class='agent-name'>{parts[0].strip()}</span> <span style='color:white'>→</span> <span class='agent-action'>{parts[1].strip()}</span>"
                else:
                    formatted_step = step
                st.markdown(f"<div class='agent-trace'>{formatted_step}</div>", unsafe_allow_html=True)

    st.title("👨‍💼 Multi-Agent Employee Intelligence")
    st.caption(f"Authenticated as: **{st.session_state.current_user['name']}**")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    query = st.chat_input("Ask a question about employees, departments, or request exports...")

    if query:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.markdown(query)

        # ------------------------
        # INPUT GUARD
        # ------------------------

        guardrail = validate_input(
            query,
            st.session_state.current_user
        )

        if not guardrail["allowed"]:

            response = f"""
🛑 Guardrails AI Blocked Request

Reason:
{guardrail["reason"]}
"""

            with st.chat_message("assistant"):
                st.markdown(response)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.stop()

    # ------------------------
    # GRAPH
    # ------------------------

        with st.chat_message("assistant"):

            with st.spinner("Agents are collaborating..."):

                input_state = {
                    "user_query": query,
                    "current_user": st.session_state.current_user,
                    "employee_name": st.session_state.get("last_employee"),
                    "department_name": st.session_state.get("last_dept"),
                    "trace": []
                }

                result = graph.invoke(input_state)
                print("\n===== GRAPH RESULT KEYS =====")
                print(result.keys())
                print("============================\n")

                if result.get("employee_name"):
                    st.session_state.last_employee = result["employee_name"]

                if result.get("department_name"):
                    st.session_state.last_dept = result["department_name"]

                st.session_state.last_trace = result.get("trace", [])

                response = result.get(
                    "analysis",
                    "✅ Action completed."
                )
                context = f"""
Employee Data:
{result.get("employee_data")}

Department Statistics:
{result.get("department_stats")}

Organization Data:
{result.get("organization_data")}

Team Data:
{result.get("team_data")}

Promotion Candidates:
{result.get("promotion_candidates")}
"""
            # ------------------------
            # OUTPUT GUARD
            # ------------------------

                guardrail = validate_output(
                    response,
                    context
                )

                if guardrail["allowed"]:

                    response = guardrail.get("response", response)
                else:
                
                    response = f"""
                    🛑 Guardrails AI Blocked Response

Reason:
{guardrail.get("reason", "Unknown")}

Sanitized Output:

{guardrail.get("response", "No sanitized response available")}
"""

                st.markdown(response)

                if result.get("excel_path"):

                    with open(result["excel_path"], "rb") as file:

                            st.download_button(
                                label="📥 Download Excel Report",
                                data=file,
                                file_name=result["excel_path"].split("/")[-1],
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )