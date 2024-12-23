simple_example = """
<examples>
<example>
<LUA_CODE>
counter = 0


function sendReply(msg, data)
    msg.reply({Data = data, Action = msg.Action .. "Response"})
end


function incrementCounter(msg)
    counter = counter + 1
    sendReply(msg, counter)
end

function decrementCounter(msg)
    counter = counter - 1
    sendReply(msg, counter)
end

function getCounter(msg)
    sendReply(msg, counter)
end


Handlers.add("incrementCounter", incrementCounter)
Handlers.add("decrementCounter", decrementCounter)
Handlers.add("getCounter", getCounter)
</LUA_CODE>
<EXISTING_TESTS>
import aos from "./aos";
import fs from "fs";
import path from "node:path";
import assert from "node:assert";
import { describe, test, before } from "node:test";

describe("Counter Tests", () => {
  let env: aos;

  before(async () => {
    const source = fs.readFileSync(
      path.join(__dirname, "../../process/build/output.lua"),
      "utf-8"
    );
    env = new aos(source);
    await env.init();
  });

  test("should initialize counter at 0", async () => {
    const response = await env.send({ Action: "getCounter" });
    assert.equal(response.Messages[0].Data, 0);
  });

  test("should increment counter", async () => {
    const response = await env.send({ Action: "incrementCounter" });
    assert.equal(response.Messages[0].Data, 1);
  });


});
</EXISTING_TESTS>
<ideal_output>
<test_planning>
1. Handlers identified:
- incrementCounter
- decrementCounter
- getCounter

2. Handlers needing tests:
- decrementCounter (no tests exist)
- getCounter (only basic initialization test exists)
- incrementCounter (only single increment test exists)

3. Test scenarios needed:
decrementCounter:
- Basic decrement functionality
- Verify negative numbers work

getCounter:
- Verify counter value after multiple operations

incrementCounter:
- Verify multiple increments

4. Number of new tests to generate: 4 tests

</test_planning>

<new_tests>
test("should decrement counter", async () => {
  const response = await env.send({ Action: "decrementCounter" });
  assert.equal(response.Messages[0].Data, 0);
});

test("should handle negative numbers when decrementing", async () => {
  const response = await env.send({ Action: "decrementCounter" });
  assert.equal(response.Messages[0].Data, -1);
});

test("should maintain correct counter value after multiple operations", async () => {
  await env.send({ Action: "incrementCounter" });
  await env.send({ Action: "incrementCounter" });
  await env.send({ Action: "decrementCounter" });
  const response = await env.send({ Action: "getCounter" });
  assert.equal(response.Messages[0].Data, 0);
});

test("should handle multiple increments correctly", async () => {
  await env.send({ Action: "incrementCounter" });
  await env.send({ Action: "incrementCounter" });
  const response = await env.send({ Action: "incrementCounter" });
  assert.equal(response.Messages[0].Data, 3);
});
</new_tests>
</ideal_output>
</example>
<example>
<LUA_CODE>
local json = require("json")

-- Task list storage
local tasks = {}

-- Task status constants
local STATUS = {
    PENDING = "[ ]",
    COMPLETED = "[X]"
}



function sendReply(msg, data)
    msg.reply({Data = data, Action = msg.Action .. "Response"})
end

function findTaskById(id)
    for _, task in ipairs(tasks) do
        if task.id == id then
            return task
        end
    end
    return nil
end


function addTaskProcessor(msg)
    local data = json.decode(msg.Data)
    local task = {
        id = #tasks + 1,
        title = data.title,
        description = data.description,
        status = STATUS.PENDING,
    }
    table.insert(tasks, task)
    sendReply(msg, task)
end

function updateTaskProcessor(msg)
    local data = json.decode(msg.Data)
    local task = findTaskById(data.id)
    if not task then
        error("Task not found")
    end
    task.status = data.status
    sendReply(msg, task)
end


function getTasksProcessor(msg)
    sendReply(msg, tasks)
end




Handlers.add("addTask", addTaskProcessor)
Handlers.add("updateTask", updateTaskProcessor)
Handlers.add("getTasks", getTasksProcessor)
</LUA_CODE>
<EXISTING_TESTS>
import aos from "./aos";
import fs from "fs";
import path from "node:path";
import assert from "node:assert";
import { describe, test, before } from "node:test";

describe("Counter Tests", () => {
  let env: aos;

  before(async () => {
    const source = fs.readFileSync(
      path.join(__dirname, "../../process/build/output.lua"),
      "utf-8"
    );
    env = new aos(source);
    await env.init();
  });

  test("addTask", async () => {
    await env.send({
      Action: "addTask",
      Data: JSON.stringify({
        title: "Test Task",
        description: "Test Description",
      }),
    });
    const response = await env.send({ Action: "getTasks" });
    console.log(response.Messages[0].Data);
  });

});
</EXISTING_TESTS>
<ideal_output>
<test_planning>
1. Handlers identified in Lua code:
- addTask
- updateTask
- getTasks

2. Handlers needing new tests:
- addTask (needs more comprehensive tests)
- updateTask (completely uncovered)
- getTasks (needs standalone tests)

3. Test scenarios needed:
For addTask:
- Verify task properties after addition
- Verify incremental ID assignment

For updateTask:
- Update task status to completed
- Test with non-existent task ID
- Verify task properties remain unchanged except status

For getTasks:
- Get empty task list
- Get multiple tasks
- Verify task list structure

4. Number of new tests to generate: 6 tests

</test_planning>

<new_tests>
test("should create task with correct properties", async () => {
  const response = await env.send({
    Action: "addTask",
    Data: JSON.stringify({
      title: "Test Task",
      description: "Test Description",
    }),
  });
  assert.strictEqual(response.Messages[0].Data.id, 1);
  assert.strictEqual(response.Messages[0].Data.title, "Test Task");
  assert.strictEqual(response.Messages[0].Data.description, "Test Description");
  assert.strictEqual(response.Messages[0].Data.status, "[ ]");
});

test("should update task status", async () => {
  await env.send({
    Action: "addTask",
    Data: JSON.stringify({
      title: "Update Test",
      description: "Test Description",
    }),
  });
  
  const response = await env.send({
    Action: "updateTask",
    Data: JSON.stringify({
      id: 1,
      status: "[X]"
    }),
  });
  assert.strictEqual(response.Messages[0].Data.status, "[X]");
});

test("should throw error when updating non-existent task", async () => {
  try {
    await env.send({
      Action: "updateTask",
      Data: JSON.stringify({
        id: 999,
        status: "[X]"
      }),
    });
    assert.fail("Should have thrown an error");
  } catch (error) {
    assert.strictEqual(error.message.includes("Task not found"), true);
  }
});

test("should get empty task list initially", async () => {
  const response = await env.send({ Action: "getTasks" });
  assert.deepStrictEqual(response.Messages[0].Data, []);
});

test("should get multiple tasks", async () => {
  await env.send({
    Action: "addTask",
    Data: JSON.stringify({
      title: "Task 1",
      description: "Description 1",
    }),
  });
  
  await env.send({
    Action: "addTask",
    Data: JSON.stringify({
      title: "Task 2",
      description: "Description 2",
    }),
  });
  
  const response = await env.send({ Action: "getTasks" });
  assert.strictEqual(response.Messages[0].Data.length, 2);
  assert.strictEqual(response.Messages[0].Data[0].title, "Task 1");
  assert.strictEqual(response.Messages[0].Data[1].title, "Task 2");
});

test("should assign incremental IDs to tasks", async () => {
  const response1 = await env.send({
    Action: "addTask",
    Data: JSON.stringify({
      title: "Task A",
      description: "Description A",
    }),
  });
  
  const response2 = await env.send({
    Action: "addTask",
    Data: JSON.stringify({
      title: "Task B",
      description: "Description B",
    }),
  });
  
  assert.strictEqual(response2.Messages[0].Data.id, response1.Messages[0].Data.id + 1);
});
</new_tests>
</ideal_output>
</example>
</examples>
"""