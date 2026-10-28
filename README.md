# AssignGame — The Missing Moonstone

A Python + Streamlit detective-game skeleton. Interview three suspects, examine evidence, and make a final accusation.

## Run

Requires Python 3.10 or newer.

```bash
cd /workspace/AssignGame  # Or your local checkout directory
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

The default **Demo (scripted)** mode needs no credentials. It previews the interface using fixed responses and does **not** meet the runtime AI assessment requirement.

## Enable live AI

This starter uses the OpenAI API. Supply `DETECTIVE_API_KEY` securely in the server environment, restart Streamlit, and select **Live AI**. Optionally set `DETECTIVE_MODEL` (default `gpt-4.1-mini`) to a compatible model your account can access. API access and billing are separate from a ChatGPT subscription.

`.env.example` documents the variables; the app does not automatically load `.env` files. Never commit keys or enter them into game questions. The API key stays on the server. Live requests require HTTPS access to `api.openai.com`.

AI generates dialogue from the player's question, the suspect's background, and recent conversation. Each suspect has separate history. Clues, culprit, and verdict are fixed so the case remains solvable. Prompts constrain dialogue, but consistency needs live testing. API failures preserve progress and show a retry message; live mode never silently substitutes demo responses.

## Project structure

- `app.py`: interface, session state, and interaction flow.
- `game.py`: case facts, input validation, and verdict logic.
- `ai.py`: demo dialogue and replaceable AI integration.
- `tests/test_app.py`: automated interface checks without real API calls.

## Validate and demonstrate

```bash
.venv/bin/python -m unittest discover -s tests -v
```

For evaluation, enable Live AI, ask Blair what they saw, ask Alex about the blue case, then accuse Alex and show the verdict. Explain how `ai.py` generates dialogue from player input. Also test empty input, a wrong accusation, and an API failure. Automated checks do not validate the live provider; complete a real AI interview before claiming the integration works.

This skeleton exposes all clues immediately. Extend it by unlocking clues through interviews, adding cases, or checking dialogue for contradictions. Switching modes or restarting clears the investigation. Progress lives in the Streamlit session, not a database.
