from graph.graph_builder import build_graph

graph = build_graph()

result = graph.invoke(
    {
        "user_query":
        "Should John Doe be promoted?"
    }
)

print(result["analysis"])