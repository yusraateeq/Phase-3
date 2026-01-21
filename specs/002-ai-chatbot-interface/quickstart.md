# Phase III Quickstart Guide: AI Chatbot Implementation

## 1. Prerequisites

### 1.1 System Requirements
- **Python**: 3.11+ (same as Phase II)
- **Node.js**: 18+ (same as Phase II)
- **Package Managers**: 
  - `uv` for Python dependencies (same as Phase II)
  - `pnpm` for JavaScript dependencies (same as Phase II)
- **Database**: Neon PostgreSQL account with credentials from Phase II
- **AI Service**: OpenAI account with API key

### 1.2 Environment Setup
Before starting, ensure Phase II is properly deployed and configured.

## 2. Backend Setup

### 2.1 Clone and Navigate
```bash
cd backend
```

### 2.2 Install AI Dependencies
```bash
uv pip install openai>=1.0.0 langchain>=0.0.300 langchain-openai>=0.0.5
```

### 2.3 Environment Configuration
Add to your `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
```

### 2.4 Database Migrations
Run the following commands to create and apply database migrations:
```bash
# Generate migration for new conversation models
alembic revision --autogenerate -m "Add conversation models"

# Apply the migration
alembic upgrade head
```

### 2.5 AI Service Initialization
Create the AI service structure:
```bash
mkdir -p src/ai src/ai/tools
touch src/ai/__init__.py
touch src/ai/openai_client.py
touch src/ai/chat_processor.py
touch src/ai/tools/__init__.py
touch src/ai/tools/task_tools.py
```

### 2.6 Start Backend Server
```bash
uvicorn src.main:app --reload
```

## 3. Frontend Setup

### 3.1 Navigate to Frontend
```bash
cd frontend
```

### 3.2 Install Chat Dependencies
```bash
pnpm install react-markdown react-syntax-highlighter
```

### 3.3 Create Chat Components
Create the following directory structure:
```bash
mkdir -p src/components/chat
touch src/components/chat/ChatInterface.tsx
touch src/components/chat/MessageBubble.tsx
touch src/components/chat/ChatInput.tsx
touch src/components/chat/ConversationHistory.tsx
```

### 3.4 Create Chat Page
```bash
mkdir -p src/app/chatbot
touch src/app/chatbot/page.tsx
```

### 3.5 Start Frontend Development Server
```bash
pnpm dev
```

## 4. Configuration

### 4.1 OpenAI Assistant Setup
1. Log into your OpenAI account
2. Navigate to the Assistants API section
3. Create a new Assistant with the following tools:
   - AddTaskTool
   - UpdateTaskTool
   - DeleteTaskTool
   - ListTasksTool
4. Note the Assistant ID for configuration

### 4.2 Environment Variables
Ensure the following are set in your respective `.env` files:
- Backend: `OPENAI_API_KEY`, `OPENAI_MODEL`
- Frontend: `NEXT_PUBLIC_WEBSOCKET_URL` (if using WebSockets)

## 5. Development Workflow

### 5.1 Backend Development
1. Start with AI service implementation
2. Implement the chat endpoint
3. Add conversation models and database integration
4. Connect to existing task APIs through tools
5. Test with unit tests

### 5.2 Frontend Development
1. Create the chat UI components
2. Implement real-time communication
3. Connect to backend API
4. Add error handling and loading states
5. Style with Tailwind CSS

### 5.3 Testing
1. Unit test AI service functions
2. Test conversation flow end-to-end
3. Verify user isolation
4. Test error handling scenarios
5. Performance testing for response times

## 6. Common Commands

### 6.1 Backend Commands
```bash
# Run backend server
uvicorn src.main:app --reload

# Run backend tests
python -m pytest tests/

# Run database migrations
alembic upgrade head

# Generate new migration
alembic revision --autogenerate -m "description"
```

### 6.2 Frontend Commands
```bash
# Start development server
pnpm dev

# Run frontend tests
pnpm test

# Build for production
pnpm build
```

## 7. Troubleshooting

### 7.1 Common Issues

**Issue**: OpenAI API returning authentication errors
**Solution**: Verify `OPENAI_API_KEY` is correctly set in `.env` file

**Issue**: Chat interface not updating in real-time
**Solution**: Check WebSocket connection or polling interval configuration

**Issue**: Database migration errors
**Solution**: Ensure you've run `alembic upgrade head` after generating migrations

**Issue**: Cross-origin errors during development
**Solution**: Verify backend and frontend are running on correct ports with proper CORS configuration

### 7.2 Debugging Tips
- Enable detailed logging in the AI service for processing insights
- Use browser developer tools to inspect API requests
- Check database directly to verify conversation/message creation
- Monitor OpenAI usage in your dashboard

## 8. Next Steps

1. Complete the implementation following the technical plan
2. Thoroughly test all chatbot functionality
3. Verify user isolation and security measures
4. Performance test with multiple concurrent users
5. Prepare for integration with Phase II features