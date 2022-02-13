method = GetMethod()

function parseTopic(row)
   topic = {id=row.id,
            name=row.name,
            description=row.description,
            board_id=row.board_id,
            created_user=row.created_user,
            created_dttm=row.created_dttm,
            updated_user=row.updated_user,
            updated_dttm=row.updated_dttm,
            delete_flg=row.delete_flg}
   return topic
end

if method == "GET" then
   results = {}
   if HasParam("id") then
      id = GetParam("id")
      for row in db:nrows("SELECT * from topics where delete_flg=0 and id='" .. id .. "'") do
         results = parseTopic(row)
      end
   elseif HasParam("board_id") then
      board_id = GetParam("board_id")
      for row in db:nrows("SELECT * from topics where delete_flg=0 and board_id='" .. board_id .. "'") do
         topic = parseTopic(row)
         results[#results+1] = topic
      end
   else
      for row in db:nrows("SELECT * from topics where delete_flg=0") do
         topic = parseTopic(row)
         results[#results+1] = topic
      end
   end
   Write(json.encode(results))

elseif method == "POST" then
   name = GetParam("name")
   description = GetParam("description")
   board_id = GetParam("board_id")
   user = GetParam("user")
   sql = [[
    INSERT INTO topics (name, description, board_id, created_user, created_dttm,
                        updated_user, updated_dttm, delete_flg)
      VALUES (']] .. name .. [['
            , ']] .. description .. [['
            , ']] .. board_id .. [['
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
   board_id = GetParam("board_id")
   user = GetParam("user")
   sql = [[UPDATE topics set name=']] .. name ..[['
          , description=']] .. description .. [['
          , board_id=']] .. board_id .. [['
          , updated_user=']] .. user .. [['
          , updated_dttm=datetime('now')
          where id=]] .. id
          db:exec(sql)

elseif method == "DELETE" then
   if HasParam("id") then
      id = GetParam("id")
      sql = [[UPDATE topics set name='updated', delete_flg=1 where id=]] .. id
   else
      sql = [[DELETE from topics]]
   end
   db:exec(sql)
end
