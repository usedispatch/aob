class Examples:
    """Class containing example code snippets used in prompts"""
    
simple_example = """
<examples>\n<example>\n<LUA_CODE>\ncounter = 0\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\n\nfunction incrementCounter(msg)\n    counter = counter + 1\n    sendReply(msg, counter)\nend\n\nfunction decrementCounter(msg)\n    counter = counter - 1\n    sendReply(msg, counter)\nend\n\nfunction getCounter(msg)\n    sendReply(msg, counter)\nend\n\n\nHandlers.add(\"incrementCounter\", incrementCounter)\nHandlers.add(\"decrementCounter\", decrementCounter)\nHandlers.add(\"getCounter\", getCounter)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"should initialize counter at 0\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should increment counter\", async () => {\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n\n});\n</EXISTING_TESTS>\n<ideal_output>\n<test_planning>\n1. Handlers in Lua code:\n- incrementCounter\n- decrementCounter\n- getCounter\n\n2. Handlers covered by existing tests:\n- getCounter (initial value test)\n- incrementCounter (single increment test)\n\n3. Handlers needing new tests:\n- decrementCounter (no tests)\n- incrementCounter (needs additional scenarios)\n- getCounter (needs additional verification after modifications)\n\n4. Test scenarios needed:\n- decrementCounter:\n  * Basic decrement functionality\n  * Verify negative numbers work\n- incrementCounter:\n  * Multiple increments\n  * Verify state persistence\n- getCounter:\n  * Verify after decrement\n  * Verify after multiple operations\n\n5. Number of new tests to generate: 6\n\nThe new tests will verify the complete functionality of the counter system, including:\n- Decrement operations\n- Multiple operations in sequence\n- State consistency across different handler calls\n</test_planning>\n\n<new_tests>\n  test(\"should decrement counter\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Data, 0);\n  });\n\n  test(\"should handle negative numbers when decrementing\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Data, -1);\n  });\n\n  test(\"should maintain state across multiple increments\", async () => {\n    await env.send({ Action: \"incrementCounter\" });\n    const response = await env.send({ Action: \"incrementCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n  test(\"should verify counter state with getCounter\", async () => {\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 1);\n  });\n\n  test(\"should handle mixed increment and decrement operations\", async () => {\n    await env.send({ Action: \"incrementCounter\" });\n    await env.send({ Action: \"incrementCounter\" });\n    await env.send({ Action: \"decrementCounter\" });\n    const response = await env.send({ Action: \"getCounter\" });\n    assert.equal(response.Messages[0].Data, 2);\n  });\n\n  test(\"should verify correct response action names\", async () => {\n    const response = await env.send({ Action: \"decrementCounter\" });\n    assert.equal(response.Messages[0].Action, \"decrementCounterResponse\");\n  });\n</new_tests>\n</ideal_output>\n</example>\n<example>\n<LUA_CODE>\nlocal json = require(\"json\")\n\n-- Task list storage\nlocal tasks = {}\n\n-- Task status constants\nlocal STATUS = {\n    PENDING = \"[ ]\",\n    COMPLETED = \"[X]\"\n}\n\n\n\nfunction sendReply(msg, data)\n    msg.reply({Data = data, Action = msg.Action .. \"Response\"})\nend\n\nfunction findTaskById(id)\n    for _, task in ipairs(tasks) do\n        if task.id == id then\n            return task\n        end\n    end\n    return nil\nend\n\n\nfunction addTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = {\n        id = #tasks + 1,\n        title = data.title,\n        description = data.description,\n        status = STATUS.PENDING,\n    }\n    table.insert(tasks, task)\n    sendReply(msg, task)\nend\n\nfunction updateTaskProcessor(msg)\n    local data = json.decode(msg.Data)\n    local task = findTaskById(data.id)\n    if not task then\n        error(\"Task not found\")\n    end\n    task.status = data.status\n    sendReply(msg, task)\nend\n\n\nfunction getTasksProcessor(msg)\n    sendReply(msg, tasks)\nend\n\n\n\n\nHandlers.add(\"addTask\", addTaskProcessor)\nHandlers.add(\"updateTask\", updateTaskProcessor)\nHandlers.add(\"getTasks\", getTasksProcessor)\n</LUA_CODE>\n<EXISTING_TESTS>\nimport aos from \"./aos\";\nimport fs from \"fs\";\nimport path from \"node:path\";\nimport assert from \"node:assert\";\nimport { describe, test, before } from \"node:test\";\n\ndescribe(\"Counter Tests\", () => {\n  let env: aos;\n\n  before(async () => {\n    const source = fs.readFileSync(\n      path.join(__dirname, \"../../process/build/output.lua\"),\n      \"utf-8\"\n    );\n    env = new aos(source);\n    await env.init();\n  });\n\n  test(\"addTask\", async () => {\n    await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Test Task\",\n        description: \"Test Description\",\n      }),\n    });\n    const response = await env.send({ Action: \"getTasks\" });\n    console.log(response.Messages[0].Data);\n  });\n\n});\n</EXISTING_TESTS>\n<ideal_output>\n<test_planning>\n1. Handlers in Lua code:\n- addTask\n- updateTask\n- getTasks\n\n2. Handlers covered by existing tests:\n- addTask (basic test exists)\n- getTasks (partially covered as part of addTask test)\n\n3. Handlers needing new tests:\n- updateTask (no coverage)\n- Additional scenarios for getTasks\n- More comprehensive scenarios for addTask\n\n4. Test scenarios needed:\nFor updateTask:\n- Update task status to completed\n- Attempt to update non-existent task\n- Verify task status change\n\nFor getTasks:\n- Get empty task list\n- Get multiple tasks\n\nFor addTask (additional coverage):\n- Add multiple tasks\n- Verify task ID increment\n\n5. Number of new tests to generate: 5\n\nThe existing tests only cover basic addTask functionality. We need to add comprehensive tests for updateTask and additional scenarios for the other handlers.\n</test_planning>\n\n<new_tests>\n  test(\"should get empty task list initially\", async () => {\n    const response = await env.send({ Action: \"getTasks\" });\n    assert.deepStrictEqual(response.Messages[0].Data, []);\n  });\n\n  test(\"should add multiple tasks\", async () => {\n    const task1 = await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"First Task\",\n        description: \"First Description\",\n      }),\n    });\n    const task2 = await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Second Task\",\n        description: \"Second Description\",\n      }),\n    });\n\n    const response = await env.send({ Action: \"getTasks\" });\n    assert.equal(response.Messages[0].Data.length, 2);\n    assert.equal(response.Messages[0].Data[0].id, 1);\n    assert.equal(response.Messages[0].Data[1].id, 2);\n  });\n\n  test(\"should update task status\", async () => {\n    const addResponse = await env.send({\n      Action: \"addTask\",\n      Data: JSON.stringify({\n        title: \"Update Test\",\n        description: \"Test Description\",\n      }),\n    });\n    \n    const taskId = addResponse.Messages[0].Data.id;\n    \n    const updateResponse = await env.send({\n      Action: \"updateTask\",\n      Data: JSON.stringify({\n        id: taskId,\n        status: \"[X]\"\n      }),\n    });\n\n    assert.equal(updateResponse.Messages[0].Data.status, \"[X]\");\n  });\n\n  test(\"should fail when updating non-existent task\", async () => {\n    try {\n      await env.send({\n        Action: \"updateTask\",\n        Data: JSON.stringify({\n          id: 999,\n          status: \"[X]\"\n        }),\n      });\n      assert.fail(\"Should have thrown an error\");\n    } catch (error) {\n      assert.ok(error.message.includes(\"Task not found\"));\n    }\n  });\n\n  test(\"should maintain task list state\", async () => {\n    const getResponse = await env.send({ Action: \"getTasks\" });\n    const tasks = getResponse.Messages[0].Data;\n    \n    // Verify the state includes previously added tasks\n    assert.ok(tasks.length > 0);\n    assert.ok(tasks.some(task => task.status === \"[X]\"));\n  });\n</new_tests>\n</ideal_output>\n</example>\n</examples>\n\n
"""

