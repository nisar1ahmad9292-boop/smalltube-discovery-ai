
import streamlit as st
import time
from google import genai

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="SmallTube Discovery AI",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 SmallTube Discovery AI")
st.caption("Find better YouTube ideas and create professional scripts.")

# ---------------- GEMINI CONNECTION ----------------

@st.cache_resource
def connect_gemini():
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    return genai.Client(api_key=api_key)

try:
    client = connect_gemini()
    connection_ok = True
except Exception as e:
    client = None
    connection_ok = False
    connection_error = str(e)

# ---------------- GEMINI REQUEST WITH RETRIES ----------------


def generate_with_retry(prompt, max_tokens=2500):

    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite"
    ]

    errors = []

    for model_name in models:
        for attempt in range(2):

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "max_output_tokens": max_tokens,
                        "temperature": 0.7
                    }
                )

                if not response.text:
                    raise ValueError("Gemini returned an empty response.")

                return response.text

            except Exception as e:
                errors.append(
                    f"{model_name}, attempt {attempt + 1}: {str(e)}"
                )

                error_text = str(e).lower()

                temporary = any(
                    code in error_text
                    for code in [
                        "503", "500", "502", "504",
                        "unavailable", "overloaded",
                        "temporarily"
                    ]
                )

                if temporary and attempt == 0:
                    time.sleep(2)
                    continue

                if temporary:
                    break

                raise

    raise RuntimeError(
        "All Gemini models failed. Details: "
        + " | ".join(errors)
    )

# ---------------- APP INPUTS ----------------

st.subheader("1. Your YouTube channel")

channel = st.text_input(
    "Channel name",
    value="PhysioFix 60"
)

topic = st.text_input(
    "What topic do you want to make videos about?",
    value="Lower back pain after sitting"
)

audience = st.text_input(
    "Target audience",
    value="General viewers"
)

language = st.selectbox(
    "Choose ONE language",
    ["English", "Urdu"]
)

video_format = st.selectbox(
    "Choose video format",
    ["YouTube Shorts", "Long video"]
)

style = st.selectbox(
    "Choose content style",
    ["Educational", "Friendly", "Professional", "Engaging"]
)

# ---------------- STAGE 1: IDEAS ----------------

st.divider()
st.subheader("2. Generate video ideas")

st.write(
    "First, discover five useful and original ideas "
    "for your selected topic."
)

if st.button("💡 Generate 5 Ideas", type="primary"):

    if not topic.strip():
        st.warning("Please enter a video topic.")

    elif not connection_ok:
        st.error("Gemini connection problem.")
        st.write(connection_error)

    else:
        ideas_prompt = f"""
You are an expert YouTube content strategist.

Create exactly FIVE excellent, original YouTube video ideas.

CHANNEL: {channel}
TOPIC: {topic}
AUDIENCE: {audience}
LANGUAGE: {language}
FORMAT: {video_format}
STYLE: {style}

STRICT QUALITY RULES:

1. Every idea must directly relate to the actual topic.
2. Each idea must address a real viewer question, problem,
   curiosity or practical need.
3. Give each idea a specific, attractive and grammatically
   correct title.
4. Avoid repetitive ideas and generic titles.
5. Do not invent facts or make misleading promises.
6. Think about what viewers would genuinely want to learn.
7. Do not create scripts yet.

For EACH of the five ideas provide:

IDEA NUMBER:
TITLE:
VIEWER PROBLEM:
OPENING HOOK:
KEY POINTS (three):
WHY VIEWERS MAY WATCH:

LANGUAGE RULES:

If English:
Use natural, simple, fluent spoken English.

If Urdu:
Use natural Pakistani Urdu in Urdu script.
Use expressions that a Pakistani Urdu speaker
would naturally use.
Do not use Hindi vocabulary or awkward translations.
Do not use Roman Urdu.

Make all five ideas meaningfully different.
Return only the five ideas with clear headings.
"""

        with st.spinner("Finding your best video ideas..."):
            try:
                result = generate_with_retry(
                    ideas_prompt,
                    max_tokens=2000
                )

                st.session_state["ideas"] = result
                st.session_state["last_topic"] = topic
                st.session_state["last_language"] = language
                st.success("Five video ideas generated!")

            except Exception as e:
                st.error("Idea generation failed.")
                st.write(str(e))


