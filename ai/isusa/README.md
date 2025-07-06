# ISUSA - International Student USA Journey

## Overview

ISUSA is a web application designed to assist international students in the USA with their journey. The application provides advice and resources for various stages of their academic and professional careers.

## Features

- User authentication (login and registration)
- Advice generation using OpenAI
- Interaction history tracking
- Navigation through different sections: Product, Solution, Resource, and Pricing

## Architecture

The application consists of three main components:

1. **Front-end**: A React-based web application that provides the user interface.
2. **Back-end**: A Flask-based API server that handles authentication, advice generation, and interaction history.
3. **Other Server**: OpenAI API server used for generating advice.

## Diagram

    A[User] -->|Interacts with| B[Front-end (React)]
    B -->|Sends requests to| C[Back-end (Flask)]
    C -->|Requests advice from| D[OpenAI API]
    C -->|Stores data in| E[MongoDB]