from lxml import html
from lxml.html import HtmlElement

def to_pdgalive_link(event_id: int) -> str:
    return f"https://www.pdga.com/apps/tournament/live/event?eventId={event_id}"

def try_parse_hole_data(hole_elements: list[HtmlElement], num_holes: int, default: int, drop_last=True) -> list[int]:
    if hole_elements == []:
        return [default for _ in range(num_holes)]
    try:
        if drop_last:
            return [int(x.text) for x in hole_elements[:-1]]
        else:
            return [int(x.text) for x in hole_elements]
    except:
        return [default for _ in range(num_holes)]
    