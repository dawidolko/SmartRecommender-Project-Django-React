# Contributing to SmartRecommender

First off, **thank you** for considering contributing to **SmartRecommender**! It's people like you that make this product recommendation platform so valuable to the community. Whether you're reporting a bug, suggesting a new feature, or submitting a pull request, **every contribution** is highly appreciated.

---

## How to Contribute

There are many ways you can help SmartRecommender evolve and grow. Below are guidelines for the most common contribution pathways.

---

## Reporting Issues

1. **Search First**

   - Before creating a new issue, please check the issue tracker to see if the problem has already been reported.

2. **Provide Details**
   - If you haven't found anything similar, go ahead and file an issue.
   - Use the bug report template if provided.
   - Include detailed steps to reproduce the behavior and any relevant information (e.g., environment, logs, screenshots).
   - For backend issues, specify which part of the system is affected (database, API, recommendation algorithm).
   - For frontend issues, include browser information and screenshots when possible.
   - For Docker-related issues, include container logs and Docker version information.

Following these guidelines helps maintainers and the community understand, reproduce, and fix the problem faster.

---

## Feature Requests

- We welcome and value new ideas, especially those that enhance our recommendation algorithms.
- Clearly describe the proposed feature, providing as much context and reasoning as possible.
- For algorithm improvements, explain the expected benefit to recommendation quality.
- For UI/UX enhancements, describe how they will improve user experience.
- For Docker/deployment improvements, explain how they will simplify setup or improve reliability.

If the idea is a good fit, maintainers or contributors can help refine and discuss how best to implement it.

---

## Pull Requests

1. **Link to an Issue**

   - Always ensure there's a corresponding issue for the pull request. This way, everyone can see why the change is being proposed and track its progress.

2. **Branch Naming**

   - Create a new branch off `main` for your work, following these naming conventions:
     - **feature/your-feature** if you're adding a feature
     - **bugfix/your-fix** if you're fixing a bug
     - **algo/your-algorithm** if you're modifying a recommendation algorithm
     - **docker/your-improvement** if you're improving Docker configuration

3. **Coding Conventions**

   - Maintain the style and structure consistent with the existing codebase.
   - For Django/Python code:
     - Follow PEP 8 guidelines
     - Write docstrings for new functions and classes
   - For React/JavaScript code:
     - Use consistent component structure
     - Follow the project's ESLint configuration
   - For Docker configurations:
     - Use multi-stage builds where appropriate
     - Follow Docker best practices for layer caching
     - Document any new environment variables

4. **Tests and CI**

   - Make sure your code passes all existing tests.
   - For backend changes, include Django tests that verify your changes.
   - For algorithm modifications, include tests that verify recommendation quality.
   - For frontend changes, ensure components render correctly.
   - For Docker changes, verify containers build and run successfully.

5. **Pull Request Template**

   - Fill out the pull request template to provide an overview of your changes.
   - Include screenshots, GIFs, or any visual aids that clarify your modifications.
   - For algorithm changes, include before/after metrics if possible.
   - For Docker changes, include build logs and performance comparisons if relevant.

6. **No Issue Numbers in Title**
   - Avoid referencing the issue number in the PR title. Instead, mention the issue number in the pull request description (e.g., "Resolves #123").

---

## Contributing to Recommendation Algorithms

SmartRecommender uses several recommendation algorithms:

1. **Collaborative Filtering**

   - When modifying this algorithm, ensure user similarity calculations remain efficient.
   - Test with various user datasets to ensure recommendations remain relevant.

2. **Content-Based Filtering**

   - Changes should preserve or improve product attribute analysis.

3. **Association Rules**

   - Modifications should maintain or improve the Apriori algorithm implementation.
   - Test changes with transaction data to verify "Frequently Bought Together" recommendations.

4. **Fuzzy Search**

   - Ensure changes maintain the balance between performance and search accuracy.
   - Test with common misspellings and partial queries.

5. **Sentiment Analysis**

   - Verify NLP processing maintains correct sentiment scoring.
   - Test with positive, negative, and neutral product reviews.

6. **Probabilistic Methods**
   - Ensure prediction models maintain accuracy while improving performance.
   - Test with historical data to verify forecast quality.

---

## Development Setup

### Option 1: Docker Setup (Recommended)

The fastest way to get started with development:

1. **Prerequisites**

   - Docker Desktop installed
   - Hardware virtualization enabled

2. **Quick Start**

   ```bash
   git clone <repository-url>
   cd SmartRecommender-Project-Django-React

   # Create .env file with database settings
   echo "DB_NAME=product_recommendation
   DB_USER=postgres
   DB_PASSWORD=admin
   DB_HOST=db
   DB_PORT=5432" > .env

   # Start all services
   docker compose -f .tools/docker/docker-compose.yml up --build
   ```

3. **Development Commands**

   ```bash
   # View logs
   docker compose -f .tools/docker/docker-compose.yml logs -f

   # Enter backend container for debugging
   docker exec -it SmartRecommender-Django bash

   # Run tests in backend container
   docker exec -it SmartRecommender-Django python manage.py test

   # Access database
   docker exec -it SmartRecommender-PostgreSQL psql -U postgres -d product_recommendation
   ```

### Option 2: Manual Setup

1. **Backend Setup**

   - Set up a PostgreSQL database
   - Install Python dependencies with `pip install -r requirements.txt`
   - Run migrations with `python manage.py migrate`
   - Generate test data with `python manage.py seed`

2. **Frontend Setup**

   - Install Node.js dependencies with `npm install`
   - Start the development server with `npm start`

3. **Testing Environment**
   - Run backend tests with `python manage.py test`
   - Run frontend tests with `npm test`

---

## Docker Development Guidelines

When contributing Docker-related changes:

1. **Performance Considerations**

   - Use `.dockerignore` files to exclude unnecessary files
   - Leverage Docker layer caching for faster builds
   - Use multi-stage builds when appropriate

2. **Environment Variables**

   - Document new environment variables in both `.env.example` and README
   - Use secure defaults where possible
   - Never commit actual credentials

3. **Container Health**

   - Include health checks for services that need them
   - Use proper wait conditions for service dependencies
   - Ensure graceful shutdown handling

4. **Testing Docker Changes**

   ```bash
   # Clean build to test from scratch
   docker compose -f .tools/docker/docker-compose.yml down -v
   docker system prune -a -f
   docker compose -f .tools/docker/docker-compose.yml up --build

   # Test individual services
   docker compose -f .tools/docker/docker-compose.yml up db
   docker compose -f .tools/docker/docker-compose.yml up backend
   ```

---

## Thank You!

We truly appreciate your time and effort in improving SmartRecommender. Your contributions help make the project better for everyone. If you have any questions, feel free to open a discussion or reach out to the maintainers.