# Display saved ideas
if "ideas" in st.session_state:

    st.divider()
    st.subheader("Your five video ideas")

    st.markdown(st.session_state["ideas"])

    st.download_button(
        "📥 Download all ideas",
        data=st.session_state["ideas"],
        file_name="smalltube_video_ideas.txt",
        mime="text/plain"
    )


# ---------------- STAGE 2: SCRIPT ----------------

st.divider()
st.subheader("3. Create your professional script")

st.write(
    "Choose one idea from the results above. "
    "Copy its title into the box below."
)

selected_idea = st.text_input(
    "Enter your selected video idea",
    placeholder="Paste your selected video title here"
)

if st.button("✍️ Generate My Script", type="primary"):

    if not connection_ok:
        st.error("Gemini connection problem.")
        st.write(connection_error)

    elif not selected_idea.strip():
        st.warning("Please enter your selected video idea.")

    elif "ideas" not in st.session_state:
        st.warning("Please generate your five ideas first.")

    else:

        script_prompt = f"""
You are a highly experienced professional YouTube scriptwriter.

Write ONE excellent, complete and natural video script.

CHANNEL: {channel}
MAIN TOPIC: {topic}
SELECTED IDEA: {selected_idea}
AUDIENCE: {audience}
LANGUAGE: {language}
FORMAT: {video_format}
STYLE: {style}

LANGUAGE QUALITY IS EXTREMELY IMPORTANT.

For English:
- Write natural spoken English.
- Use correct grammar and sentence structure.
- Sound like an experienced human presenter.
- Use short, clear and meaningful sentences.

For Urdu:
- Write in Urdu script, not Roman Urdu.
- Use natural Pakistani Urdu.
- Do not translate English sentences word for word.
- Avoid Hindi vocabulary and Indian-style expressions.
- Use fluent, familiar and grammatically correct Urdu.
- Make the dialogue sound natural when spoken aloud.

SCRIPT STRUCTURE:

1. Attractive video title.
2. Opening hook that creates curiosity.
3. Short introduction.
4. Main explanation in a logical sequence.
5. Useful examples or practical tips.
6. Memorable conclusion.
7. Natural call to action.

FORMAT REQUIREMENTS:

For YouTube Shorts:
- Target 45 to 60 seconds.
- Approximately 100 to 140 spoken words.
- No unnecessary introduction.
- Strong hook in the first few seconds.
- Keep the explanation focused.

For Long video:
- Create a detailed, well-organized script.
- Include meaningful sections and transitions.
- Avoid repetition and filler.

Also provide:
- Scene-by-scene visual suggestions.
- Relevant video description.
- Five to eight relevant hashtags.
- Thumbnail concept.

IMPORTANT:
Do not write generic filler.
Do not repeat the same point.
Do not make unsupported claims.
Make every sentence useful and meaningful.

If the topic is about health or physiotherapy:
- Provide educational information, not diagnosis.
- Do not promise a cure.
- Do not claim exercises suit everyone.
- Recommend professional assessment for severe,
  persistent or concerning symptoms.

Before returning the answer, check grammar,
natural speech, accuracy and logical flow.

Return only the finished professional content.
"""

        with st.spinner(
            "Creating your professional script. Please wait..."
        ):
            try:
                script = generate_with_retry(
                    script_prompt,
                    max_tokens=3500
                )

                st.session_state["generated_script"] = script
                st.success("Your script is ready!")

            except Exception as e:
                st.error("Script generation failed.")
                st.write(str(e))


# Display generated script
if "generated_script" in st.session_state:

    st.divider()
    st.subheader("Your professional video script")

    st.markdown(st.session_state["generated_script"])

    st.download_button(
        "📥 Download your script",
        data=st.session_state["generated_script"],
        file_name="smalltube_professional_script.txt",
        mime="text/plain"
    )


# ---------------- FOOTER ----------------

st.divider()
st.caption(
    "SmallTube Discovery AI | AI-assisted YouTube planning. "
    "Organic search or recommendation placement is not guaranteed."
)
