import pyautogui
import pyperclip
import time
import webbrowser
import re

def fetch_problem_statement(contest_id: str, problem_index: str, sleep_time: int) -> str | None:
    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
    webbrowser.open(url)
    time.sleep(sleep_time)
    def wait_until_problem_ready(timeout=10, interval=0.2):
        previous_text = ""
        start_time = time.time()
        while time.time() - start_time < timeout:
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "c")
            current_text = pyperclip.paste()
            if current_text != previous_text and "Invocation" in current_text and "Codeforces (c)" in current_text:
                return current_text
            previous_text = current_text
            time.sleep(interval)
        return ""
    raw_clipboard = wait_until_problem_ready()
    pyautogui.hotkey("ctrl", "w")
    if not raw_clipboard:
        return None
    start_marker = "Invocation"
    end_marker = "Codeforces (c)"
    start = raw_clipboard.find(start_marker)
    end = raw_clipboard.find(end_marker)
    if start == -1 or end == -1 or end <= start:
        return None
    return raw_clipboard[start + len(start_marker):end].strip()

def extract_submission_ids(contest_id: str, problem_letter: str, lang_index: int, sleep_time: int) -> list:
    url = f"https://codeforces.com/contest/{contest_id}/status?order=BY_CONSUMED_TIME_ASC"
    webbrowser.open(url)
    time.sleep(sleep_time)
    pyautogui.hotkey("ctrl", "f")
    pyperclip.copy("Status Filter")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("esc")
    pyautogui.press("tab")
    offset = ord(problem_letter.upper()) - ord("A")
    pyautogui.press("right", presses=offset + 1)
    pyautogui.press("tab")
    pyautogui.press("right")
    pyautogui.press("tab")
    if lang_index > 0:
        pyautogui.press("right", presses=lang_index)
    pyautogui.press("tab", presses=4)
    pyautogui.press("enter")
    time.sleep(sleep_time)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    pyautogui.hotkey("ctrl", "w")
    time.sleep(0.5)
    content = pyperclip.paste()
    if not content:
        return []
    submission_ids = re.findall(r'(?<=\n)(\d{9})(?=\s)', content)
    return list(dict.fromkeys(submission_ids))

def get_code_from_submission(contest_id: str, submission_id: str, sleep_time: int) -> str | None:
    url = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"
    webbrowser.open(url)
    time.sleep(sleep_time)
    def wait_until_code_ready(timeout=8, interval=0.1):
        previous_text = ""
        start_time = time.time()
        while time.time() - start_time < timeout:
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "c")
            current_text = pyperclip.paste()
            if current_text != previous_text and "→ Source" in current_text and "Click to see test details" in current_text:
                return current_text
            previous_text = current_text
            time.sleep(interval)
        return ""
    clipboard_text = wait_until_code_ready()
    pyautogui.hotkey("ctrl", "w")
    if not clipboard_text:
        return None
    start_marker = "→ Source"
    end_marker = "Click to see test details"
    start = clipboard_text.find(start_marker)
    end = clipboard_text.find(end_marker)
    if start == -1 or end == -1 or end <= start:
        return None
    code = clipboard_text[start + len(start_marker):end].strip()
    return code[len("Copy"):].strip() if code.startswith("Copy") else code