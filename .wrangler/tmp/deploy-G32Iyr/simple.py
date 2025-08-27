def on_fetch(request, env):
    return Response("Enhanced MCP Memory - Python Workers Active!", headers={
        "content-type": "text/plain"
    })