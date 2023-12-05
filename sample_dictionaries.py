user = {"users": {
    "john_doe": {
        "username": "john_doe",
        "password": "password123",
        "email": "john@example.com",
        "chats":[{"chat_room1":"security level"}, {"chat_room2":"security level"}]
        },
    "jane_smith": {
        "username": "jane_smith",
        "password": "secret456",
        "email": "jane@example.com",
        "chats":[{"chat_room1":"security level"}, {"chat_room2":"security level"}]
        }
      }
    }

chats = {"chat_room_1":{"security level":{"password":{
        "members": [
          "user_id_1",
          "user_id_2",
          "user_id_3"
        ],
        "chat_history": {
          "message_id_1": {
            "id": "message_id_1",
            "date": "2023-01-01T12:00:00",
            "sent_from": "user_id_1",
            "content": "Hello, how are you?"
          },
          "message_id_2": {
            "id": "message_id_2",
            "date": "2023-01-01T12:05:00",
            "sent_from": "user_id_2",
            "content": "I'm good, thanks! How about you?"
          },
        }
      },
    }
  }
}