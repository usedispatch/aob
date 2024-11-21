import ell
import anthropic

client = anthropic.Anthropic()

def antrophic_generate_test_code(lua_code: str,existing_tests: str) :
    client = anthropic.Anthropic()
    message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "<examples>\n<example>\n<LUA_CODE>\n\ncounter = 0\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\n\nfunction incrementCounter(msg)\n    counter = counter + 1\n    sendReply(msg, counter)\nend\n\nfunction decrementCounter(msg)\n    counter = counter - 1\n    sendReply(msg, counter)\nend\n\nfunction getCounter(msg)\n    sendReply(msg, counter)\nend\n\n\nHandlers.add(\"incrementCounter\", incrementCounter)\nHandlers.add(\"decrementCounter\", decrementCounter)\nHandlers.add(\"getCounter\", getCounter)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n\n});\n</EXISTING_TESTS>\n<ideal_output>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n  test(\"should decrement counter\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should handle multiple increments\", async () => {\n    await env.send({ Action: \"incrementCounter\" });\n    await env.send({ Action: \"incrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 2);\n  });\n\n  test(\"should handle multiple decrements\", async () => {\n    await env.send({ Action: \"decrementCounter\" });\n    await env.send({ Action: \"decrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should allow negative numbers\", async () => {\n    await env.send({ Action: \"decrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, -1);\n  });\n});\n\n</ideal_output>\n</example>\n<example>\n<LUA_CODE>\nlocal json = require(\"json\")\n\n-- Task list storage\nlocal tasks = {}\n\n-- Task status constants\nlocal STATUS = {\n    PENDING = \"[ ]\",\n    COMPLETED = \"[X]\"\n}\n\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\nfunction findTaskById(id)\n    for _, task in ipairs(tasks) do\n        if task.id == id then\n            return task\n        end\n    end\n    return nil\nend\n\n\nfunction addTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = {\n        id = #tasks + 1,\n        title = data.title,\n        description = data.description,\n        status = STATUS.PENDING,\n    }\n    table.insert(tasks, task)\n    sendReply(msg, task)\nend\n\nfunction updateTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = findTaskById(data.id)\n    if not task then\n        error(\"Task not found\")\n    end\n    task.status = data.status\n    sendReply(msg, task)\nend\n\n\nfunction getTasksProcessor(msg)\n    sendReply(msg, tasks)\nend\n\n\n\n\nHandlers.add(\"addTask\", addTaskProcessor)\nHandlers.add(\"updateTask\", updateTaskProcessor)\nHandlers.add(\"getTasks\", getTasksProcessor)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"addTask\", async () => {\n    await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Test Task\",\n        description: \"Test Description\",\n      }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n});\n\n</EXISTING_TESTS>\n<ideal_output>\n  test(\"updateTask\", async () => {\n    await env.send({\n      Action: \"updateTask\",\n      Data: JSON.stringify({ id: 1, status: \"[X]\" }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n  test(\"getTasks\", async () => {\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n</ideal_output>\n</example>\n</examples>\n\n"
                },
                {
                    "type": "text",
                    "text": f"You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests.\n\nFirst, examine the following Lua code:\n\n<lua_code>\n{lua_code}\n</lua_code>\n\nNow, review the existing TypeScript tests:\n\n<existing_tests>\n{existing_tests}\n</existing_tests>\n\nYour goal is to generate new TypeScript tests for the Lua code provided. Follow these guidelines:\n\n1. Focus on testing handlers in the Lua code.\n2. Ensure tests are comprehensive but do not duplicate existing tests.\n3. Follow TypeScript and existing test patterns.\n4. Be idempotent - only add new tests for new Lua code, not for code that already has tests.\n5. Maintain the existing test file structure.\n\nGenerate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself. If the already provided test's are fulfilling output None.\n\nProvide your output in the following format:\n\n<new_tests>\n[Insert only the new TypeScript test code here]\n</new_tests>\n\nRemember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers "
                }
            ]
        }
    ]
    )
    print(message.content[0].text)
    return message.content[0].text



