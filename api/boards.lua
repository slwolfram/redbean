method = GetMethod()

function parseBoard(row)
   board = {id=row.id,
            name=row.name,
            description=row.description,
            created_user=row.created_user,
            created_dttm=row.created_dttm,
            updated_user=row.updated_user,
            updated_dttm=row.updated_dttm,
            delete_flg=row.delete_flg}
   return board
end

if method == "GET" then
   results = {}
   if HasParam("id") then
      id = GetParam("id")
      for row in db:nrows("SELECT * from boards where delete_flg=0 and id='" .. id .. "'") do
         results = parseBoard(row)
      end
   else
      for row in db:nrows("SELECT * from boards where delete_flg=0") do
         board = parseBoard(row)
         results[#results+1] = board
      end
   end
   Write(json.encode(results))

elseif method == "POST" then
   name = GetParam("name")
   description = GetParam("description")
   user = GetParam("user")
   sql = [[
    INSERT INTO boards (name, description, created_user, created_dttm,
                        updated_user, updated_dttm, delete_flg)
      VALUES (']] .. name .. [['
            , ']] .. description .. [['
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
   user = GetParam("user")
   sql = [[UPDATE boards set name=']] .. name ..[['
          , description=']] .. description .. [['
          , updated_user=']] .. user .. [['
          , updated_dttm=datetime('now')
          where id=]] .. id
          db:exec(sql)

elseif method == "DELETE" then
   if HasParam("id") then
      id = GetParam("id")
      sql = [[UPDATE boards set name='updated', delete_flg=1 where id=]] .. id
   else
      sql = [[DELETE from boards]]
   end
   db:exec(sql)
end
