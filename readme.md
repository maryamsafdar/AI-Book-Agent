# 📚 AI Book Generator

## Overview
The **AI Book Generator** is a Streamlit-based application that helps authors create structured books using AI. The user provides a title and a description of the book, and the AI generates a Table of Contents (TOC). Once the TOC is approved, the AI generates content for each chapter and subtopic in markdown format. The content is then pushed to a GitHub repository using PyGithub.

## Features
- Generate a book's Table of Contents based on user input.
- AI-powered generation of chapter content in markdown format.
- Content approval flow to ensure user satisfaction.
- Automatic publishing to a GitHub repository using PyGithub.
- Uses LangGraph for managing multi-step conversational flows.
- Attractive user interface built with Streamlit for easy interaction.

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- GitHub account for repository access
- GROQ API key for generating content

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-book-generator.git
   cd ai-book-generator

2. Install the required Python packages:
  ```bash
  pip install -r requirements.txt

3. Create a .env file in the project root and add your Groq API key:
   ```bash
   GROQ_API_KEY=groq_api_key

4. Run the Streamlit app:
  ```bash 
  streamlit run app.py


<!-- Example 1:
Title: The Art of Mindfulness Description: "This book explores the concept of mindfulness and its importance in today's fast-paced world. It covers techniques for meditation, mindful living, and how to incorporate mindfulness into everyday routines to achieve a balanced and peaceful life. The book includes practical exercises and real-life examples."

Example 2:
Title: The Beginner's Guide to Python Programming Description: "An introductory guide designed for new programmers, this book covers the basics of Python programming, including variables, loops, functions, and data structures. Each chapter is filled with hands-on examples, exercises, and tips for building practical Python applications. The goal is to help readers build a strong foundation in Python and prepare them for more advanced programming challenges."

Example 3:
Title: Exploring the Mysteries of Space Description: "This book takes readers on a journey through the cosmos, exploring the planets, stars, and galaxies that make up our universe. It delves into the history of space exploration, the latest discoveries in astronomy, and theories about the origins of the universe. Ideal for space enthusiasts, it blends scientific information with engaging storytelling."

Example 4:
Title: Healthy Cooking for Busy Families Description: "A cookbook designed for families who want to eat healthy but are short on time. It features quick and easy recipes, tips for meal planning, and strategies for balancing nutrition with a busy lifestyle. The book includes breakfast, lunch, dinner, and snack options, all made with wholesome ingredients and minimal prep time."

Example 5:
Title: Building Emotional Intelligence in Children Description: "A practical guide for parents and educators, this book focuses on helping children understand and manage their emotions. It discusses the importance of emotional intelligence for success in life and provides strategies for fostering empathy, resilience, and effective communication skills. The book also includes activities that parents can do with their children to strengthen emotional awareness."

These examples will help you get a sense of the kind of inputs the AI Book Generator can process to create a detailed table of contents and chapters. Feel free to modify these examples to suit your needs. -->





