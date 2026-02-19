import importlib.util
import sys
from pathlib import Path
from crewai import Crew, Process

import backend.config.settings  # noqa: F401 — triggers env var loading

AGENTS_DIR = Path(__file__).resolve().parent / "agents"

AGENT_CONFIGS = {
    "web-search-agent": {
        "agent_var": "web_search_agent",
        "task_factory": "create_web_search_task",
    },
    "file-reader-agent": {
        "agent_var": "file_reader_agent",
        "task_factory": "create_file_reader_task",
    },
    "file-writer-agent": {
        "agent_var": "file_writer_agent",
        "task_factory": "create_file_writer_task",
    },
    "pdf-search-agent": {
        "agent_var": "pdf_search_agent",
        "task_factory": "create_pdf_search_task",
    },
    "csv-rag-agent": {
        "agent_var": "csv_rag_agent",
        "task_factory": "create_csv_rag_task",
    },
    "scrape-agent": {
        "agent_var": "scrape_agent",
        "task_factory": "create_scrape_task",
    },
    "google-search-agent": {
        "agent_var": "google_search_agent",
        "task_factory": "create_google_search_task",
    },
    "shopping-agent": {
        "agent_var": "shopping_agent",
        "task_factory": "create_shopping_task",
    },
    "serper-search-agent": {
        "agent_var": "serper_search_agent",
        "task_factory": "create_serper_search_task",
    },
}


def _load_module_from_path(module_name: str, file_path: Path):
    """Load a Python module from an absolute file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_agent_package(agent_type: str):
    """Load the __init__, tool, agent, and task modules for a hyphenated agent directory."""
    agent_dir = AGENTS_DIR / agent_type
    safe_name = agent_type.replace("-", "_")
    pkg_name = f"backend.agents.{safe_name}"

    init_path = agent_dir / "__init__.py"
    if init_path.exists() and pkg_name not in sys.modules:
        init_mod = _load_module_from_path(pkg_name, init_path)
        init_mod.__path__ = [str(agent_dir)]
        init_mod.__package__ = pkg_name

    for sub in ("tool", "agent", "task"):
        full_name = f"{pkg_name}.{sub}"
        if full_name not in sys.modules:
            _load_module_from_path(full_name, agent_dir / f"{sub}.py")

    return sys.modules[f"{pkg_name}.agent"], sys.modules[f"{pkg_name}.task"]


def get_available_agents() -> list[str]:
    return list(AGENT_CONFIGS.keys())


def run_crew(agent_type: str, query: str) -> str:
    if agent_type not in AGENT_CONFIGS:
        raise ValueError(
            f"Unknown agent type '{agent_type}'. "
            f"Available agents: {get_available_agents()}"
        )

    config = AGENT_CONFIGS[agent_type]
    agent_mod, task_mod = _load_agent_package(agent_type)

    agent = getattr(agent_mod, config["agent_var"])
    task_factory = getattr(task_mod, config["task_factory"])
    task = task_factory(query)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
