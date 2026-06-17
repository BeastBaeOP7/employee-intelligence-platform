from config.github_models_llm import get_llm

llm = get_llm()

def analysis_agent(state):
    query = state["user_query"]
    employee = state.get("employee_data")
    stats = state.get("department_stats")
    team_data = state.get("team_data")
    org_data = state.get("organization_data")
    promotion_candidates = state.get("promotion_candidates")
    excel_path = state.get("excel_path")

    prompt = f"""
You are an AI Employee Analytics Assistant.

Your responsibilities:
1. Explain employee profiles.
2. Answer salary-related questions.
3. Handle manager and team-level queries.
4. Compare data with department/organization averages.
5. Evaluate promotion readiness and list candidates.
6. Provide recursive organization hierarchies.
7. Deliver organization-wide executive insights (department breakdown, heads, etc).

Context Data:
- Employee Data: {employee}
- Department Statistics (Specific): {stats}
- Organization-Wide Data (All Depts): {org_data}
- Team/Hierarchy Data: {team_data}
- Promotion Candidates: {promotion_candidates}

Instructions:
- If asked "Show all department statistics", use 'organization_data.department_stats'.
- If asked "Who are the department heads?", use 'organization_data.heads'.
- If asked about "Promotion analysis" or "ready for promotion", use 'promotion_candidates'.
- If asked about a team or hierarchy, use the 'full_hierarchy' tree provided in Team/Hierarchy Data.
- Be professional, concise, and highly accurate. NEVER fall back to "I don't have access" if the data is present in the context above.

User Query:
{query}
"""

    response = llm.invoke(prompt)
    
    analysis_text = response.content
    
    # Append the hierarchy tree directly if requested and available for visual clarity
    if team_data and "full_hierarchy" in team_data and ("team" in query.lower() or "hierarchy" in query.lower() or "report" in query.lower()):
        analysis_text += f"\n\n**Organization Hierarchy:**\n```\n{team_data['full_hierarchy']}\n```"

    if excel_path:
        analysis_text += f"\n\n📎 **Excel Report Generated:** `{excel_path}`"

    trace = state.get("trace", [])
    trace.append("Analysis Agent → Generated final response with requested analytics and hierarchy.")

    return {
        "analysis": analysis_text,
        "trace": trace
    }