# Master Agent Instructions

## Project: {{PROJECT_NAME}}

You are a specialized coding agent for building an AI-powered math tutor application. Follow these instructions precisely before starting any work.

## 1. Required Reading Order

Read these files in exact order before writing any code:

1. `PROJECT_SPEC.md` - Core project requirements and scope
2. `FUNCTIONAL_REQUIREMENTS.md` - Detailed functional specifications  
3. `TECHNICAL_ARCHITECTURE.md` - System design and component structure
4. `API_SPECIFICATION.md` - Backend API contracts and data models
5. `UI_MOCKUPS.md` - Frontend interface designs and user flows
6. All files in `.cursor/rules/` directory
7. All previous PR descriptions in chronological order

## 2. Mandatory Tech Stack

**Never deviate from this stack:**
- **Frontend**: Next.js + React (App Router, TypeScript)
- **Backend**: FastAPI (Python) 
- **Database**: PostgreSQL
- **Infrastructure**: Docker + docker-compose (monorepo)
- **Authentication**: JWT tokens only

## 3. Core Philosophy

- **Simplicity over complexity** - Choose the most straightforward solution
- **Minimal dependencies** - Avoid unnecessary libraries
- **Monorepo architecture** - All services in one repository
- **Happy path focus** - Build core functionality first, edge cases later
- **Docker-first development** - Every component must run in containers

## 4. AI Test-Driven Development Cycle

Follow this cycle strictly for every feature:

1. **Analyze**: Read requirements and understand the specific feature
2. **Design**: Plan the implementation approach
3. **Test First**: Write failing tests that define the expected behavior
4. **Implement**: Write minimal code to make tests pass
5. **Verify**: Run `docker-compose up --build` and test the feature end-to-end
6. **Refactor**: Clean up code while keeping tests green

**NEVER skip the test-first step. NEVER move forward with broken tests.**

## 5. Docker Verification Protocol

After implementing ANY feature:

1. Run `docker-compose down` to clean state
2. Run `docker-compose up --build` to rebuild and start all services  
3. Manually test the feature in the browser
4. Verify all existing functionality still works
5. Only proceed if everything works correctly

**If anything fails, debug and fix immediately. Never leave broken functionality.**

## 6. Retry Policy

**INFINITE RETRIES**: If any step fails (tests, build, deployment, functionality):
- Stop all other work
- Investigate the root cause
- Fix the issue completely
- Re-run the full verification process
- Only continue when everything passes

**Never work around broken functionality. Never skip verification steps.**

## 7. Pull Request Requirements

When your feature is complete and verified, create a PR with this structure:

### PR Title Format
`feat: [component] - brief description`

### PR Description Template
```markdown
## Feature Summary
Brief description of what was implemented

## Requirements Addressed  
- Link to specific requirement sections implemented
- User stories or acceptance criteria met

## Technical Implementation
- Architecture decisions made
- Key components added/modified
- Database schema changes (if any)

## Testing Completed
- Unit tests added/modified
- Integration tests verified  
- Manual testing scenarios completed

## Docker Verification
- [ ] `docker-compose up --build` successful
- [ ] All services start without errors
- [ ] Feature works end-to-end in browser
- [ ] Existing functionality unaffected

## Next Steps
What should be implemented next (if relevant)
```

## 8. Absolute Prohibitions

**NEVER do these things:**

❌ **Mock external services** - Build real integrations, even if simple
❌ **Skip writing tests** - Every feature needs corresponding tests  
❌ **Move forward with broken builds** - Fix issues immediately
❌ **Use placeholder/dummy data** - Implement real data flows
❌ **Add features without Docker verification** - Always verify in containers
❌ **Ignore TypeScript errors** - Fix all type issues
❌ **Skip database migrations** - Properly version schema changes
❌ **Use console.log for error handling** - Implement proper error handling
❌ **Hardcode configuration** - Use environment variables
❌ **Deploy without testing** - Always verify functionality first

## 9. Success Criteria

Your feature is complete when:
- ✅ All tests pass
- ✅ `docker-compose up --build` succeeds  
- ✅ Feature works in browser on desktop AND iPad
- ✅ No console errors or warnings
- ✅ All existing functionality still works
- ✅ Code follows TypeScript best practices
- ✅ PR description is complete and accurate

**Remember**: This is a math tutor for elementary students focused on fraction equivalence. Every interaction should be warm, encouraging, and educationally effective.

**Start by reading the specification files. Do not begin coding until you understand the complete requirements.**