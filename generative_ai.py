# imporing package to connect with ollama server
import ollama

SYSTEM_PROMPT = """
You are a Docker Expert. You can explain things in 1 -2 lines max.
You don't overtink, hallucinate or keep resoning in loop.
You resone and act according to user prompt

there are the things you do:
1/ You tell about errors ( what went wrong, etc)
2/ Yor tell about the root cause ( what was cause likely)
3/ You tell about the fix or solution in short
"""

while True: 
    user_input = input("Enter your message:\n")
    if user_input == "exit":
        break
    # Request
    response = ollama.chat(
        model="gemma:2b",  
        messages=[{'role' : 'system', 'content' : SYSTEM_PROMPT},{
            'role': 'user',
            'content': user_input,
        }]
    )

    print(response['message']['content'])