from fastmcp import FastMCP
import tools

mcp = FastMCP()

# Register Tools
tools.register_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
