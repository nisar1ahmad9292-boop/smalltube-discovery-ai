
import streamlit as st
from google import genai

st.set_page_config(
    page_title="SmallTube Discovery AI",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 SmallTube Discovery AI")
st.write("Plan better YouTube videos with AI.")

# Connect securely to Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

# User inputs
channel = st.text_input(
    "Channel name",
    "PhysioFix 60"
)

topic = st.text_input(
    "Video topic",
    "Lower back pain after sitting"
)

languages = st.multiselect(
    "Choose languages",
    ["English", "Urdu"],
    default=["English", "Urdu"]
)

formats = st.multiselect(
    "Choose video formats",
    ["YouTube Shorts", "Long video"],
    default=["YouTube Shorts", "Long video"]
)

audience = st.text_input(
    "Target audience",
    "General viewers"
)

tone = st.selectbox(
    "Video style",
    ["Educational", "Friendly", "Professional", "Engaging"]
)

if st.button("🚀 Generate my AI video plan", type="primary"):

    if not topic.strip():
        st.warning("Please enter a video topic.")

    elif not languages or not formats:
        st.warning("Please select at least one language and format.")

    elif client is None:
        st.error(
            "Gemini connection not found. "
            "Please check your Streamlit Secrets."
        )

    else:
        prompt = f"""
You are an expert YouTube content strategist and scriptwriter.

Create a professional YouTube content plan.

CHANNEL: {channel}
TOPIC: {topic}
LANGUAGES: {", ".join(languages)}
VIDEO FORMATS: {", ".join(formats)}
TARGET AUDIENCE: {audience}
STYLE: {tone}

IMPORTANT INSTRUCTIONS:

1. Give 10 original and relevant video ideas related to the topic.
2. For each idea provide:
   - A catchy YouTube title
   - A strong opening hook
   - Why viewers may find it useful
3. Create a separate, complete sample script for each selected video format.
4. Make the scripts natural, engaging and easy to speak.
5. If Urdu is selected, write natural Urdu in Urdu script.
6. If English is selected, use clear, natural English.
7. Include scene suggestions and visual ideas.
8. Include a suitable description, call to action and hashtags.
9. Avoid repetitive, misleading or exaggerated titles.
10. Make content original. Do not copy existing creators.

HEALTH CONTENT SAFETY:
If the topic is about health or physiotherapy:
- Keep information educational.
- Do not diagnose viewers.
- Do not promise cures or guaranteed results.
- Do not recommend exercises as suitable for everyone.
- Mention professional assessment when symptoms are severe,
  persistent or concerning.

Use clear headings and a well-organized format.
"""

        with st.spinner("Gemini is creating your video plan..."):
            try:
                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )

                result = response.text

                if result:
                    st.success("Your AI video plan is ready!")
                    st.markdown(result)

                    st.download_button(
                        "📥 Download video plan",
                        data=result,
                        file_name="smalltube_video_plan.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Gemini returned an empty response.")

            except Exception as e:
                st.error("Something went wrong while generating your plan.")
                st.write(str(e))
