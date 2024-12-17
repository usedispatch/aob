import ell
import anthropic
from .examples import simple_example,sqlite_example
from .prompt_templates import TEST_GENERATION_PROMPT


client = anthropic.Anthropic()

def antrophic_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
    client = anthropic.Anthropic()
    example_text = sqlite_example if sqlite else simple_example
    # message = client.messages.create(
    # model="claude-3-5-sonnet-20241022",
    # max_tokens=1000,
    # temperature=0,
    # messages=[
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "text",
    #                 "text": example_text,
    #             },
    #             {
    #                 "type": "text",
    #                 "text": TEST_GENERATION_PROMPT.format(lua_code=lua_code, existing_tests=existing_tests)
    #             }
    #         ]
    #     },
    #      {
    #         "role": "assistant",
    #         "content": [
    #             {
    #                 "type": "text",
    #                 "text": "<test_planning>"
    #             }
    #         ]
    #     }
    # ]
    # )
    message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "<examples>\n<example>\n<LUA_CODE>\ncounter = 0\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\n\nfunction incrementCounter(msg)\n    counter = counter + 1\n    sendReply(msg, counter)\nend\n\nfunction decrementCounter(msg)\n    counter = counter - 1\n    sendReply(msg, counter)\nend\n\nfunction getCounter(msg)\n    sendReply(msg, counter)\nend\n\n\nHandlers.add(\"incrementCounter\", incrementCounter)\nHandlers.add(\"decrementCounter\", decrementCounter)\nHandlers.add(\"getCounter\", getCounter)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n\n});\n</EXISTING_TESTS>\n<ideal_output>\n<test_planning>\n1. Handlers in Lua code:\n- incrementCounter\n- decrementCounter\n- getCounter\n\n2. Handlers covered by existing tests:\n- getCounter (initial value test)\n- incrementCounter (single increment test)\n\n3. Handlers needing new tests:\n- decrementCounter (no tests)\n- incrementCounter (needs additional scenarios)\n- getCounter (needs additional verification after modifications)\n\n4. Test scenarios needed:\n- decrementCounter:\n  * Basic decrement functionality\n  * Verify negative numbers work\n- incrementCounter:\n  * Multiple increments\n  * Verify state persistence\n- getCounter:\n  * Verify after decrement\n  * Verify after multiple operations\n\n5. Number of new tests to generate: 6\n\nThe new tests will verify the complete functionality of the counter system, including:\n- Decrement operations\n- Multiple operations in sequence\n- State consistency across different handler calls\n</test_planning>\n\n<new_tests>\n  test(\"should decrement counter\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should handle negative numbers when decrementing\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Data, -1);\n  });\n\n  test(\"should maintain state across multiple increments\", async () => {\n    await env.send({ Action: \"incrementCounter\" });\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n  test(\"should verify counter state with getCounter\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n  test(\"should handle mixed increment and decrement operations\", async () => {\n    await env.send({ Action: \"incrementCounter\" });\n    await env.send({ Action: \"incrementCounter\" });\n    await env.send({ Action: \"decrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 2);\n  });\n\n  test(\"should verify correct response action names\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Action, \"decrementCounterResponse\");\n  });\n</new_tests>\n</ideal_output>\n</example>\n<example>\n<LUA_CODE>\nlocal json = require(\"json\")\n\n-- Task list storage\nlocal tasks = {}\n\n-- Task status constants\nlocal STATUS = {\n    PENDING = \"[ ]\",\n    COMPLETED = \"[X]\"\n}\n\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\nfunction findTaskById(id)\n    for _, task in ipairs(tasks) do\n        if task.id == id then\n            return task\n        end\n    end\n    return nil\nend\n\n\nfunction addTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = {\n        id = #tasks + 1,\n        title = data.title,\n        description = data.description,\n        status = STATUS.PENDING,\n    }\n    table.insert(tasks, task)\n    sendReply(msg, task)\nend\n\nfunction updateTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = findTaskById(data.id)\n    if not task then\n        error(\"Task not found\")\n    end\n    task.status = data.status\n    sendReply(msg, task)\nend\n\n\nfunction getTasksProcessor(msg)\n    sendReply(msg, tasks)\nend\n\n\n\n\nHandlers.add(\"addTask\", addTaskProcessor)\nHandlers.add(\"updateTask\", updateTaskProcessor)\nHandlers.add(\"getTasks\", getTasksProcessor)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"addTask\", async () => {\n    await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Test Task\",\n        description: \"Test Description\",\n      }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n});\n</EXISTING_TESTS>\n<ideal_output>\n<test_planning>\n1. Handlers in Lua code:\n- addTask\n- updateTask\n- getTasks\n\n2. Handlers covered by existing tests:\n- addTask (basic test exists)\n- getTasks (partially covered as part of addTask test)\n\n3. Handlers needing new tests:\n- updateTask (no coverage)\n- Additional scenarios for getTasks\n- More comprehensive scenarios for addTask\n\n4. Test scenarios needed:\nFor updateTask:\n- Update task status to completed\n- Attempt to update non-existent task\n- Verify task status change\n\nFor getTasks:\n- Get empty task list\n- Get multiple tasks\n\nFor addTask (additional coverage):\n- Add multiple tasks\n- Verify task ID increment\n\n5. Number of new tests to generate: 5\n\nThe existing tests only cover basic addTask functionality. We need to add comprehensive tests for updateTask and additional scenarios for the other handlers.\n</test_planning>\n\n<new_tests>\n  test(\"should get empty task list initially\", async () => {\n    const response = await env.send({ Action: \"getTasks\" });\n    assert.deepStrictEqual(response.Messages[0].Data, []);\n  });\n\n  test(\"should add multiple tasks\", async () => {\n    const task1 = await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"First Task\",\n        description: \"First Description\",\n      }),\n    });\n    const task2 = await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Second Task\",\n        description: \"Second Description\",\n      }),\n    });\n\n    const response = await env.send({ Action: \"getTasks\" });\n    assert.equal(response.Messages[0].Data.length, 2);\n    assert.equal(response.Messages[0].Data[0].id, 1);\n    assert.equal(response.Messages[0].Data[1].id, 2);\n  });\n\n  test(\"should update task status\", async () => {\n    const addResponse = await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Update Test\",\n        description: \"Test Description\",\n      }),\n    });\n    \n    const taskId = addResponse.Messages[0].Data.id;\n    \n    const updateResponse = await env.send({\n      Action: \"updateTask\",\n      Data: JSON.stringify({\n        id: taskId,\n        status: \"[X]\"\n      }),\n    });\n\n    assert.equal(updateResponse.Messages[0].Data.status, \"[X]\");\n  });\n\n  test(\"should fail when updating non-existent task\", async () => {\n    try {\n      await env.send({\n        Action: \"updateTask\",\n        Data: JSON.stringify({\n          id: 999,\n          status: \"[X]\"\n        }),\n      });\n      assert.fail(\"Should have thrown an error\");\n    } catch (error) {\n      assert.ok(error.message.includes(\"Task not found\"));\n    }\n  });\n\n  test(\"should maintain task list state\", async () => {\n    const getResponse = await env.send({ Action: \"getTasks\" });\n    const tasks = getResponse.Messages[0].Data;\n    \n    // Verify the state includes previously added tasks\n    assert.ok(tasks.length > 0);\n    assert.ok(tasks.some(task => task.status === \"[X]\"));\n  });\n</new_tests>\n</ideal_output>\n</example>\n</examples>\n\n"
                },
                {
                    "type": "text",
                    "text": "You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests.\n\nFirst, examine the following Lua code:\n\n<lua_code>\n{{LUA_CODE}}\n</lua_code>\n\nNow, review the existing TypeScript tests:\n\n<existing_tests>\n{{EXISTING_TESTS}}\n</existing_tests>\n\nYour goal is to generate new TypeScript tests for the Lua code provided. Follow these guidelines:\n\n1. Focus on testing handlers in the Lua code that are not covered by existing tests.\n2. Ensure new tests are comprehensive and follow the structure of existing tests.\n3. Use TypeScript and the 'aos' framework, maintaining consistency with existing tests.\n4. Only add new tests for handlers that don't have corresponding tests.\n5. Maintain the existing test file structure, including the 'describe' and 'test' blocks.\n\nBefore providing the new tests, analyze the Lua code and existing tests. Wrap your analysis in <test_planning> tags. Consider the following steps:\n1. List all handlers in the Lua code\n2. Identify which handlers are already covered by existing tests\n3. Determine which handlers need new tests\n4. For each handler needing tests, outline potential scenarios to test\n5. Count the number of new tests you plan to generate\n\nThen, generate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself in the <new_tests> section. If the existing tests are comprehensive and no new tests are needed, output 'None' in the <new_tests> tags.\n\nProvide your output in the following format:\n\n<test_planning>\n[Insert your analysis and reasoning here, following the steps outlined above]\n</test_planning>\n\n<new_tests>\n[Insert only the new TypeScript test code here, or 'None' if no new tests are needed]\n</new_tests>\n\nRemember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers or uncovered scenarios."
                }
            ]
        },
        # {
        #     "role": "assistant",
        #     "content": [
        #         {
        #             "type": "text",
        #             "text": "<test_planning>"
        #         }
        #     ]
        # }
    ]
)
    print(message.content[0].text);
    return message.content[0].text





