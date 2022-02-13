method = GetMethod()

function parsePost(row)
   post  = {id=row.id,
            name=row.name,
            description=row.description,
            topic_id=row.topic_id,
            parent_post_id=row.parent_post_id,
            created_user=row.created_user,
            created_dttm=row.created_dttm,
            updated_user=row.updated_user,
            updated_dttm=row.updated_dttm,
            delete_flg=row.delete_flg}
   return post
end

if method == "GET" then
   results = {}
   if HasParam("id") then
      id = GetParam("id")
      for row in db:nrows("SELECT * from posts where delete_flg=0 and id='" .. id .. "'") do
         results = parsePost(row)
      end
   elseif HasParam("topic_id") then
      board_id = GetParam("topic_id")
      for row in db:nrows("SELECT * from posts where delete_flg=0 and topic_id='" .. board_id .. "'") do
         post = parsePost(row)
         results[#results+1] = post
      end
   else
      for row in db:nrows("SELECT * from posts where delete_flg=0") do
         post = parseTopic(row)
         results[#results+1] = post
      end
   end
   Write(json.encode(results))

elseif method == "POST" then
   name = GetParam("name")
   description = GetParam("description")
   topic_id = GetParam("topic_id")
   parent_post_id = GetParam("parent_post_id")
   user = GetParam("user")
   sql = [[
    INSERT INTO posts (name, description, topic_id, parent_post_id, created_user, created_dttm,
                        updated_user, updated_dttm, delete_flg)
      VALUES (']] .. name .. [['
            , ']] .. description .. [['
            , ]] .. topic_id .. [[
            , ]] .. parent_post_id .. [[
            , ']] .. user .. [['
            , datetime('now')
            , ']] .. user .. [['
            , datetime('now'), 0)]]
            db:exec(sql)
            Write(db:last_insert_rowid())

elseif method == "PUT" then
   id = GetParam("id")
   name = GetParam("name")
   description = GetParam("description")
   topic_id = GetParam("topic_id")
   parent_post_id = GetParam("parent_post_id")
   user = GetParam("user")
   sql = [[UPDATE posts set name=']] .. name ..[['
          , description=']] .. description .. [['
          , topic_id=]] .. topic_id .. [[
          , parent_post_id=]] .. parent_post_id .. [[ 
          , updated_user=']] .. user .. [['
          , updated_dttm=datetime('now')
          where id=]] .. id
          db:exec(sql)

elseif method == "DELETE" then
   if HasParam("id") then
      id = GetParam("id")
      sql = [[UPDATE posts set delete_flg=1 where id=]] .. id
   else
      sql = [[DELETE from posts]]
   end
   db:exec(sql)
end
