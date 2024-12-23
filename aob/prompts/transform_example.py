def convert_escaped_newlines(input_string: str) -> str:
    """
    Converts escaped newlines (\n) in a string to actual newlines.
    
    Args:
        input_string (str): String containing escaped newlines
        
    Returns:
        str: String with actual newlines
    """
    # First, handle any double backslashes to prevent issues
    input_string = input_string.replace('\\\\', '\\')
    
    # Convert \n to actual newlines
    return input_string.encode().decode('unicode_escape')

if __name__ == "__main__":
    # Example usage
    example_input = "<examples>\n<example>\n<LUA_CODE>\ncounter = 0\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\n\nfunction incrementCounter(msg)\n    counter = counter + 1\n    sendReply(msg, counter)\nend\n\nfunction decrementCounter(msg)\n    counter = counter - 1\n    sendReply(msg, counter)\nend\n\nfunction getCounter(msg)\n    sendReply(msg, counter)\nend\n\n\nHandlers.add(\"incrementCounter\", incrementCounter)\nHandlers.add(\"decrementCounter\", decrementCounter)\nHandlers.add(\"getCounter\", getCounter)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n\n});\n</EXISTING_TESTS>\n<ideal_output>\n<test_planning>\n1. Handlers identified:\n- incrementCounter\n- decrementCounter\n- getCounter\n\n2. Handlers needing tests:\n- decrementCounter (no tests exist)\n- getCounter (only basic initialization test exists)\n- incrementCounter (only single increment test exists)\n\n3. Test scenarios needed:\ndecrementCounter:\n- Basic decrement functionality\n- Verify negative numbers work\n\ngetCounter:\n- Verify counter value after multiple operations\n\nincrementCounter:\n- Verify multiple increments\n\n4. Number of new tests to generate: 4 tests\n\n</test_planning>\n\n<new_tests>\ntest(\"should decrement counter\", async () => {\n  const response = await env.send({ Action: \"decrementCounter\" });\n  assert.equal(response.Messages[0].Data, 0);\n});\n\ntest(\"should handle negative numbers when decrementing\", async () => {\n  const response = await env.send({ Action: \"decrementCounter\" });\n  assert.equal(response.Messages[0].Data, -1);\n});\n\ntest(\"should maintain correct counter value after multiple operations\", async () => {\n  await env.send({ Action: \"incrementCounter\" });\n  await env.send({ Action: \"incrementCounter\" });\n  await env.send({ Action: \"decrementCounter\" });\n  const response = await env.send({ Action: \"getCounter\" });\n  assert.equal(response.Messages[0].Data, 0);\n});\n\ntest(\"should handle multiple increments correctly\", async () => {\n  await env.send({ Action: \"incrementCounter\" });\n  await env.send({ Action: \"incrementCounter\" });\n  const response = await env.send({ Action: \"incrementCounter\" });\n  assert.equal(response.Messages[0].Data, 3);\n});\n</new_tests>\n</ideal_output>\n</example>\n<example>\n<LUA_CODE>\nlocal json = require(\"json\")\n\n-- Task list storage\nlocal tasks = {}\n\n-- Task status constants\nlocal STATUS = {\n    PENDING = \"[ ]\",\n    COMPLETED = \"[X]\"\n}\n\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\nfunction findTaskById(id)\n    for _, task in ipairs(tasks) do\n        if task.id == id then\n            return task\n        end\n    end\n    return nil\nend\n\n\nfunction addTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = {\n        id = #tasks + 1,\n        title = data.title,\n        description = data.description,\n        status = STATUS.PENDING,\n    }\n    table.insert(tasks, task)\n    sendReply(msg, task)\nend\n\nfunction updateTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = findTaskById(data.id)\n    if not task then\n        error(\"Task not found\")\n    end\n    task.status = data.status\n    sendReply(msg, task)\nend\n\n\nfunction getTasksProcessor(msg)\n    sendReply(msg, tasks)\nend\n\n\n\n\nHandlers.add(\"addTask\", addTaskProcessor)\nHandlers.add(\"updateTask\", updateTaskProcessor)\nHandlers.add(\"getTasks\", getTasksProcessor)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"addTask\", async () => {\n    await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Test Task\",\n        description: \"Test Description\",\n      }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n});\n</EXISTING_TESTS>\n<ideal_output>\n<test_planning>\n1. Handlers identified in Lua code:\n- addTask\n- updateTask\n- getTasks\n\n2. Handlers needing new tests:\n- addTask (needs more comprehensive tests)\n- updateTask (completely uncovered)\n- getTasks (needs standalone tests)\n\n3. Test scenarios needed:\nFor addTask:\n- Verify task properties after addition\n- Verify incremental ID assignment\n\nFor updateTask:\n- Update task status to completed\n- Test with non-existent task ID\n- Verify task properties remain unchanged except status\n\nFor getTasks:\n- Get empty task list\n- Get multiple tasks\n- Verify task list structure\n\n4. Number of new tests to generate: 6 tests\n\n</test_planning>\n\n<new_tests>\ntest(\"should create task with correct properties\", async () => {\n  const response = await env.send({\n    Action: \"addTask\",\n    Data: JSON.stringify({\n      title: \"Test Task\",\n      description: \"Test Description\",\n    }),\n  });\n  assert.strictEqual(response.Messages[0].Data.id, 1);\n  assert.strictEqual(response.Messages[0].Data.title, \"Test Task\");\n  assert.strictEqual(response.Messages[0].Data.description, \"Test Description\");\n  assert.strictEqual(response.Messages[0].Data.status, \"[ ]\");\n});\n\ntest(\"should update task status\", async () => {\n  await env.send({\n    Action: \"addTask\",\n    Data: JSON.stringify({\n      title: \"Update Test\",\n      description: \"Test Description\",\n    }),\n  });\n  \n  const response = await env.send({\n    Action: \"updateTask\",\n    Data: JSON.stringify({\n      id: 1,\n      status: \"[X]\"\n    }),\n  });\n  assert.strictEqual(response.Messages[0].Data.status, \"[X]\");\n});\n\ntest(\"should throw error when updating non-existent task\", async () => {\n  try {\n    await env.send({\n      Action: \"updateTask\",\n      Data: JSON.stringify({\n        id: 999,\n        status: \"[X]\"\n      }),\n    });\n    assert.fail(\"Should have thrown an error\");\n  } catch (error) {\n    assert.strictEqual(error.message.includes(\"Task not found\"), true);\n  }\n});\n\ntest(\"should get empty task list initially\", async () => {\n  const response = await env.send({ Action: \"getTasks\" });\n  assert.deepStrictEqual(response.Messages[0].Data, []);\n});\n\ntest(\"should get multiple tasks\", async () => {\n  await env.send({\n    Action: \"addTask\",\n    Data: JSON.stringify({\n      title: \"Task 1\",\n      description: \"Description 1\",\n    }),\n  });\n  \n  await env.send({\n    Action: \"addTask\",\n    Data: JSON.stringify({\n      title: \"Task 2\",\n      description: \"Description 2\",\n    }),\n  });\n  \n  const response = await env.send({ Action: \"getTasks\" });\n  assert.strictEqual(response.Messages[0].Data.length, 2);\n  assert.strictEqual(response.Messages[0].Data[0].title, \"Task 1\");\n  assert.strictEqual(response.Messages[0].Data[1].title, \"Task 2\");\n});\n\ntest(\"should assign incremental IDs to tasks\", async () => {\n  const response1 = await env.send({\n    Action: \"addTask\",\n    Data: JSON.stringify({\n      title: \"Task A\",\n      description: \"Description A\",\n    }),\n  });\n  \n  const response2 = await env.send({\n    Action: \"addTask\",\n    Data: JSON.stringify({\n      title: \"Task B\",\n      description: \"Description B\",\n    }),\n  });\n  \n  assert.strictEqual(response2.Messages[0].Data.id, response1.Messages[0].Data.id + 1);\n});\n</new_tests>\n</ideal_output>\n</example>\n</examples>\n\n"
    
    formatted = convert_escaped_newlines(example_input)
    with open('formatted_output.txt', 'w', encoding='utf-8') as f:
        f.write(formatted)