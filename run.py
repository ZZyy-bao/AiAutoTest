from core.commom.ai_model import AiDeepseek

ds = AiDeepseek()

content = ds.chat(
    user_content="你好呀"
)
print(content)
print(ds.chat_messages_list)