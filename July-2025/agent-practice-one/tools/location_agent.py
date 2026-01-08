
from agents import function_tool
@function_tool
def get_location(location: str, region: str):
    """
    get the location which about user is asking
    """
    return f"you {location } is location in {region}"