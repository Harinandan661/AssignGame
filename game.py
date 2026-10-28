"""Fixed facts and rules; extend these to design your own case."""

TITLE = "The Missing Moonstone"
BRIEF = "At 8:15 pm, the museum's Moonstone vanished. Interview suspects, examine evidence, and make an accusation."
EVIDENCE = [
    "The display was opened with a staff key at 8:12 pm; its lock was undamaged.",
    "The east-hall camera shows Alex carrying a blue case away at 8:13 pm.",
    "A blue case containing the Moonstone was found in Alex's assigned locker.",
]
SUSPECTS = {
    "Alex": {
        "role": "Museum technician",
        "facts": "You had a staff key and carried a blue equipment case through the east hall at 8:13 pm. You claim you were fixing lights. You are evasive about your locker.",
        "demo": "I was fixing the lights. That blue case was for my equipment.",
    },
    "Blair": {
        "role": "Security guard",
        "facts": "You were at reception from 8:00 to 8:20 pm. You saw Alex carrying a blue case through the east hall. You did not witness the theft.",
        "demo": "I was at reception. I saw Alex heading through the east hall.",
    },
    "Casey": {
        "role": "Visiting researcher",
        "facts": "You were in the reading room and had no staff key. Earlier, Alex mentioned repairing the display lights. You did not witness the theft.",
        "demo": "I don't have a staff key. Alex mentioned repairing the lights.",
    },
}
CULPRIT = "Alex"
EXPLANATION = "Alex used the staff key, carried the Moonstone in the blue case, and hid it in their locker. The key record, camera sighting, and recovered stone establish the solution."


def validate_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Enter a question before interviewing a suspect.")
    if len(question) > 500:
        raise ValueError("Keep your question to 500 characters or fewer.")
    return question


def accuse(suspect: str) -> bool:
    if suspect not in SUSPECTS:
        raise ValueError("Choose one of the three suspects.")
    return suspect == CULPRIT