sqlite_example = """<examples>
<example>
<LUA_CODE>
local sqlite3 = require("lsqlite3")
local json = require("json")
DB = DB or sqlite3.open_memory()
DbAdmin = require('DbAdmin').new(DB)

-- Table definitions
AUTHORS = [[
    CREATE TABLE IF NOT EXISTS Authors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
]]

POSTS = [[
    CREATE TABLE IF NOT EXISTS Posts (
        id TEXT PRIMARY KEY,
        author_id TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        published_at INTEGER DEFAULT (strftime('%s', 'now')),
        FOREIGN KEY (author_id) REFERENCES Authors(id)
    );
]]

function Configure()
    DbAdmin:exec(AUTHORS)
    DbAdmin:exec(POSTS)
    Configured = true
end

if not Configured then Configure() end


function sendReply(msg, data)
    msg.reply({Data = data, Action = msg.Action .. "Response"})
end

function addAuthor(data)
    DbAdmin:apply(
        'INSERT INTO Authors (id, name, email) VALUES (?, ?, ?)',
        {
            data.id,
            data.name,
            data.email
        }
    )
end

function addPost(data)
    DbAdmin:apply(
        'INSERT INTO Posts (id, author_id, title, content) VALUES (?, ?, ?, ?)',
        {
            data.id,
            data.author_id,
            data.title,
            data.content
        }
    )
end

function getPosts()
    local results = DbAdmin:exec([[
        SELECT Posts.*, Authors.name as author_name 
        FROM Posts 
        JOIN Authors ON Posts.author_id = Authors.id
        ORDER BY published_at DESC;
    ]])
    return json.encode(results)
end

function updatePost(data)
    DbAdmin:apply(
        'UPDATE Posts SET title = ?, content = ? WHERE id = ?',
        {
            data.title,
            data.content,
            data.id
        }
    )
end

function deletePost(id)
    DbAdmin:apply('DELETE FROM Posts WHERE id = ?', {id})
end





-- Processor functions for Authors
function addAuthorProcessor(msg)
    local data = json.decode(msg.Data)
    addAuthor(data)
    sendReply(msg, data)
end

-- Processor functions for Posts
function addPostProcessor(msg)
    local data = json.decode(msg.Data)
    addPost(data)
    sendReply(msg, data)
end

function getPostsProcessor(msg)
    local data = getPosts()
    print(data)
    sendReply(msg, data)
end

function updatePostProcessor(msg)
    local data = json.decode(msg.Data)
    updatePost(data)
    sendReply(msg, data)
end

function deletePostProcessor(msg)
    local data = json.decode(msg.Data)
    deletePost(data.id)
    sendReply(msg, {success = true})
end

-- Register handlers
Handlers.add("AddAuthor", addAuthorProcessor)
Handlers.add("AddPost", addPostProcessor)
Handlers.add("GetPosts", getPostsProcessor)
Handlers.add("UpdatePost", updatePostProcessor)
Handlers.add("DeletePost", deletePostProcessor)
</LUA_CODE>
<EXISTING_TESTS>
import aos from "./aos";
import fs from "fs";
import path from "node:path";
import assert from "node:assert";
import { describe, test, before, todo } from "node:test";

describe("Tests", () => {
  let env: aos;

  before(async () => {
    const source = fs.readFileSync(
      path.join(__dirname, "../../process/build/output.lua"),
      "utf-8"
    );
    env = new aos(source);
    await env.init();
  });

  test("load DbAdmin module", async () => {
    const dbAdminCode = fs.readFileSync(
      path.join(__dirname, "../../process/build/dbAdmin.lua"),
      "utf-8"
    );
    const result = await env.send({
      Action: "Eval",
      Data: `
  local function _load() 
    ${dbAdminCode}
  end
  _G.package.loaded["DbAdmin"] = _load()
  return "ok"
      `,
    });
    console.log("result DbAdmin Module", result);
    assert.equal(result.Output.data, "ok");
  });

  test("load source", async () => {
    const code = fs.readFileSync(
      path.join(__dirname, "../../process/build/output.lua"),
      "utf-8"
    );
    const result = await env.send({ Action: "Eval", Data: code });
    console.log("result load source", result);
    // assert.equal(result.Output.data, "OK");
  });

  test("should add Author", async () => {
    const author = {
      id: "1",
      name: "Test Author",
      email: "test@author.com",
    };

    const response = await env.send({
      Action: "AddAuthor",
      Data: JSON.stringify(author),
    });

    console.log("add author", response.Messages);
  });

  test("should add post", async () => {
    const post = {
      id: "1",
      title: "Test Post",
      content: "Test Content",
      author_id: "1",
    };
    const response = await env.send({
      Action: "AddPost",
      Data: JSON.stringify(post),
    });
    console.log("add post", response.Messages);
  });

  test("should get posts", async () => {
    const response = await env.send({ Action: "GetPosts" });
    console.log("get posts", response.Messages);
  });
});

</EXISTING_TESTS>
<ideal_output>
  test("should update post", async () => {
    const updatedPost = {
      id: "1",
      title: "Updated Test Post",
      content: "Updated Test Content",
    };

    const response = await env.send({
      Action: "UpdatePost",
      Data: JSON.stringify(updatedPost),
    });

    console.log("update post", response.Messages);
  });
  test("should get posts after update", async () => {
    const response = await env.send({ Action: "GetPosts" });
    console.log("get posts after update", response.Messages);
  });
  test("should delete post", async () => {
    const deletePost = {
      id: "1",
    };
    const response = await env.send({
      Action: "DeletePost",
      Data: JSON.stringify(deletePost),
    });

    console.log("delete post", response.Messages);
  });
  test("should get posts after deletion", async () => {
    const response = await env.send({ Action: "GetPosts" });
    console.log("get posts after deletion", response.Messages);
  });
</ideal_output>
</example>
</examples>
"""

