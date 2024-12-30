# GeoWise Agent

## Features

- **Local LLM** (Llama-based) 
- **Conversational Memory**: Keeps track of recent messages and context
- **Integrated Tools**:
  - `get_countries_by_name` (RESTCountries API)
  - `google_search` (Web search)

## AI Feature Roadmap (Priority)

1. **Knowledge Base / RAG**  
   - **What**: Store custom documents (like travel guides or Wikipedia data) in a vector store.  
   - **Why**: Provide richer, more detailed answers and citations beyond a quick API lookup.  
   - **How**: Use an embedding model to index documents, then retrieve relevant passages for the LLM to use during inference.

2. **AI Summaries & Reports**  
   - **What**: Generate structured summaries, bullet-point overviews, or short PDF reports about countries.  
   - **Why**: Useful for travelers, students, or decision-makers needing quick reference.  
   - **How**: Extend the existing prompt with instructions on how to summarize or format the output. Possibly chain it with a PDF or email tool.

3. **Semantic Search & Auto-Suggestions**  
   - **What**: Suggest possible queries or refine user requests in real-time.  
   - **Why**: Improves user experience, helps them find relevant info.  
   - **How**: Maintain a semantic index of common topics/queries. On each keystroke (in a front-end), compare against the index to present suggestions.

4. **Multilingual Support**  
   - **What**: Detect user input language and respond in the same language.  
   - **Why**: Expands usability globally.  
   - **How**: Use a small language detection model and either a multilingual Llama or dynamic translation via a third-party API.

5. **Enhanced Prompt Engineering**  
   - **What**: Add few-shot examples showcasing how to use each tool effectively.  
   - **Why**: Increases model’s reliability in calling the right tools.  
   - **How**: Provide 2-3 sample QA interactions within the system prompt or use prompt templates with clear instructions.


## Installation & Setup

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/muhammadarslanshahzad/geowise-agent.git
   cd geowise-agent
    ```

2. **Install Requirements**
    ```bash
        pip install -r requirements.txt
    ```

3. **Usage**
 - __Terminal__: 
    ```bash 
    python conversational_agent.py
    ```
 - __StreamLit UI__:
    ```bash 
        streamlit run app.py
    ```
 