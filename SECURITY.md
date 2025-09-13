# Security Policy

## Supported Versions

The following versions of SmartRecommender are currently receiving security updates:

| Version | Supported          | Notes                                 |
| ------- | ------------------ | ------------------------------------- |
| 3.0     | :white_check_mark: | Current stable release (Latest)       |
| 2.0     | :white_check_mark: | Previous stable - critical fixes only |
| 1.0     | :x:                | No longer supported                   |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in SmartRecommender, please follow these steps:

### Where to Report

- **For critical vulnerabilities**: Email the maintainers directly via GitHub
- **For general security issues**: Create a private security advisory on GitHub
- **Do not** create public issues for security vulnerabilities until they are resolved

### What to Include

Please provide the following information in your report:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Affected components** (backend/frontend/Docker/database)
5. **Suggested fix** (if you have one)
6. **Your contact information** for follow-up questions

### Response Timeline

- **Initial response**: Within 48 hours
- **Status updates**: Weekly updates on investigation progress
- **Resolution timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: 60 days

### What to Expect

**If the vulnerability is accepted:**

- We will work with you to understand and reproduce the issue
- We will develop a fix and test it thoroughly
- We will coordinate a responsible disclosure timeline
- You will be credited in our security acknowledgments (unless you prefer to remain anonymous)

**If the vulnerability is declined:**

- We will explain why we don't consider it a security issue
- We may suggest alternative reporting channels if appropriate
- We will still appreciate your effort in helping secure our project

## Security Best Practices

### For Users

1. **Keep your installation updated** to the latest supported version
2. **Use strong passwords** for database and admin accounts
3. **Enable HTTPS** in production deployments
4. **Regularly backup** your database
5. **Monitor logs** for suspicious activity
6. **Use environment variables** for sensitive configuration

### For Contributors

1. **Never commit secrets** (passwords, API keys, certificates)
2. **Use parameterized queries** to prevent SQL injection
3. **Validate all user input** on both frontend and backend
4. **Follow Django security guidelines** for backend development
5. **Keep dependencies updated** and scan for vulnerabilities
6. **Use secure Docker practices** (non-root users, minimal base images)

## Known Security Considerations

- **Database access**: Ensure PostgreSQL is properly configured with restricted access
- **File uploads**: Media files are validated but should be served through proper web server configuration
- **API endpoints**: Authentication required for sensitive operations
- **Session management**: Django's built-in session framework is used
- **Docker security**: Containers run with appropriate user permissions

## Security Updates

Security updates will be announced through:

- GitHub releases with security tags
- README.md updates for critical issues
- Commit messages clearly marked with "SECURITY:"

## Acknowledgments

We appreciate security researchers and contributors who help keep SmartRecommender secure. Security contributors will be acknowledged in our releases unless they prefer to remain anonymous.
