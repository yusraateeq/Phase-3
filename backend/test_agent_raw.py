import asyncio
import sys
import traceback
sys.path.insert(0, 'src')

from sqlmodel import Session, create_engine
from ai.agent import TodoAgent
from core.config import settings
from uuid import uuid4
from langchain_core.messages import HumanMessage

async def test_agent():
    # Create a test database session
    engine = create_engine(settings.DATABASE_URL)
    
    with Session(engine) as session:
        # Create agent with a test user ID
        test_user_id = uuid4()
        agent = TodoAgent(session=session, user_id=test_user_id)
        
        # Test a simple message
        print("Testing agent with message: 'hi'", file=sys.stderr)
        try:
            # Call the agent executor directly to see the raw error
            response = await agent.agent_executor.ainvoke({
                "messages": [HumanMessage(content="hi")]
            })
            print(f"Response: {response}", file=sys.stderr)
        except Exception as e:
            print(f"FULL ERROR:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(test_agent())
