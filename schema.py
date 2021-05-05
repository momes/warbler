# USERS
#                                  Table "public.users"
#       Column      |  Type   | Collation | Nullable |              Default              
# ------------------+---------+-----------+----------+-----------------------------------
#  id               | integer |           | not null | nextval('users_id_seq'::regclass)
#  email            | text    |           | not null | 
#  username         | text    |           | not null | 
#  image_url        | text    |           |          | 
#  header_image_url | text    |           |          | 
#  bio              | text    |           |          | 
#  location         | text    |           |          | 
#  password         | text    |           | not null | 
# Indexes:
#     "users_pkey" PRIMARY KEY, btree (id)
#     "users_email_key" UNIQUE CONSTRAINT, btree (email)
#     "users_username_key" UNIQUE CONSTRAINT, btree (username)
# Referenced by:
#     TABLE "follows" CONSTRAINT "follows_user_being_followed_id_fkey" FOREIGN KEY (user_being_followed_id) REFERENCES users(id) ON DELETE CASCADE
#     TABLE "follows" CONSTRAINT "follows_user_following_id_fkey" FOREIGN KEY (user_following_id) REFERENCES users(id) ON DELETE CASCADE
#     TABLE "messages" CONSTRAINT "messages_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE


# FOLLOWS
# Table "public.follows"
#          Column         |  Type   | Collation | Nullable | Default 
# ------------------------+---------+-----------+----------+---------
#  user_being_followed_id | integer |           | not null | 
#  user_following_id      | integer |           | not null | 
# Indexes:
#     "follows_pkey" PRIMARY KEY, btree (user_being_followed_id, user_following_id)
# Foreign-key constraints:
#     "follows_user_being_followed_id_fkey" FOREIGN KEY (user_being_followed_id) REFERENCES users(id) ON DELETE CASCADE
#     "follows_user_following_id_fkey" FOREIGN KEY (user_following_id) REFERENCES users(id) ON DELETE CASCADE

#MESSAGES
#                                        Table "public.messages"
#   Column   |            Type             | Collation | Nullable |               Default                
# -----------+-----------------------------+-----------+----------+--------------------------------------
#  id        | integer                     |           | not null | nextval('messages_id_seq'::regclass)
#  text      | character varying(140)      |           | not null | 
#  timestamp | timestamp without time zone |           | not null | 
#  user_id   | integer                     |           | not null | 
# Indexes:
#     "messages_pkey" PRIMARY KEY, btree (id)
# Foreign-key constraints:
#     "messages_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

#LIKES
#                  Table "public.likes"
#    Column   |  Type   | Collation | Nullable | Default 
# ------------+---------+-----------+----------+---------
#  user_id    | integer |           | not null | 
#  message_id | integer |           | not null | 
# Indexes:
#     "likes_pkey" PRIMARY KEY, btree (user_id, message_id)
# Foreign-key constraints:
#     "likes_message_id_fkey" FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
#     "likes_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE