# from fastapi import APIRouter, Depends
# from auth import get_current_user
# from services.chat_service import create_chat_session, store_message
# from schemas import ChatMessage
# from services.llm_service import get_ai_response
# from services.chat_service import get_chat_history
# from services.llm_service import get_ai_response_with_context

# router = APIRouter(prefix="/chat", tags=["Chat"])
# @router.post("/start")
# def start_chat(current_user = Depends(get_current_user)):
#     chat_id = create_chat_session(current_user.id)
#     return {"chat_id": chat_id}
# # @router.post("/{chat_id}/message")
# # def send_message(
# #     chat_id: str,
# #     payload: ChatMessage,
# #     current_user = Depends(get_current_user)
# # ):
# #     store_message(chat_id, "user", payload.message)
# #     return {"status": "message stored"}


# @router.post("/{chat_id}/message")
# async def send_message(
#     chat_id: str,
#     payload: ChatMessage,
#     current_user = Depends(get_current_user)
# ):
#     # 1️⃣ Store user message
#     store_message(chat_id, "user", payload.message)

#     # 2️⃣ Get AI response
#     ai_response = await get_ai_response(payload.message)

#     # 3️⃣ Store AI message
#     store_message(chat_id, "ai", ai_response)

#     # 4️⃣ Return AI response
#     return {
#         "user_message": payload.message,
#         "ai_response": ai_response
#     }

# @router.get("/{chat_id}/history")
# def chat_history(
#     chat_id: str,
#     current_user = Depends(get_current_user)
# ):
#     history = get_chat_history(chat_id)
#     return {
#         "chat_id": chat_id,
#         "messages": history
#     }


from fastapi import APIRouter, Depends
from auth import get_current_user
from schemas import ChatMessage
from services.chat_service import (
    create_chat_session,
    store_message,
    get_chat_history
)
from services.llm_service import get_ai_response_with_context

router = APIRouter(prefix="/chat", tags=["Chat"])


# 🔹 STEP 3: Start a new chat session
@router.post("/start")
def start_chat(current_user = Depends(get_current_user)):
    chat_id = create_chat_session(current_user.id)
    return {
        "chat_id": chat_id
    }


# 🔹 Helper: Convert chat history into LLM format
# def build_llm_messages(history: list, new_message: str):
#     messages = []

#     for msg in history:
#         if msg["sender"] == "user":
#             messages.append({
#                 "role": "user",
#                 "content": msg["text"]
#             })
#         else:
#             messages.append({
#                 "role": "assistant",
#                 "content": msg["text"]
#             })

#     # Add the latest user message
#     messages.append({
#         "role": "user",
#         "content": new_message
#     })

#     return messages

def build_llm_messages(history: list, new_message: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that answers questions accurately and clearly. "
                "Stay strictly on the topic asked by the user. "
                "If the question is about Large Language Models (LLMs), "
                "explain concepts like transformers, training, inference, and use cases. "
                "Do NOT change the topic unless the user explicitly asks."
            )
        }
    ]

    for msg in history:
        messages.append({
            "role": "user" if msg["sender"] == "user" else "assistant",
            "content": msg["text"]
        })

    messages.append({
        "role": "user",
        "content": new_message
    })

    return messages


@router.post("/{chat_id}/message")
async def send_message(
    chat_id: str,
    payload: ChatMessage,
    current_user = Depends(get_current_user)
):
    # 1️⃣ Fetch existing chat history (BEFORE storing new message)
    history = get_chat_history(chat_id)

    # 2️⃣ Build LLM context using history + new message
    llm_messages = build_llm_messages(history, payload.message)

    # 3️⃣ Get AI response
    ai_response = await get_ai_response_with_context(llm_messages)

    # 4️⃣ Store user message ONCE
    store_message(chat_id, "user", payload.message)

    # 5️⃣ Store AI response ONCE
    store_message(chat_id, "ai", ai_response)

    # 6️⃣ Return AI response
    return {
        "reply": ai_response
    }


# # 🔹 STEP 5: Fetch chat history
@router.get("/{chat_id}/history")
def chat_history(
    chat_id: str,
    current_user = Depends(get_current_user)
):
    history = get_chat_history(chat_id)
    return {
        "chat_id": chat_id,
        "messages": history
    }
