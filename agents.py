# Makaledeki ajan fonksiyonları (planner_agent, search_agent, synthesizer_agent) aynen alınmıştır.
# Tek fark: configure() Colab userdata yerine ortam değişkeninden anahtar okur (Streamlit için).
import os
import google.generativeai as genai

def configure():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı.")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-pro-latest')


def planner_agent(model, topic: str) -> list[str]:
    print("Planner Agent: Creating a research plan...")
    prompt = f"""
    You are an expert research planner. Your task is to break down the following topic
    into 3-5 specific, answerable questions. Return these questions as a Python list of strings.

    TOPIC: "{topic}"

    Example output: ["question 1", "question 2", "question 3"]
    """
    try:
        response = model.generate_content(prompt)
        plan_str = response.text.strip().replace('[', '').replace(']', '').replace('"', '')
        plan = [q.strip() for q in plan_str.split(',') if q.strip()]

        print("Plan created:")
        for i, q in enumerate(plan, 1):
            print(f"   {i}. {q}")
        return plan
    except Exception as e:
        print(f"Error in Planner Agent: {e}")
        return []

def search_agent(model, question: str) -> str:
    print(f"Search Agent: Researching question: '{question}'...")
    try:
        search_tool = genai.protos.Tool(
            google_search_retrieval=genai.protos.GoogleSearchRetrieval(disable_attribution=True)
        )
        prompt = f"Provide a detailed answer to the following question: {question}"
        response = model.generate_content(prompt, tools=[search_tool])

        print("   - Information found.")
        return response.text
    except Exception as e:
        print(f"Error in Search Agent: {e}")
        return ""

def synthesizer_agent(model, topic: str, research_results: list) -> str:
    print("Synthesizer Agent: Writing the final report...")

    research_notes = ""
    for question, data in research_results:
        research_notes += f"### Question: {question}\n### Research Data:\n{data}\n\n---\n\n"

    prompt = f"""
    You are an expert research analyst. Your task is to synthesize the provided research notes
    into a comprehensive, well-structured report on the topic: "{topic}".

    The report should have an introduction, a body that covers the key findings from the notes,
    and a conclusion. Use the information from the research notes ONLY.

    ## Research Notes ##
    {research_notes}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in Synthesizer Agent: {e}")
        return "Error: Could not generate the final report."
