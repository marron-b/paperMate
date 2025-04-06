import mcp
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import UserMessage, AssistantMessage, Message

mcp = FastMCP("PaperResearcher")


@mcp.prompt(
    name="find_similar_papers_by_keyword",
    description="""
        Searches for academic research papers based on a given keyword or query.
        Returns relevant and recent papers from trusted academic databases such as 
        IEEE, ACM, Springer, Elsevier.
        """,
)
def find_similar_papers_by_keyword(keyword: str) -> list[Message]:
    return [
        AssistantMessage(
            """You are an expert in academic research discovery. 
            Based on the user's provided keyword, find the most practically relevant, 
            recent, and high-quality academic papers 
            that could inform technology strategy or 
            decision-making in a real-world tech company context.
            Search trusted databases such as IEEE, ACM, Springer or Elsevier. 
            Prioritize papers that:
                * Are published within the past 3 years (2022–2025)
                * Are peer-reviewed and from well-regarded journals or conferences
                * Include real-world case studies, industry data, 
                    or actionable frameworks
                * Have high relevance to technology adoption, innovation management, 
                    strategic planning, or technical operations in industry
            For each paper, return:
                * Title
                * Authors
                * Publication year
                * Journal or conference name
                * DOI or direct link
                * A concise 1–2 sentence summary 
                    focusing on its key practical contribution or industry relevance
            Please prioritize papers with clear business or engineering applications."""
        ),
        UserMessage(
            f"Please find academic research papers related to the keyword: {keyword}"
        ),
    ]


@mcp.prompt(
    name="recommend_related_papers",
    description="""
        Recommends academic research papers related to a given paper title. 
        Suggestions are based on similar topics or research methods, and focus on 
        papers published in the past 3 years (from 2025). Results include metadata 
        such as title, authors, publication year, journal/conference, and DOI or link.
        """,
)
def recommend_related_papers(title: str, related_papers: list[dict]) -> list[Message]:
    messages = [
        AssistantMessage(
            """
            You are an expert in academic paper recommendation. 
            Based on the provided paper title, recommend academic papers 
            that are closely related in topic, methodology, or strategic application.
            Focus on papers that:
                * Were published within the last 3 years (2022–2025)
                * Come from reliable and peer-reviewed academic sources 
                    such as IEEE, ACM, Springer or Elsevier.
                * Demonstrate practical relevance to technology strategy, 
                    innovation management, or real-world technology deployment
                * Share common frameworks, research approaches, 
                    or application domains with the original paper
            For each recommended paper, please include:
                * Title
                * Authors
                * Publication year
                * Journal or conference name
                * DOI or direct link
                * A concise 1–2 sentence summary focusing on its main contribution 
                    and how it relates to the original paper
            Please prioritize papers with strong practical or strategic relevance.
            """
        ),
        UserMessage(
            f"""
            Please recommend research papers 
            related to the following paper: '{title}'
            """
        ),
    ]

    for paper in related_papers:
        messages.append(
            AssistantMessage(
                f"📄 **Title**: {paper['title']}\n"
                f"🔗 **DOI or Link**: {paper['doi']}\n"
            )
        )

    return messages
