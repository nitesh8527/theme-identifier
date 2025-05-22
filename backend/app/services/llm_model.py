from langchain_groq import ChatGroq


model = ChatGroq(
                temperature=0,
                groq_api_key= "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", #"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", #"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", #secrets.GROQ_API_KEY,
                model_name="llama-3.3-70b-versatile"
            )