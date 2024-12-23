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