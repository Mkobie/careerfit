def make_ansi_hyperlink(text: str, url: str) -> str:
    """
    Returns a string that, in many modern terminals, appears as clickable text,
    always underlined. No color styling is applied.
    """
    ESC = "\033"
    BEL = "\007"

    # Terminal hyperlink sequences:
    #   Opening:  ESC ] 8 ; ; URL BEL
    #   Closing:  ESC ] 8 ; ; BEL
    hyperlink_open = f"{ESC}]8;;{url}{BEL}"
    hyperlink_close = f"{ESC}]8;;{BEL}"

    # ANSI styling for underlining
    underline_on = f"{ESC}[4m"
    style_off = f"{ESC}[0m"

    return f"{underline_on}{hyperlink_open}{text}{hyperlink_close}{style_off}"

def get_description_with_hyperlink(company: dict) -> str:
    """
    Prints the company's description, but adds a hyperlink around the company's name
    """

    link = company.get("website") or company.get("linkedin job page")

    description = company.get("description", "No description")
    company_name = company.get("name", "Unknown Company")

    if not link:
        return description
    else:
        linked_name = make_ansi_hyperlink(company_name, link)

        if description.startswith(company_name):
            updated_description = linked_name + description[len(company_name):]
        else:
            updated_description = f"{linked_name} {description}"

        return updated_description
