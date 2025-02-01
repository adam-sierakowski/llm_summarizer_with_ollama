import argparse
import jsonlines
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain

def create_db_from_url(url: str):
    loader = WebBaseLoader(url)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)[:4]
    return docs

def generate_summary(docs, llm):
    chain = load_summarize_chain(llm,
                            chain_type="map_reduce",
                            # verbose = True
                            )
    output_summary = chain.invoke(docs)
    summary = output_summary['output_text']
    return summary

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Specify input URL")
    parser.add_argument("-l", "--llm", help="Specify the ollama LLM you want to use (defaulting to llama3.2:latest). Use `ollama ls` to check which models you have")
    parser.add_argument("-o", "--output", help="Output file")
    msg = "This script summarizes provided url using local llm.\nOutputs are appended to a .jsonl file."
    
    args = parser.parse_args()

    url = args.input.strip() if args.input else quit("Please provide input. Use -h flag for help")
    output_file = args.output.strip() if args.output else "summarizer_outputs.jsonl"
    model_name = args.llm.strip() if args.llm else "llama3.2:latest"

    return url, model_name, output_file

def split_into_think_and_say(llm_response):
    if "</think>" in llm_response:
        think, say = llm_response.split("</think>", 1)
        return think + "</think>", say
    else:
        return None, llm_response

def main():

    url, model_name, output_file = get_args()

    try:
        llm = OllamaLLM(model=model_name)
    except Exception as e:
        print(f"Tried initializing model {model_name} and failed.")
        quit(e)

    print(f"Input url is {url}")
    print("Proceeding...")

    docs = create_db_from_url(url)
    response = generate_summary(docs, llm)
    chain_of_thought, actual_response = split_into_think_and_say(response)

    output = {
        "url": url,
        "model_used": model_name,
        "chain_of_thought": chain_of_thought,
        "summary": actual_response
    }

    with jsonlines.open(output_file, mode="a") as writer:
        writer.write(output)

    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()