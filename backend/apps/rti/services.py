# business logic for rti
def generate_rti_template(name, address, info_sought, public_authority):
    """
    Generates a simple RTI application text block dynamically.
    """
    return f"""
To,
The Public Information Officer,
{public_authority}

Subject: Application under RTI Act 2005

Dear Sir/Madam,
I, {name}, residing at {address}, seek the following information under Section 6(1) of the RTI Act 2005:

{info_sought}

Thanking You,
Yours faithfully,
{name}
Date: ___________
"""
