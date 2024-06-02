import random
responses = {
    "greeting": [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Greetings! How may I assist you?",
        "Hello! What brings you here today?",
        "Hi! How can I assist you?",
        "Hey! What do you need help with?",
        "Hello! How can I be of service?",
        "Hi! What can I help you with?",
        "Greetings! How can I assist?",
        "Hello! How may I help you today?"
    ],
    "feeling_sick": [
        "I'm sorry to hear that you're feeling sick. Can you describe your symptoms?",
        "That's unfortunate. What symptoms are you experiencing?",
        "I hope you feel better soon. What are your symptoms?",
        "Can you tell me more about how you're feeling?",
        "I'm here to help. What symptoms do you have?",
        "Tell me more about your illness so I can assist.",
        "I'm sorry to hear that. What symptoms are you dealing with?",
        "Please describe your symptoms for me.",
        "What symptoms are you experiencing today?",
        "Can you tell me about your symptoms?"
    ],
    "ask_advice": [
        "Sure, I'd be happy to offer some advice",
        "Of course! What advice are you looking for?",
        "I'm here to help. What do you need advice on?",
        "Sure, I can help with that. What's your question?",
        "What kind of advice do you need?",
        "Feel free to ask your question. I'm here to help.",
        "I'm happy to offer advice. What do you need?",
        "Let me know how I can assist you with advice.",
        "I'd be glad to help. What advice do you need?",
        "I'm here to give you advice. What do you need help with?"
    ],
    "ask_disease_info": [
        "I can provide information about various diseases. Which disease are you interested in?",
        "Sure, I can help with that. Which disease do you want to know about?",
        "I'd be happy to provide information. Which disease are you curious about?",
        "Tell me which disease you need information on.",
        "I can help with disease information. What are you interested in?",
        "Which disease do you want to learn more about?",
        "Feel free to ask about any disease. I'm here to help.",
        "I can provide details on many diseases. Which one?",
        "Ask me about any disease, and I'll give you information.",
        "What disease information are you looking for?"
    ],
    "ask_symptoms": [
        "Please tell me more about your symptoms so I can assist you better.",
        "Can you describe your symptoms in more detail?",
        "I need more information about your symptoms to help.",
        "What symptoms are you experiencing?",
        "Tell me more about your symptoms.",
        "Describe your symptoms for me.",
        "What are the symptoms you're dealing with?",
        "Please provide more details about your symptoms.",
        "What symptoms do you have?",
        "Can you tell me about your symptoms?"
    ],
    "farewell": [
        "Goodbye! Take care.",
        "See you later! Stay safe.",
        "Farewell! Hope to see you soon.",
        "Bye! Take care of yourself.",
        "Goodbye! Have a great day.",
        "See you! Stay healthy.",
        "Bye! Wishing you the best.",
        "Goodbye! Stay well.",
        "Farewell! All the best.",
        "Bye! Take care and stay safe."
    ],
    "listing_symptoms": [
        "Thank you for listing your symptoms. I will try to help you based on this information.",
        "Got it. Let me see how I can assist you with these symptoms.",
        "Thank you for providing your symptoms. I'll do my best to help.",
        "Noted your symptoms. Let me check what can be done.",
        "Thanks for the details. I'll see how I can help with these symptoms.",
        "Your symptoms are noted. Let's see how I can assist.",
        "I'll use this information to help you. Thank you for listing your symptoms.",
        "Got your symptoms. Let me assist you further.",
        "Thanks for sharing your symptoms. I'll see how I can help.",
        "I'll do my best to assist you based on your symptoms. Thank you."
    ]
}

def get_response(intent):
     if intent in responses:
        return random.choice(responses[intent])
     else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"