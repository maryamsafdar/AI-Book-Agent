# import os
# import streamlit as st
# from typing import TypedDict, Annotated, List
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langgraph.graph import StateGraph, END
# from langchain_core.runnables.graph import MermaidDrawMethod
# from langchain_groq import ChatGroq # type: ignore
# from github import Github
# from dotenv import load_dotenv
# import markdown2

# # Load environment variables for API keys
# load_dotenv()
# os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# llm = ChatGroq( model="llama-3.1-70b-versatile", temperature=0)

# # Define the state that the agent will maintain
# class BookState(TypedDict):
#     messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
#     title: str
#     description: str
#     chapters: List[str]
#     content: dict

# # Setup the language model
# # llm = ChatOpenAI(model="gpt-4")

# # Prompts for generating Table of Contents and chapters
# toc_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an experienced book author. Create a detailed Table of Contents based on the book title: {title} and description: {description}."),
#     ("human", "Create a Table of Contents for my book."),
# ])

# chapter_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an expert in writing. Write a detailed chapter on {chapter} based on the given outline."),
#     ("human", "Write a chapter for my book.")
# ])

# # Streamlit User Interface
# st.title("AI Book Generator")
# st.write("Welcome to the AI Book Generator! Provide your book's title and description, and let the AI generate the content for you.")

# # Initialize session state for maintaining the workflow
# if 'state' not in st.session_state:
#     st.session_state['state'] = {
#         "messages": [],
#         "title": "",
#         "description": "",
#         "chapters": [],
#         "content": {},
#     }

# # Input Section for Title and Description
# if st.session_state['state']['title'] == "":
#     title = st.text_input("Enter the Book Title", "")
#     description = st.text_area("Enter the Book Description", "")

#     if st.button("Submit Title and Description") and title and description:
#         st.session_state['state']['title'] = title
#         st.session_state['state']['description'] = description
#         st.session_state['state']['messages'].append(HumanMessage(content=title))
#         st.session_state['state']['messages'].append(HumanMessage(content=description))
#         st.success("Title and description submitted! Proceed to generate Table of Contents.")

# # Generate Table of Contents
# if st.session_state['state']['title'] and not st.session_state['state']['chapters']:
#     if st.button("Generate Table of Contents"):
#         st.write(f"Generating Table of Contents for: {st.session_state['state']['title']}...")
#         response = llm.invoke(
#             toc_prompt.format_messages(
#                 title=st.session_state['state']['title'],
#                 description=st.session_state['state']['description']
#             )
#         )
#         st.write(response.content)
#         toc = response.content.split("\n")
#         st.session_state['state']['chapters'] = [chapter.strip() for chapter in toc if chapter.strip()]
#         st.session_state['state']['messages'].append(AIMessage(content=response.content))
#         st.success("Table of Contents generated! Proceed to generate chapters.")

# # Generate Chapters
# if st.session_state['state']['chapters'] and not st.session_state['state']['content']:
#     if st.button("Generate Chapters"):
#         st.write("Generating content for chapters...")
#         for chapter in st.session_state['state']['chapters']:
#             st.write(f"Generating content for chapter: {chapter}")
#             response = llm.invoke(chapter_prompt.format_messages(chapter=chapter))
#             st.session_state['state']['content'][chapter] = response.content
#             st.session_state['state']['messages'].append(AIMessage(content=response.content))
#             st.write(response.content)
#         st.success("All chapters generated! You can now push the content to GitHub.")

# # Push Content to GitHub
# if st.session_state['state']['content']:
#     repo_name = st.text_input("Enter the GitHub Repository Name", "")
#     if st.button("Push Book to GitHub") and repo_name:
#         g = Github(GITHUB_TOKEN)
#         user = g.get_user()
#         repo = user.create_repo(repo_name)
        
#         # Create directories and push markdown files
#         for chapter, content in st.session_state['state']['content'].items():
#             chapter_dir = chapter.replace(" ", "_")
#             repo.create_file(f"{chapter_dir}/README.md", f"Add {chapter} content", markdown2.markdown(content))
        
#         st.success(f"Book successfully pushed to {repo.html_url}")


import os
import streamlit as st
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from github import Github
from dotenv import load_dotenv
import markdown2

# Set page configuration for Streamlit
st.set_page_config(
    page_title="AI Book Generator",
    page_icon="📚",
    layout="wide"
)

# Load environment variables for API keys
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Initialize the ChatGroq model
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Define the state structure for book generation
class BookState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    title: str
    description: str
    chapters: List[str]
    content: dict

# Prompts for generating Table of Contents and chapters
toc_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced book author. Create a detailed Table of Contents based on the book title: {title} and description: {description}."),
    ("human", "Create a Table of Contents for my book."),
])

