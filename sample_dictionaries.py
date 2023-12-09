user = {"users": {
    "john_doe": {
        "user_id":"john_doe+salt",
        "username": "john_doe",
        "key": "bytes",
        "email": "john@example.com",
        "level":"admin",
        "status":"Enabled",
        "chats":{
          "chat_room1":{
            "chat_name":"chat_room1",
            "security level":"Open",
            "access":{
                "read":True,
                "write":True
              }
            },
          "chat_room2":{
            "chat_name":"chat_room2",
            "security level":"Secret",
            "access":{
                "read":True,
                "write":True
              }
            }
          }
        },
    "jane_smith":{
        "user_id": "jane_smith+salt",
        "password": "secret456",
        "email": "jane@example.com",
        "level":"user",
        "status":"Disabled",
        "chats":{
          "chat_room1":{
            "security level":"Open",
            "access":{
                "read":True,
                "write":False
              }
            },
          "chat_room2":{
            "security level":"Secret",
            "access":{
                "read":False,
                "write":False
              }
            }
          }
        }
      }
    }

chats = {"chat_id":{"security level":{"password":{
        "members": [
          "user_id_1",
          "user_id_2",
          "user_id_3"
        ],
        "chat_history": {
          "message_id_1": {
            "id": "unique_message_id",
            "date": "2023-01-01T12:00:00",
            "sent_from": "user_id_1",
            "content": "Hello, how are you?"
          },
          "message_id_2": {
            "id": "unique_message_id",
            "date": "2023-01-01T12:05:00",
            "sent_from": "user_id_2",
            "content": "I'm good, thanks! How about you?"
          },
        },
        "message_count":"count"
      },
    }
  },
  "chat_name":"name",
  "creation_date":"date",
  "chat_description":"description"
}

