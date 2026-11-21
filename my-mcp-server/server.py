"""
A simple MCP server that provides time-related tools.
This demonstrates the basic structure of an MCP server in Python using FastMCP.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server.mcpserver import MCPServer

# Create the MCP server instance
mcp = MCPServer("time-tools")


@mcp.tool()
def get_current_time(timezone: str = "UTC") -> str:
    """
    Returns the current time in a specified timezone.
    
    Use this when the user asks what time it is, or needs to know
    the time in a specific location.
    
    Args:
        timezone: IANA timezone name (e.g., 'America/New_York', 'Asia/Tokyo').
                  Use 'UTC' for universal time. Defaults to UTC.
    
    Common timezones: UTC, America/New_York, America/Los_Angeles,
    Europe/London, Asia/Tokyo, Asia/Singapore.
    """
    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception:
        return f"Error: Invalid timezone '{timezone}'. Use IANA timezone names like 'America/New_York' or 'Asia/Tokyo'."


@mcp.tool()
def convert_time(time: str, from_timezone: str, to_timezone: str) -> str:
    """
    Converts a time from one timezone to another.
    
    Use this when the user wants to know what time it will be
    in one place when it's a specific time in another place.
    
    Args:
        time: Time in HH:MM format (24-hour), e.g., '14:30'
        from_timezone: Source timezone (IANA name)
        to_timezone: Target timezone (IANA name)
    """
    try:
        hour, minute = map(int, time.split(":"))
        from_tz = ZoneInfo(from_timezone)
        to_tz = ZoneInfo(to_timezone)
        
        today = datetime.now().date()
        dt_from = datetime(today.year, today.month, today.day, hour, minute, tzinfo=from_tz)
        dt_to = dt_from.astimezone(to_tz)
        
        return (
            f"{time} in {from_timezone} is {dt_to.strftime('%H:%M')} in {to_timezone}\n"
            f"(Full: {dt_to.strftime('%Y-%m-%d %H:%M:%S %Z')})"
        )
    except ValueError:
        return f"Error: Invalid time format. Use HH:MM (24-hour), e.g., '14:30'"
    except Exception as e:
        return f"Error: {str(e)}. Make sure timezone names are valid IANA names."


if __name__ == "__main__":
    mcp.run()
