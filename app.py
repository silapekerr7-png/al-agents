import streamlit as st
from agents import configure, planner_agent, search_agent, synthesizer_agent

st.title("AI Research Assistant (Multi-Agent, Gemini) :mag:")
st.write("Planner -> Search Agent -> Synthesizer")

topic=st.text_input("Araştırılacak konu")
if st.button("Araştır") and topic.strip():
    try:
        model=configure()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    with st.spinner("Planner Agent plan hazırlıyor..."):
        plan=planner_agent(model,topic)
    if not plan:
        st.error("Araştırma planı oluşturulamadı.")
        st.stop()
    st.subheader("Plan")
    for i,q in enumerate(plan,1):
        st.write(f"{i}. {q}")

    research_results=[]
    for q in plan:
        with st.spinner(f"Search Agent araştırıyor: {q}"):
            data=search_agent(model,q)
        if data:
            research_results.append((q,data))
    if not research_results:
        st.error("Araştırma sırasında bilgi bulunamadı.")
        st.stop()

    with st.spinner("Synthesizer Agent raporu yazıyor..."):
        rapor=synthesizer_agent(model,topic,research_results)
    st.subheader("Final Rapor")
    st.markdown(rapor)
