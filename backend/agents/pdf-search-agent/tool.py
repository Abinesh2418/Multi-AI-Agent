from crewai_tools import PDFSearchTool

pdf_search_tool = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="groq",
            config=dict(
                model="llama-3.3-70b-versatile",
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="sentence-transformers/all-MiniLM-L6-v2",
            ),
        ),
    )
)
