# Feature: AI Chat (Tool Functions + LLM Wiring)

## Prompt
Asked the AI to build the four tool functions first (count_tickets,
get_ticket_by_id, get_tickets_by_assignee, get_pending_tickets), tested
directly against MySQL before adding any LLM integration — per the
tool-calling-only decision from planning.

## Key AI output — tool functions
- `count_tickets(status=None, priority=None)` — dynamic WHERE clause.
- `get_ticket_by_id` — thin wrapper around the existing tickets.py function.
- `get_tickets_by_assignee(name)` — case-insensitive match via LOWER().
- `get_pending_tickets()` — explicitly defined as status IN (Open, In Progress).

## Verification (tools only, no LLM yet)
Ran a manual script confirming all four functions returned correct results
matching the live database (including a case-insensitivity check for
assignee lookups).

## LLM integration — provider changes (debugging history)
1. **Anthropic API (first attempt):** wired tool-calling loop successfully,
   but hit `401 authentication_error` — required paid API credits, which
   was not acceptable for this project.
2. **Google Gemini (second attempt):** switched to Gemini's automatic
   function-calling for simpler code. Hit a `.env` loading bug first
   (relative path issue, fixed with `Path(__file__).resolve().parent`),
   then discovered Gemini's free tier requires a billing account to be
   enabled for this account/region regardless of the "Free tier" label
   shown in Google AI Studio.
3. **Groq (final, working):** switched to Groq's OpenAI-compatible
   chat-completions API with manual tool-calling, since Groq's free tier
   requires no credit card. First model tried, `llama-3.3-70b-versatile`,
   returned `404 model_not_found` (deprecated). Switched to
   `openai/gpt-oss-120b`, confirmed by Groq's own docs to support tool use.
   This resolved the issue — AI chat confirmed working end-to-end.

## Key design points preserved across all three providers
- The LLM only ever receives data from the four defined tool functions —
  no text-to-SQL, no fallback path.
- Every tool call and final answer is printed to the terminal for
  debugging/demo evidence.
- `pages/3_AI_Chat.py` never needed to change across any provider switch,
  since it only calls `ai_chat.answer_question(question)`.

## Outcome
Working AI chat answering the assignment's example questions using live
MySQL data via Groq (`openai/gpt-oss-120b`) tool-calling.