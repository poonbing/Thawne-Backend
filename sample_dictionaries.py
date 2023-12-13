user = {"users": {
    "john_doe": {
        "user_id":"john_doe+salt",
        "username": "john_doe",
        "password": "bytes",
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
        "username" :"Jane_bald",
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
          "message_count_1": {
            "id": "unique_message_id",
            "date": "2023-01-01T12:00:00",
            "sent_from": {"user_id_1":"username"},
            "content": "Hello, how are you?"
          },
          "message_count_2": {
                    "id":"new_message_id",
                    "date":"timestamp",
                    "sent_from":{"user_id":"username"},
                    "content":"message_content",
                    "file":{
                        "filename":"filename",
                        "file_url":"url",
                        "file_security":"security level",
                        "file_password":"key"
                    }
                },
        },
        "message_count":"count"
      },
    },
    "chat_name":"name",
    "creation_date":"date",
    "chat_description":"description",
    "creator":"creator"
  }
  
}

{
    "username":{
        "email":"email",
        "level":"level",
        "password":"password"
    }
}

