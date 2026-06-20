# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
search_listings takes in attributes (e.g., size, price, clothing category) and returns 3 matching listings from listings.json sorted by relevance. 

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): describes what clothing  user is looking for by using its category/type/aesthetic. 
- `size` (str): represents the size of the clothing user is looking for
- `max_price` (float): represents the maximum price user is willing to pay for clothing

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
Return 3 matching listing sorted by relevance. Each listing is represented as a string formatted as "[Title]- $[Price], [Platform], [Condition]".

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
If no listing match, the agent should reason again what to do- either stop or provide other options that may interest the user- and report that no listings were found for the original user request. 
---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
suggest_outfit returns clothing items in wardrobe_schema.json that will complement the clothing returned by search_listings. The tool also explains how to style the clothings as well (e.g., rolling sleeves).

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): is the item FitFinder suggests using search_listings
- `wardrobe` (dict): is a list of items in the user's wardrobe 

**What it returns:**
<!-- Describe the return value -->
returns a string with an outfit suggestion. 

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
In the case of an error, the agent should provide general outfit suggestions. 
---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
It generates a social media caption that describes the outfit. 

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (...): is the string of the outfit returned by suggest_outfit

**What it returns:**
<!-- Describe the return value -->
It returns a string which is the social media caption.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
In the case of an error, return a string that says there was an error. 
---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
Takes user request and extracts relevant data that describe what the user is looking for and creates a structured query. Then the model calls search_listings() using extracted data and conveys the top matched result. In the case of no results, the model recommends other styles, price ranges, etc. that are similar to the original request and asks for user approval to repeat the search_listings() loop or stop the search. If FitFinder finds a listing, the agent calls suggest_outfit() and FitFinder returns a string that suggests pairings for the new item in user's wardrobe to create an outfit. If user's wardrobe is empty, the Fitfinder returns a general outfit suggestion. Lastly, once FitFinder successful suggests an outfit, FitFinder generates a social media caption that is short but descriptive of the outfit. 
---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | tells user to try differently and stops |
| suggest_outfit | Wardrobe is empty | suggests a general outfit |
| create_fit_card | Outfit input is missing or incomplete | return a descriptive error message |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->
User query
    │
    ▼
Planning Loop ───────────────────────────────────────────┐
    │                                                    │
    ├─► search_listings(description, size, max_price)    │
    │       │ results=[]                                 │
    │       ├──► [ERROR] "No listings found..." → return │
    │       │                                            │
    │       │ results=[item, ...]                        │
    │       ▼                                            │
    │   Session: selected_item = results[0]              │
    │       │                                            │
    ├─► suggest_outfit(selected_item, wardrobe)          │
    │       │                                            │
    │   Session: outfit_suggestion = "..."               │
    │       │                                            │
    └─► create_fit_card(outfit_suggestion, selected_item)│
            │                                            │
        Session: fit_card = "..."                        │
            │                                            └─ error path returns here
            ▼
        Return session
---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
The agent calls search_listings to find relevant listings in listing.json.

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
The agent calls suggest_outfit using output of search_listings to create an outfit suggestion. 

**Step 3:**
<!-- Continue until the full interaction is complete -->
The agent calls create_fit_card to generate a social media caption that describes the outfit. 

**Final output to user:**
<!-- What does the user actually see at the end? -->
The user sees what FitFinder finds in listings, picks as an outfit, and writes as a caption. 