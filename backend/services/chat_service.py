# from neo4j_db import get_neo4j_session
# import uuid
# from datetime import datetime

# def create_chat_session(user_id: int):
#     chat_id = str(uuid.uuid4())

#     query = """
#     MERGE (u:User {user_id: $user_id})
#     CREATE (c:ChatSession {
#         chat_id: $chat_id,
#         created_at: $created_at
#     })
#     CREATE (u)-[:HAS_CHAT]->(c)
#     """

#     with get_neo4j_session() as session:
#         session.run(
#             query,
#             user_id=user_id,
#             chat_id=chat_id,
#             created_at=str(datetime.utcnow())
#         )

#     return chat_id




# def store_message(chat_id: str, sender: str, text: str):
#     query = """
#     MATCH (c:ChatSession {chat_id: $chat_id})
#     CREATE (m:Message {
#         sender: $sender,
#         text: $text,
#         timestamp: $timestamp
#     })
#     CREATE (c)-[:HAS_MESSAGE]->(m)
#     """

#     with get_neo4j_session() as session:
#         session.run(
#             query,
#             chat_id=chat_id,
#             sender=sender,
#             text=text,
#             timestamp=str(datetime.utcnow())
#         )



# def get_chat_history(chat_id: str):
#     query = """
#     MATCH (c:ChatSession {chat_id: $chat_id})-[:HAS_MESSAGE]->(m:Message)
#     RETURN m
#     ORDER BY m.timestamp ASC
#     """

#     messages = []

#     with get_neo4j_session() as session:
#         result = session.run(query, chat_id=chat_id)

#         for record in result:
#             m = record["m"]
#             messages.append({
#                 "sender": m["sender"],
#                 "text": m["text"],
#                 "timestamp": m["timestamp"]
#             })

#     return messages

from neo4j_db import get_neo4j_session
import uuid
from datetime import datetime


def create_chat_session(user_id: int):
    chat_id = str(uuid.uuid4())

    query = """
    MERGE (u:User {user_id: $user_id})
    CREATE (c:ChatSession {
        chat_id: $chat_id,
        created_at: $created_at
    })
    CREATE (u)-[:HAS_CHAT]->(c)
    """

    with get_neo4j_session() as session:
        session.run(
            query,
            user_id=user_id,
            chat_id=chat_id,
            created_at=str(datetime.utcnow())
        )

    return chat_id


def store_message(chat_id: str, sender: str, text: str):
    query = """
    MATCH (c:ChatSession {chat_id: $chat_id})
    CREATE (m:Message {
        sender: $sender,
        text: $text,
        timestamp: $timestamp
    })
    CREATE (c)-[:HAS_MESSAGE]->(m)
    """

    with get_neo4j_session() as session:
        session.run(
            query,
            chat_id=chat_id,
            sender=sender,
            text=text,
            timestamp=str(datetime.utcnow())
        )


def get_chat_history(chat_id: str):
    query = """
    MATCH (c:ChatSession {chat_id: $chat_id})-[:HAS_MESSAGE]->(m:Message)
    RETURN DISTINCT m
    ORDER BY m.timestamp ASC
    """

    messages = []

    with get_neo4j_session() as session:
        result = session.run(query, chat_id=chat_id)

        for record in result:
            m = record["m"]
            messages.append({
                "sender": m["sender"],
                "text": m["text"],
                "timestamp": m["timestamp"]
            })

    return messages
