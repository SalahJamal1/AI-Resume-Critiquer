
from langchain_core.prompts import ChatPromptTemplate

from graph.consts import llm


prompt=ChatPromptTemplate.from_messages([
    ("system","""Please analyze this resume and provide constructive feedback. 
Focus on the following aspects:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Specific improvements for {job_role}

Resume content:
{documents}

Please provide your analysis in a clear, structured format with specific recommendations.""")
])

analyze_chain=prompt | llm