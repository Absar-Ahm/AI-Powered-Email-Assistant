def build_prompt(tone, recipient, purpose=None, topic=None, original_email=None, mode="new"):
    if mode == "new":
        return f"""
You are a professional email writer.

Write a {tone} email to a {recipient} regarding the following purpose: {purpose}.

Topic/Context:
{topic}

The email should be polite, clear, and appropriately structured.
"""
    elif mode == "reply":
        return f"""
You are a professional email assistant.

You just received the following email from a {recipient}:
---
{original_email}
---

Write a polite and well-structured {tone} reply to this email. The purpose of your reply is: {purpose}.
Respond appropriately based on the content and tone of the original message.
"""
