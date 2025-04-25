

def build_safe_prompt(origin, destination, days, include_flights, include_hotels, include_transport):
    if not destination or not destination.strip():
        return None

    prompt = f"Plan a {days}-day trip from {origin.strip()} to {destination.strip()}."
    if include_flights:
        prompt += " Include best flights."
    if include_hotels:
        prompt += " Include hotel options."
    if include_transport:
        prompt += " Include local transport suggestions."
    prompt += " Format the output in markdown with emojis and clear structure."
    return prompt
