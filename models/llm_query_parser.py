from transformers import pipeline

nlp_model = pipeline("text-classification", model="ProsusAI/finbert")

def parse_user_input(user_input):
    sentiment = nlp_model(user_input)[0]
    return sentiment

if __name__ == "__main__":
    print(parse_user_input("I want to invest for 5 years with low risk."))
