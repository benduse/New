from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Chatbot:
    def __init__(self, model_name="facebook/opt-350m"):
        print("Initializing chatbot... This might take a moment.")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print("Chatbot is ready!")

    def generate_response(self, user_input, max_length=100):
        # Prepare the input
        inputs = self.tokenizer(f"User: {user_input}\nBot:", return_tensors="pt", return_token_type_ids=False)
        
        # Generate response
        with torch.no_grad():
            generated_ids = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode and return the response
        response = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return response.split("Bot:")[-1].strip()

def main():
    print("Starting the chatbot...")
    chatbot = Chatbot()
    
    print("\nChat with the bot! (type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        
        response = chatbot.generate_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