# Replace placeholders like {{LUA_CODE}} with real values,
# because the SDK does not support variables.




@ell.simple(model='gpt-4',max_tokens=1000,temperature=0)
def openai_generate_test_code(lua_code: str,existing_tests: str) -> str:
    return [
        ell.user("<examples>\n<example>\n<LUA_CODE>\n\ncounter = 0\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\n\nfunction incrementCounter(msg)\n    counter = counter + 1\n    sendReply(msg, counter)\nend\n\nfunction decrementCounter(msg)\n    counter = counter - 1\n    sendReply(msg, counter)\nend\n\nfunction getCounter(msg)\n    sendReply(msg, counter)\nend\n\n\nHandlers.add(\"incrementCounter\", incrementCounter)\nHandlers.add(\"decrementCounter\", decrementCounter)\nHandlers.add(\"getCounter\", getCounter)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n\n});\n</EXISTING_TESTS>\n<ideal_output>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n  test(\"should decrement counter\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should handle multiple increments\", async () => {\n    await env.send({ Action: \"incrementCounter\" });\n    await env.send({ Action: \"incrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 2);\n  });\n\n  test(\"should handle multiple decrements\", async () => {\n    await env.send({ Action: \"decrementCounter\" });\n    await env.send({ Action: \"decrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should allow negative numbers\", async () => {\n    await env.send({ Action: \"decrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, -1);\n  });\n});\n\n</ideal_output>\n</example>\n<example>\n<LUA_CODE>\nlocal json = require(\"json\")\n\n-- Task list storage\nlocal tasks = {}\n\n-- Task status constants\nlocal STATUS = {\n    PENDING = \"[ ]\",\n    COMPLETED = \"[X]\"\n}\n\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\nfunction findTaskById(id)\n    for _, task in ipairs(tasks) do\n        if task.id == id then\n            return task\n        end\n    end\n    return nil\nend\n\n\nfunction addTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = {\n        id = #tasks + 1,\n        title = data.title,\n        description = data.description,\n        status = STATUS.PENDING,\n    }\n    table.insert(tasks, task)\n    sendReply(msg, task)\nend\n\nfunction updateTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = findTaskById(data.id)\n    if not task then\n        error(\"Task not found\")\n    end\n    task.status = data.status\n    sendReply(msg, task)\nend\n\n\nfunction getTasksProcessor(msg)\n    sendReply(msg, tasks)\nend\n\n\n\n\nHandlers.add(\"addTask\", addTaskProcessor)\nHandlers.add(\"updateTask\", updateTaskProcessor)\nHandlers.add(\"getTasks\", getTasksProcessor)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"addTask\", async () => {\n    await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Test Task\",\n        description: \"Test Description\",\n      }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n});\n\n</EXISTING_TESTS>\n<ideal_output>\n  test(\"updateTask\", async () => {\n    await env.send({\n      Action: \"updateTask\",\n      Data: JSON.stringify({ id: 1, status: \"[X]\" }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n  test(\"getTasks\", async () => {\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n</ideal_output>\n</example>\n</examples>\n\n"),
        ell.user(f"You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests.\n\nFirst, examine the following Lua code:\n\n<lua_code>\n{lua_code}\n</lua_code>\n\nNow, review the existing TypeScript tests:\n\n<existing_tests>\n{existing_tests}\n</existing_tests>\n\nYour goal is to generate new TypeScript tests for the Lua code provided. Follow these guidelines:\n\n1. Focus on testing handlers in the Lua code.\n2. Ensure tests are comprehensive but do not duplicate existing tests.\n3. Follow TypeScript and existing test patterns.\n4. Be idempotent - only add new tests for new Lua code, not for code that already has tests.\n5. Maintain the existing test file structure.\n\nGenerate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself. If the already provided test's are fulfilling output None.\n\nProvide your output in the following format:\n\n<new_tests>\n[Insert only the new TypeScript test code here]\n</new_tests>\n\nRemember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers ")
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