from models.prompts import prompt_template
from services.llm_model import model
import json



def preprocess_context(data):
    lines = []
    for j in range(len(data)):
        name = data[j][0]
        content = data[j][1]
        meta = ", ".join(f"{k}: {v}" for k, v in data[j][2].items())
        lines.append(
                f"{j}. Document:\n"
                f"   name: {name}\n"
                f"   Content: {content[:200]}...\n"
                f"   Metadata: {meta}\n"
            )
    return "\n".join(lines)

def llm_output(selected_data:list, query:str):
    try:        
        content = []
        for data in selected_data:
            result = data.query(
                query_texts=[query],
                n_results=5)
            content.append((data.name,result['documents'][0][0],result['metadatas'][0][0]))

        context = preprocess_context(data=content)

        formatted_prompt = prompt_template.format(context=context, question=query)

        response_text = model.invoke(formatted_prompt)

        #json output
        data_list = json.loads(response_text.content)


        return  data_list

    except Exception as e:
        return f"❌ failed -- {e}"