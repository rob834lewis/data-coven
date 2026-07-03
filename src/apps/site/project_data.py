from dataclasses import dataclass


@dataclass
class Project:
    name: str
    slug: str
    description: str
    technologies: list[str]
    live_url: str | None = None
    github_url: str | None = None


PROJECTS = [
    Project(
        name="Finance Ferret",
        slug="finance-ferret",
        description="A Flask app for teaching children how to manage pocket money, savings goals and spending choices.",
        technologies=["Python", "Flask", "PostgreSQL", "SQLAlchemy"],
        live_url=None,
        github_url=None,
    ),
    Project(
        name="Coffee App",
        slug="coffee-app",
        description="A small data app demonstrating batch, streaming and on-demand data processing patterns.",
        technologies=["Python", "Flask", "SQLite", "Dashboards"],
        live_url=None,
        github_url=None,
    ),
    Project(
        name="Exchange Rates ETL",
        slug="exchange-rates-etl",
        description="An ETL pipeline that extracts ECB exchange rates, validates the data and loads it into cloud databases.",
        technologies=["Python", "PostgreSQL", "BigQuery", "Cloud Scheduler"],
        live_url=None,
        github_url=None,
    ),
]