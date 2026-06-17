import streamlit as st
from graph.graph_builder import build_graph
from database.database import SessionLocal
from database.models import Employee

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

# Helper to get all employees for selection
def get_all_employees():
    db = SessionLocal()
    try:
        return db.query(Employee).all()
    finally:
        db.close()

employees = get_all_employees()
employee_options = {f"{e.name} ({e.role})": e for e in employees}

# Sidebar - User Selection & Trace
with st.sidebar:
    st.title("🔐 Authentication")
    selected_name = st.selectbox(
        "Select Current User (Identity Simulation)",
        options=list(employee_options.keys()),
        index=0
    )
    current_employee = employee_options[selected_name]
    st.session_state.current_user = {
        "employee_id": current_employee.employee_id,
        "name": current_employee.name,
        "role": current_employee.role,
        "department": current_employee.department
    }
    
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

st.title("🏢 Multi-Agent Employee Intelligence")
st.caption(f"Logged in as: **{current_employee.name}** | Role: **{current_employee.role}** | Dept: **{current_employee.department}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Chat Input
query = st.chat_input(
    "Ask a question about employees, departments, or request exports..."
)

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Agents are collaborating..."):

            # Prepare state for graph
            input_state = {
                "user_query": query,
                "current_user": st.session_state.current_user,
                "employee_name": st.session_state.get("last_employee"),
                "department_name": st.session_state.get("last_dept"),
                "trace": []
            }

            # Execute Graph
            result = graph.invoke(input_state)

            print(result)

            # Update Context
            if result.get("employee_name"):
                st.session_state.last_employee = result["employee_name"]

            if result.get("department_name"):
                st.session_state.last_dept = result["department_name"]

            # Store trace
            st.session_state.last_trace = result.get(
                "trace",
                []
            )

            # Display response
            response = result.get(
                "analysis",
                "✅ Report generated successfully."
            )

            st.markdown(response)

            # Excel Download Button
            if result.get("excel_path"):

                excel_file = result["excel_path"]

                st.success(
                    "✅ Excel report generated successfully!"
                )

                with open(excel_file, "rb") as file:

                    st.download_button(
                        label="📥 Download Excel Report",
                        data=file,
                        file_name=excel_file.split("/")[-1],
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            # Update Trace Sidebar
            with trace_container:

                for step in st.session_state.last_trace:

                    if "→" in step:

                        parts = step.split("→")

                        formatted_step = (
                            f"<span class='agent-name'>{parts[0].strip()}</span> "
                            f"<span style='color:white'>→</span> "
                            f"<span class='agent-action'>{parts[1].strip()}</span>"
                        )

                    else:
                        formatted_step = step

                    st.markdown(
                        f"<div class='agent-trace'>{formatted_step}</div>",
                        unsafe_allow_html=True
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
