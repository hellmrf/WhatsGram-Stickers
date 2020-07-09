# Comment the following line to run migrations
exit()

from db import DB

with DB() as db:
    db.cursor.execute("CREATE TABLE users ( id serial, chat_id character varying(32), package_name character varying("
                      "64), stage smallint, package_title character varying(64), telegram_id integer, PRIMARY KEY ("
                      "id), UNIQUE (chat_id));")
