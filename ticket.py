def create_mock_ticket(user_name: str, email: str, summary: str, description: str):
    print("==== SUPPORT TICKET CREATED ====")
    print(f"Name: {user_name}")
    print(f"Email: {email}")
    print(f"Summary: {summary}")
    print(f"Description: {description}")
    print("Ticket would be sent to Jira (mocked).")
