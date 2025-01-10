import ell
import anthropic
from ell.providers.anthropic import AnthropicProvider

from .simple_example import simple_example
from .sqlite_example import sqlite_example
from .prompt_templates import TEST_GENERATION_PROMPT,SYSTEM_PROMPT


client = anthropic.Anthropic()

# def antrophic_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
#     client = anthropic.Anthropic()
#     example_text = sqlite_example if sqlite else simple_example
#     message = client.messages.create(
#     model="claude-3-5-sonnet-20241022",
#     max_tokens=2000,
#     temperature=0,
#     system=SYSTEM_PROMPT,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": example_text
#                 },
#                 {
#                     "type": "text",
#                     "text": TEST_GENERATION_PROMPT.format(lua_code=lua_code, existing_tests=existing_tests)
#                 },
#                 {
#                     "role": "assistant",
#                     "content": [
#                         {
#                     "type": "text",
#                     "text": "<test_planning>"
#                 }
#             ]
#         }
#             ]
#         },
#     ]
#     )
#     print(message.content[0].text);
#     return message.content[0].text


@ell.simple(model='claude-3-5-sonnet-20241022',client=client,max_tokens=2000)
def claude_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
    example_text = sqlite_example if sqlite else simple_example
    user_prompt = TEST_GENERATION_PROMPT.format(LUA_CODE=lua_code, EXISTING_TESTS=existing_tests)
    return [
        ell.system(SYSTEM_PROMPT),
        ell.user(example_text),
        ell.user(user_prompt),
        ell.assistant("<test_planning>")
    ]



@ell.simple(model='gpt-4',max_tokens=2000,temperature=0)
def openai_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
    example_text = sqlite_example if sqlite else simple_example
    user_prompt = TEST_GENERATION_PROMPT.format(LUA_CODE=lua_code, EXISTING_TESTS=existing_tests)
    return [
        ell.system(SYSTEM_PROMPT),
        ell.user(example_text),
        ell.user(user_prompt),
        ell.assistant("<test_planning>")
    ]




def generate_chunked_test_code(lua_code: str, existing_tests: str, sqlite: bool = False, part: int = 1, previous_parts: list[str] = None) -> str:
    """
    Generate test code in chunks, where each chunk stays within token limits.
    The LLM will number its output as <part X of Y> and continue in subsequent calls.
    
    Args:
        lua_code: The Lua code to generate tests for
        existing_tests: Existing TypeScript tests
        sqlite: Whether to use sqlite example
        part: Current part number to generate (default 1)
        previous_parts: List of test code from previous parts
    
    Returns:
        Test code for the requested part
    """
    example_text = sqlite_example if sqlite else simple_example
    previous_parts = previous_parts or []
    
    context = ""
    if previous_parts:
        context = "\nPrevious parts generated:\n"
        for i, prev_part in enumerate(previous_parts, 1):
            context += f"\n<part {i}>\n{prev_part}\n</part {i}>"
    
    chunked_prompt = f"""
{TEST_GENERATION_PROMPT}

{context}

IMPORTANT: Due to token limits, split your output into multiple parts.
- Each part should be small enough to fit within output token limits
- Number each part as <part X of Y> at the start
- This is part {part} - if there are more parts needed, end with "Continue with next part"
- If this is the final part, do not include "Continue with next part"
- Ensure your new tests are consistent with and build upon the previous parts
- Do not repeat tests from previous parts
"""
    return [
        ell.user(example_text),
        ell.user(chunked_prompt.format(lua_code=lua_code, existing_tests=existing_tests))
    ]

def generate_complete_test_code(lua_code: str, existing_tests: str, sqlite: bool = False) -> str:
    """
    Generate complete test code by making multiple LLM calls if needed.
    Handles the chunked responses and combines them.
    
    Args:
        lua_code: The Lua code to generate tests for
        existing_tests: Existing TypeScript tests
        sqlite: Whether to use sqlite example
    
    Returns:
        Complete combined test code from all parts
    """
    all_parts = []
    current_part = 1
    
    while True:
        response = openai_generate_test_code(
            lua_code=lua_code,
            existing_tests=existing_tests,
            sqlite=sqlite,
            system_prompt=generate_chunked_test_code(
                lua_code=lua_code,
                existing_tests=existing_tests,
                sqlite=sqlite,
                part=current_part,
                previous_parts=all_parts
            )
        )
        
        # Extract test code from the response
        if "<new_tests>" in response:
            test_code = response.split("<new_tests>")[1].split("</new_tests>")[0].strip()
            if test_code.lower() != "none":
                all_parts.append(test_code)
        
        # Check if we need to continue
        if "Continue with next part" not in response:
            break
            
        current_part += 1
        if current_part > 10:  # Safety limit to prevent infinite loops
            break
            
    return "\n".join(all_parts) if all_parts else "None"


