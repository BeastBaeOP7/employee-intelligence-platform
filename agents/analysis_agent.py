from config.github_models_llm import get_llm

llm = get_llm()


def analysis_agent(state):
    print("\n========== ANALYSIS AGENT ==========")
    print(f"Query               : {state['user_query']}")
    print(f"Intents             : {state.get('intents')}")

    print("\nAvailable Context")
    print("------------------------------")
    print(f"Employee Data       : {'YES' if state.get('employee_data') else 'NO'}")
    print(f"Department Stats    : {'YES' if state.get('department_stats') else 'NO'}")
    print(f"Organization Data   : {'YES' if state.get('organization_data') else 'NO'}")
    print(f"Team Data           : {'YES' if state.get('team_data') else 'NO'}")
    print(f"Promotion Candidates: {'YES' if state.get('promotion_candidates') else 'NO'}")
    print("===================================")

    query = state["user_query"]
    employee = state.get("employee_data")
    stats = state.get("department_stats")
    team_data = state.get("team_data")
    org_data = state.get("organization_data")
    promotion_candidates = state.get("promotion_candidates")

    prompt = f"""
You are the Analysis Agent of an Employee Analytics System.

Your ONLY responsibility is generating a clear natural-language response.

You MUST ONLY use the data provided below.

Never invent employees.

Never invent salaries.

Never invent departments.

Never invent statistics.

Never assume missing information.

If some required information is missing, explicitly state that it is unavailable.

--------------------------------

AVAILABLE DATA

Employee Data:
{employee}

Department Statistics:
{stats}

Organization Statistics:
{org_data}

Team Information:
{team_data}

Promotion Candidates:
{promotion_candidates}

--------------------------------

RULES

1. Use ONLY the available data.

2. Do NOT fabricate values.

3. If a section is None, ignore it.

4. If the answer cannot be produced from the data,
say the information is unavailable.

5. Keep responses concise and professional.

--------------------------------

USER QUERY

{query}
"""

    response = llm.invoke(prompt)
    analysis_text = response.content.strip()
    print("\n[Analysis Agent]")
    print("Response generated successfully.")
    print(f"Response Length : {len(analysis_text)} characters")
    print("=" * 35)


    # Append the hierarchy tree directly if requested and available
    if (
        team_data
        and "full_hierarchy" in team_data
        and any(kw in query.lower() for kw in ["team", "hierarchy", "report"])
    ):
        analysis_text += f"\n\n**Organization Hierarchy:**\n```\n{team_data['full_hierarchy']}\n```"

    trace = state.get("trace", [])
    trace.append("Analysis Agent → Generated response "
                f"[Employee={'YES' if employee else 'NO'}, "
                f"Department={'YES' if stats else 'NO'}, "
                f"Organization={'YES' if org_data else 'NO'}, "
                f"Team={'YES' if team_data else 'NO'}, "
                f"Promotion={'YES' if promotion_candidates else 'NO'}]"
    )

    return {
        "analysis": analysis_text,
        "trace": trace,
    }