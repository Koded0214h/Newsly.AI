# Newsly.AI - Frontend Setup and Development Guide

## Frontend Setup (React)

1. **Prerequisites**
   - Node.js (v16 or higher)
   - npm (comes with Node.js)
   - Git

2. **Initial Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/your-username/Newsly.AI.git
   cd Newsly.AI

   # Install dependencies
   npm install
   ```

3. **Development**
   ```bash
   # Start the development server
   npm start
   ```
   The frontend will run on `http://localhost:3000`

4. **Building for Production**
   ```bash
   npm run build
   ```
   This creates an optimized production build in the `build` folder.

## Important Notes

- **DO NOT** modify any backend files unless specifically instructed
- The backend is already configured and running on `http://localhost:8000`
- All API endpoints are prefixed with `/api/`
- The backend handles:
  - User authentication
  - Article management
  - Email digests
  - AI summarization

## GitHub Workflow

### Making Changes

1. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Make changes to frontend files only
   - Test your changes locally
   - Ensure the code follows the project's style guide

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

4. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your feature branch
   - Add description of changes
   - Request review if needed

### Updating Your Local Repository

1. **Fetch Latest Changes**
   ```bash
   git fetch origin
   ```

2. **Update Your Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git merge main
   ```

3. **Resolve Conflicts** (if any)
   - Fix conflicts in your code editor
   - Commit the resolved changes
   - Push the updates

## Best Practices

1. **Branch Naming**
   - Use descriptive names
   - Prefix with feature/, bugfix/, or hotfix/
   - Example: `feature/user-profile` or `bugfix/login-error`

2. **Commit Messages**
   - Be clear and descriptive
   - Use present tense
   - Example: "Add user profile component" not "Added user profile component"

3. **Code Review**
   - Review your own code before pushing
   - Ensure all tests pass
   - Check for any console errors
   - Verify responsive design

4. **Frontend Development**
   - Keep components small and focused
   - Use proper error handling
   - Implement loading states
   - Follow React best practices

## Troubleshooting

1. **Dependencies Issues**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Remove node_modules and reinstall
   rm -rf node_modules
   npm install
   ```

2. **Git Issues**
   ```bash
   # Reset to last known good state
   git reset --hard origin/main
   
   # Clean untracked files
   git clean -fd
   ```

3. **Development Server Issues**
   ```bash
   # Kill process on port 3000 (if needed)
   lsof -i :3000
   kill -9 <PID>
   ```

## Need Help?

- Check existing issues on GitHub
- Create a new issue if needed
- Contact the project maintainers

Remember: Always work on frontend changes in your feature branch and never directly on the main branch. 