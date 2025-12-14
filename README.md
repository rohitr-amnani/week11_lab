# Week 11: Multi-Domain Intelligence Platform
Student Name: [Rohit Ramnani]
Student ID: [M01095242]
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A comprehensive, role-based dashboard application built with Streamlit and Python. This platform integrates three distinct operational domains—Cybersecurity, Data Science, and IT Operations—into a single interface. It features secure authentication, interactive data visualization, database management (CRUD), and domain-specific AI Assistants.

## Features
- Secure Authentication: User registration and login with role selection (User, Admin, Analyst) and `bcrypt` password hashing.
- Cybersecurity Dashboard: Real-time threat monitoring with attack trend graphs, incident logging, and severity tracking.
- Data Science Dashboard: Dataset registry with metadata management, storage analytics, and correlation visualizations.
- IT Operations Dashboard: IT ticket management system with priority tracking, workflow status updates, and volume analysis.
- AI Integration: Three distinct AI chatbots personalized for Cybersecurity, Data Science, and IT Support tasks.
- Interactive Visualizations: Dynamic charts using Plotly Express and Streamlit metrics.


## Technical Implementation
- Framework: Streamlit (Python)
- Hashing Algorithm: `bcrypt` with automatic salt generation
- Data Storage: SQLite Database (`intelligence_platform.db`) managed via `DatabaseManager`
- Password Security: Hashed storage using `bcrypt`, SQL injection prevention via parameterized queries
- Visualization Library: Plotly Express for interactive bar, line, and scatter charts
- AI Service: OpenAI API integration for contextual chatbots
- Validation: Input validation for usernames, passwords, and form data fields