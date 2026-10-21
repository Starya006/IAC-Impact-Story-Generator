# IAC Impact Story Generator

**Project:** Automated Impact Story Generation of IAC Participants (IP-11760)
**Programme:** Cloud Counselage – Global Professional Internship (GPI), Generative AI
**Type:** Individual project, 120 hours

## Overview
A desktop prototype that turns a participant's experience details into a clear, readable impact story. It supports Cloud Counselage's IAC Vision 2030 goal of documenting and sharing participant impact without writing each story by hand.

The user fills in a short form, picks a format and point of view, and generates a story. The story appears in an editable preview so a human can review and correct it before saving or copying it. This follows the problem statement's requirement that AI augments, rather than replaces, genuine human stories.

## Features
- **Participant form** with three sections: participant details, experience and learning, and outcomes and reflection.
- **Three story formats:** Detailed Impact Story, Social Media Post, Partner or Grant Report.
- **Two points of view:** First person and Third person.
- **Two generation modes:**
  - *Gemini mode:* if a Gemini API key is entered, the story is written by the `gemini-2.5-flash` model. The prompt tells the model to use only the information provided and not to invent facts, statistics or outcomes.
  - *Basic fallback mode:* if no key is entered, or the Gemini call fails, a built-in template generator builds the story from the form fields. No external service is called.
- **Human review step:** the preview is editable, and every story ends with a reminder to check it and get participant approval before sharing.
- **Save and copy:** save the story as `.txt` or `.md`, or copy it to the clipboard.
- **Hints and clear form:** placeholder hints are not treated as real data, and the form can be reset in one click.
- **Keyboard shortcuts:** `Ctrl+Enter` generates the story and `Ctrl+S` saves it.

## Folder contents
| File | Purpose |
|---|---|
| `IAC_Impact_Story_Generator.py` | The prototype source code |
| `IAC_Impact_Story.txt` | Sample story produced by the prototype |
| `README.md` | This file |
| `requirements.txt` | Dependencies and setup notes |
| `WORKFLOW.md` | Workflow of the system |
| `Demo_Video.mp4` | Demo video (to be uploaded) |

## How to run
1. Install Python 3.8 or later. Tkinter must be available (see `requirements.txt`).
2. Open a terminal in this folder and run:
   ```
   python IAC_Impact_Story_Generator.py
   ```
3. Fill in the participant details.
4. Choose the story format and point of view.
5. (Optional) Enter a Gemini API key.
6. Click **Generate Impact Story**, or **Use Basic Fallback** to skip the AI service.
7. Review and edit the story in the preview.
8. Click **Save Story to File** or **Copy Story**.

## Getting a Gemini API key (optional)
Create a key in Google AI Studio and paste it into the "Gemini API Key" box. The key is masked on screen and is not saved to disk. Do not share your key or commit it to a public repository.

## Sample input and output
A sample result for a Generative AI Internship (4 weeks) is in `IAC_Impact_Story.txt`.

## Ethical use
- The AI is instructed to use only the details provided.
- Stories are drafts. A person must check them for accuracy and get the participant's approval before they are published.

## Current limitations
- Participant details are typed in by the user. The prototype does not yet pull data from LinkedIn posts or IAC review pages.
- One story is generated at a time.
- Output is saved as plain text or Markdown only.

## Possible future work
- Import participant data from LinkedIn posts and IAC internship and certification reviews.
- Generate stories in batches for many participants.
- Export to PDF or Word, and add more story formats.
- Add a sentiment and theme summary across many stories for grant reporting.
