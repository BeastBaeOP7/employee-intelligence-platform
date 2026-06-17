from graph.graph_builder import build_graph

graph = build_graph()

result = graph.invoke(
    {
        "employee_id": 101,
        "question": "Is this employee paid above average?"
    }
)

print(result["analysis"])