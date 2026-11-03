
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
You are a senior YouTube content strategist, professional scriptwriter,
and bilingual English-Urdu communication expert.

Your task is to create a high-quality, practical YouTube content plan.

CHANNEL: {channel}
TOPIC: {topic}
LANGUAGES: {", ".join(languages)}
FORMATS: {", ".join(formats)}
TARGET AUDIENCE: {audience}
STYLE: {tone}

PART 1 — CONTENT IDEAS

Generate 10 genuinely different and useful video ideas.

For every idea provide:
1. A clear and attractive title.
2. A natural opening hook.
3. The main question or problem addressed.
4. Three useful points the video will explain.
5. Why viewers might find it valuable.

Avoid repetitive ideas, vague titles and artificial clickbait.

PART 2 — LANGUAGE QUALITY

If English is selected:
- Write in natural, modern spoken English.
- Use short, grammatically correct sentences.
- Sound like a knowledgeable human speaking to viewers.
- Avoid robotic, repetitive or overly complicated wording.

If Urdu is selected:
- Write in natural Pakistani Urdu using Urdu script.
- Use simple, fluent and conversational Pakistani expressions.
- Do not use Hindi vocabulary or Indian-style Hindi sentences.
- Do not translate English word-for-word.
- Write as a native Pakistani Urdu speaker would naturally speak.
- Avoid Roman Urdu unless specifically requested.
- Check grammar, sentence flow and word choice.

IMPORTANT:
Create separate English and Urdu versions.
Do not mix both languages in the same script.
Do not use awkward constructions such as
"Why does simple exercises happen?"
Use grammatically correct and natural questions.

PART 3 — VIDEO SCRIPTS

For each selected video format, create a complete sample script
for the most useful idea.

For every script include:

1. VIDEO TITLE
2. OPENING HOOK
3. MAIN EXPLANATION
4. PRACTICAL EXAMPLES OR TIPS
5. CONCLUSION
6. CALL TO ACTION

For YouTube Shorts:
- Target duration: 45–60 seconds.
- Start with an interesting hook.
- Keep the explanation concise and useful.
- Make the spoken dialogue easy to deliver.

For long videos:
- Create a logical introduction, detailed explanation,
  practical sections and conclusion.
- Avoid unnecessary repetition.
- Make the script informative and engaging.

PART 4 — VISUAL PLAN

Suggest suitable scenes and visuals for each script.
Keep visual suggestions relevant to the spoken dialogue.

PART 5 — YOUTUBE PUBLISHING

Provide:
- A natural video description.
- A relevant call to action.
- 5–8 relevant hashtags.
- A suitable thumbnail concept.

PART 6 — QUALITY CHECK

Before presenting the final answer, check:
- Are all ideas relevant to the actual topic?
- Are titles grammatically correct?
- Does each script make sense when spoken aloud?
- Is the Urdu natural Pakistani Urdu?
- Is the English natural spoken English?
- Are the two language versions separate?
- Is there unnecessary repetition?
- Are the claims accurate and not exaggerated?

HEALTH AND PHYSIOTHERAPY SAFETY:
If the topic concerns health or physiotherapy:
- Provide educational information, not individual diagnosis.
- Do not promise a cure or guaranteed results.
- Do not claim one exercise is suitable for everyone.
- Include professional assessment advice for severe,
  persistent or concerning symptoms.

Present the final answer with clear headings and separate sections.
Prioritize accuracy, natural language and practical value over quantity.
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
