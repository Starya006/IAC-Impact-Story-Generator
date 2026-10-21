# Workflow – IAC Impact Story Generator

## 1. High-level flow
```
Participant details (form)
        |
        v
Choose story format + point of view
        |
        v
Click "Generate Impact Story"
        |
        v
   API key entered? ---- No ----> Basic fallback generator (template)
        |                                   |
       Yes                                  |
        |                                   |
        v                                   |
Gemini (gemini-2.5-flash)                   |
   |            |                           |
 Success      Error / empty / offline       |
   |            |                           |
   |            +--> Basic fallback --------+
   |                                        |
   +------------------+---------------------+
                      v
        Story shown in editable preview
                      |
                      v
   Human review: check accuracy, edit, get participant approval
                      |
                      v
        Save to .txt/.md   or   Copy to clipboard
```

## 2. Steps in detail
| # | Step | What happens in the prototype |
|---|---|---|
| 1 | Enter details | The user enters name, programme, duration, activities, skills gained, challenges, achievements and reflection. Hint text is ignored if left unchanged. |
| 2 | Choose settings | Story format (Detailed Impact Story, Social Media Post, Partner or Grant Report) and point of view (First or Third person). |
| 3 | Validate | If every field is empty, the app asks for at least some information. |
| 4 | Pick the generator | With a Gemini API key the app calls Gemini. Without one, it uses the basic fallback. |
| 5 | Gemini request | The app builds a prompt from the form data. The prompt says to use only the information provided and not to invent facts, statistics or outcomes. It sends the prompt to the Gemini API (temperature 0.5, up to 1400 tokens). |
| 6 | Handle errors | On an API error, connection problem or empty reply, the app shows a warning and produces the story with the basic fallback. |
| 7 | Preview | The story appears in an editable text box, with a status message telling the user which generator was used. |
| 8 | Human review | The user checks the story, edits it, and confirms it with the participant. Every story ends with a review reminder. |
| 9 | Save or copy | The story is saved as `.txt` or `.md`, or copied to the clipboard. |
| 10 | Reset | "Clear Form" resets all fields, the preview, the API key and the settings, after confirmation. |

## 3. Modules in the code
| Part | Role |
|---|---|
| `basic_story()` | Builds a story from templates for the chosen format and point of view. Works offline. |
| `gemini_story()` | Builds the prompt, calls the Gemini REST API with `urllib`, and returns the text or raises a clear error. |
| `ImpactStoryApp` | The Tkinter interface: form cards, story settings, status bar, preview, and the buttons for generate, fallback, clear, save and copy. |
| `main()` | Creates the window and starts the app. |

## 4. How the prototype meets the problem statement
| Requirement | How it is addressed |
|---|---|
| Generate personalised impact stories | Each story is built from one participant's own details. |
| Ethical, accurate representation | The prompt forbids invented facts, and stories are drafts for review. |
| Human oversight before publication | The editable preview and the review reminder on every story. |
| Different types of impact (skills, confidence, outcomes) | Dedicated fields for skills, challenges, achievements and reflection. |
| Use for social media, grants and partner showcases | The Social Media Post and Partner or Grant Report formats. |
| Reduce manual effort | A story is generated in seconds from one form. |
