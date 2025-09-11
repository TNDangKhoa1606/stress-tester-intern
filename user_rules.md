# Workflow Guidelines

*These guidelines apply to any AI assistant (e.g., Google Gemini, Anthropic Claude, OpenAI ChatGPT, DeepSeek, Sonama, OpenRouter) and are not specific to a single model. They ensure a consistent, safe, and effective workflow across different AI platforms when assisting with code tasks.*

**Addressing (Xưng hô):** In Vietnamese-language interactions, the user (Anh 2) addresses the assistant as **"em"**, and the assistant (em) should address the user as **"Anh 2"** for respectful communication.

Always follow the workflow:

**Plan → Confirm → Apply → Verify**

---

## 1. Planning
- Clearly state:
  - Goal of the change  
  - Possible risks  
  - Affected files  
  - Estimated size of change  
  - Acceptance criteria (use **Given/When/Then** or equivalent)  

- Always specify:
  - Exact file path from `<REPO_ROOT>`  
  - Precise location for edits (e.g., before/after a method, line number, or inside a block)  
  - Sufficient detail so the assistant is not forced to guess any requirements or context  

- Provide context about:
  - Tech stack and environment  
  - Dependencies or frameworks involved  
  - Required configuration or variables  
  - Any compatibility considerations with the specified environment  

- If any requirement or detail is unclear, **ask for clarification** before proceeding (do not make assumptions).

---

## 2. Code Changes
- Keep existing formatting and comments intact.  
- Follow the project’s established coding style and linter/formatter rules.  
- Do not arbitrarily rename variables, methods, or classes (avoid unnecessary diffs).  
- Do not hardcode secrets or sensitive data:  
    - Use environment variables or configuration files for credentials and keys.  
- Apply secure coding practices by default:  
    - Parameterized queries (to prevent SQL injection, etc.)  
    - Input validation and sanitization  
    - Proper output escaping  
    - No sensitive data in logs or error messages  
- Ensure changes are efficient and optimized (avoid introducing performance bottlenecks).

---

## 3. Testing
- For every change, include or suggest relevant tests:  
  - Unit tests for individual components  
  - Integration tests for how components work together  
  - Manual testing steps for QA if applicable  
- Show that acceptance criteria are met through tests or examples of expected output.  
- Include tests for edge cases and failure scenarios to ensure robustness.  
- If modifying hot paths (critical sections of code):  
  - Provide performance budgets or benchmarks (e.g., latency, memory usage limits).  
  - Indicate how to measure and verify the performance impact.

---

## 4. Version Control
- Respect the version control workflow and policies:  
  - Specify the target branch for the changes.  
  - Follow commit message conventions (e.g., **Conventional Commits** style).  
  - Prepare a patch/diff and display it for review before committing.  
- Write clear and descriptive commit messages explaining what and why.  
- Do not commit without explicit approval:  
  - If approval is pending, keep changes in a local branch or draft.  
- Break down large modifications into small, reviewable commits or merge requests.  
- Never request too many files or lines of code at once (avoid overloading the review or the AI's context window).  
- If the change affects a public API or database schema:  
  - Plan for a migration and/or rollback strategy.  
  - Document any breaking changes for users.

---

## 5. Dependencies
- When proposing new dependencies, specify clearly:  
  - License (ensure it's compatible with the project)  
  - Size or impact on build/package  
  - Maintenance status (popularity, last update)  
  - Security implications (any known vulnerabilities)  
- Consider if the new dependency is truly necessary or if existing libraries/standard functions can achieve the same result (avoid adding bloat).

---

## 6. Logging & Error Handling
- Always show the code diff and explain the reasoning before applying changes (for transparency in review).  
- Use structured logging for any new log statements (e.g., JSON or key-value format) for consistency.  
- Maintain consistent error handling patterns (use the project's error models or conventions).  
- Ensure error handling is robust and prevents crashes or undefined behavior.  
- Avoid logging sensitive information (user data, secrets) in any logs or error messages.

---

## 7. Approval Flow
- Each step **must wait for explicit approval** from the reviewer/user before moving forward to the next.  
- Do not proceed from planning to coding, coding to testing, or testing to committing without confirmation.  
- Clearly mark points where approval is needed, and pause for feedback.
