"""Test interaction and recovery without network requests."""

import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from ai import AIUnavailable

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class GameFlowTests(unittest.TestCase):
    def test_demo_interview_verdict_and_restart(self):
        app = AppTest.from_file(APP).run()
        self.assertFalse(app.exception)
        app.text_input[0].set_value("Where were you?")
        next(b for b in app.button if b.label == "Ask suspect").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.chat_message), 2)
        app.checkbox[0].check()
        next(b for b in app.button if b.label == "Make accusation").click().run()
        self.assertIn("Case solved", app.success[0].value)
        self.assertTrue(app.text_input[0].disabled)
        next(b for b in app.button if b.label == "Restart investigation").click().run()
        self.assertEqual(len(app.chat_message), 0)
        self.assertEqual(len(app.success), 0)
        self.assertFalse(app.text_input[0].disabled)

    def test_invalid_input_and_wrong_accusation(self):
        app = AppTest.from_file(APP).run()
        next(b for b in app.button if b.label == "Ask suspect").click().run()
        self.assertIn("Enter a question", app.error[0].value)
        next(b for b in app.button if b.label == "Make accusation").click().run()
        self.assertIn("Confirm", app.error[0].value)
        app.selectbox[1].select("Blair")
        app.checkbox[0].check()
        next(b for b in app.button if b.label == "Make accusation").click().run()
        self.assertIn("evidence points to Alex", app.error[0].value)

    def test_ai_error_preserves_progress(self):
        app = AppTest.from_file(APP).run()
        app.radio[0].set_value("Live AI").run()
        with patch("ai.interview", return_value="I was in the east hall."):
            app.text_input[0].set_value("Where were you?")
            next(b for b in app.button if b.label == "Ask suspect").click().run()
        self.assertEqual(len(app.chat_message), 2)
        with patch("ai.interview", side_effect=AIUnavailable("Please try again.")):
            app.text_input[0].set_value("What were you carrying?")
            next(b for b in app.button if b.label == "Ask suspect").click().run()
        self.assertFalse(app.exception)
        self.assertIn("Please try again", app.error[0].value)
        self.assertEqual(len(app.chat_message), 2)


if __name__ == "__main__":
    unittest.main()