@ell.simple(model='gpt-4',max_tokens=1000,temperature=0,client=client)
def openai_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
    example_text = sqlite_example if sqlite else simple_example
    return [
        ell.user(example_text),
        ell.user(TEST_GENERATION_PROMPT.format(lua_code=lua_code, existing_tests=existing_tests))
    ]


# @ell.simple(model='claude-3-5-sonnet-20241022', client=client,max_tokens=2000)
# def generate_test_code(lua_code: str, existing_tests: str) -> str:
#     prompt = f"""
# Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests. 
# You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. 
# First, examine the following Lua code:

# <lua_code>
# {lua_code}
# </lua_code>

# Now, review the existing TypeScript tests:

# <existing_tests>
# {existing_tests}
# </existing_tests>

# Your goal is to generate new TypeScript tests only for new handlers in the Lua code provided. Follow these guidelines:

# 1. Focus exclusively on testing new handlers in the Lua code that don't have corresponding tests.
# 2. Ensure new tests are comprehensive and follow TypeScript and existing test patterns.
# 3. Maintain the existing test file structure.
# 4. Do not generate any tests for handlers that already have tests.

# Before generating new tests, carefully analyze the Lua code and existing tests. Wrap your analysis in <code_analysis> tags:

# 1. List all handlers in the Lua code, numbering them.
# 2. List all handlers in the existing tests, numbering them.
# 3. Compare the two lists and identify new handlers that need testing.
# 4. For each new handler, outline its functionality and potential test cases.

# After your analysis, generate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself. If no new tests are needed, output "None".

# Provide your output in the following format:

# <new_tests>
# [Insert only the new TypeScript test code here, or "None" if no new tests are needed]
# </new_tests>

# Remember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers."""

#     return prompt