chapter_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in writing. Write a detailed chapter on {chapter} based on the given outline."),
    ("human", "Write a chapter for my book.")
])

# Define functions for generating the Table of Contents and chapters
def generate_toc(state: BookState) -> BookState:
    """Generate the Table of Contents."""
    response = llm.invoke(
        toc_prompt.format_messages(
            title=state["title"],
            description=state["description"]
        )
    )
    toc = response.content.split("\n")
    state["chapters"] = [chapter.strip() for chapter in toc if chapter.strip()]
    state["messages"].append(AIMessage(content=response.content))
    return state

def generate_chapters(state: BookState) -> BookState:
    """Generate content for each chapter."""
    for chapter in state["chapters"]:
        response = llm.invoke(chapter_prompt.format_messages(chapter=chapter))
        state["content"][chapter] = response.content
        state["messages"].append(AIMessage(content=response.content))
    return state

# Define the workflow using LangGraph
workflow = StateGraph(BookState)

# Add nodes for each step
workflow.add_node("generate_toc", generate_toc)
workflow.add_node("generate_chapters", generate_chapters)

# Define the edges and flow of the workflow
workflow.add_edge("generate_toc", "generate_chapters")
workflow.add_edge("generate_chapters", END)

# Set entry point for the workflow
workflow.set_entry_point("generate_toc")

# Compile the workflow into an app
app = workflow.compile()

# Streamlit User Interface
st.markdown(
    """
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .success {
            color: #4CAF50;
            font-weight: bold;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
            font-size: 2em;
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("📚 AI Book Generator")
st.markdown("Welcome to the **AI Book Generator!** 🎉 Provide your book's title and description, and let the AI generate the content for you.")

# Initialize session state for maintaining the workflow
if 'state' not in st.session_state:
    st.session_state['state'] = {
        "messages": [],
        "title": "",
        "description": "",
        "chapters": [],
        "content": {},
    }

# Sidebar for navigation
st.sidebar.header("🛠️ Functionality")
sidebar_options = st.sidebar.radio("Select an Action", ["Home", "Generate TOC", "Generate Chapters", "Push to GitHub"])

# Input Section for Title and Description
if sidebar_options == "Home":
    st.sidebar.subheader("Book Information")
    title = st.text_input("Enter the Book Title", "")
    description = st.text_area("Enter the Book Description", "")

    if st.button("Submit Title and Description") and title and description:
        st.session_state['state']['title'] = title
        st.session_state['state']['description'] = description
        st.session_state['state']['messages'].append(HumanMessage(content=title))
        st.session_state['state']['messages'].append(HumanMessage(content=description))
        st.success("Title and description submitted! Proceed to generate Table of Contents.", icon="✅")

# Generate Table of Contents using the workflow
if sidebar_options == "Generate TOC":
    if st.session_state['state']['title'] and not st.session_state['state']['chapters']:
        if st.button("Generate Table of Contents"):
            st.write(f"🔍 Generating Table of Contents for: **{st.session_state['state']['title']}**...")
            result = app.invoke(st.session_state['state'])
            st.session_state['state'] = result
            st.write("### Generated Table of Contents:")
            st.write("\n".join(st.session_state['state']['chapters']))
            st.success("✅ Table of Contents generated! Proceed to generate chapters.")

# Show the "Generate Chapters" button immediately after TOC generation
if sidebar_options == "Generate Chapters":
    if st.session_state['state']['chapters']:
        if st.button("Generate Chapters"):
            st.write("📖 Generating content for chapters...")
            result = app.invoke(st.session_state['state'])
            st.session_state['state'] = result
            st.write("### Generated Chapters:")
            for chapter, content in st.session_state['state']['content'].items():
                st.write(f"#### {chapter}")
                st.write(content)
            st.success("✅ All chapters generated! You can now push the content to GitHub.")

# Push Content to GitHub
if sidebar_options == "Push to GitHub":
    if st.session_state['state']['content']:
        st.sidebar.subheader("GitHub Repository")
        repo_name = st.text_input("Enter the GitHub Repository Name", "")
        if st.button("Push Book to GitHub") and repo_name:
            g = Github(GITHUB_TOKEN)
            user = g.get_user()
            repo = user.create_repo(repo_name)
            
            # Create directories and push markdown files
            for chapter, content in st.session_state['state']['content'].items():
                chapter_dir = chapter.replace(" ", "_")
                repo.create_file(f"{chapter_dir}/README.md", f"Add {chapter} content", markdown2.markdown(content))
            
            st.success(f"📤 Book successfully pushed to [GitHub Repository]({repo.html_url})!", icon="📁")
