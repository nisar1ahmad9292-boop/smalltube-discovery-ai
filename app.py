
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
                        "temperature": 0.5
                    }
                )

                if not response.text:
                    raise ValueError("Empty response from Gemini.")

                return response.text

            except Exception as e:
                error_text = str(e).lower()
                errors.append(f"{model_name}: {str(e)}")

                temporary = any(
                    word in error_text
                    for word in [
                        "503", "500", "502", "504",
                        "unavailable", "overloaded",
                        "temporarily"
                    ]
                )

                if temporary and attempt == 0:
                    time.sleep(3)
                    continue

                if temporary:
                    break

                raise

    raise RuntimeError(
        "Gemini is temporarily unavailable. Please try again later. "
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
You are an expert YouTube content strategist, audience researcher,
and professional video idea developer.

Your task is to create FIVE highly distinct, original,
valuable and engaging YouTube video ideas.

PROJECT DETAILS:
Channel: {channel}
Main topic: {topic}
Target audience: {audience}
Language: {language}
Video format: {video_format}
Style: {style}

QUALITY REQUIREMENTS:

1. Each of the five ideas must explore a DIFFERENT angle.
2. Avoid repeating the same problem, solution or message.
3. Focus on real questions, problems and interests of the target audience.
4. Prefer specific, practical and useful topics over generic topics.
5. Create curiosity without misleading or sensational claims.
6. Titles must be clear, natural and attractive.
7. Hooks must capture attention within the first few seconds.
8. Key points must be meaningful, relevant and logically connected.
9. Explain why the intended audience would find each idea valuable.
10. Do not invent statistics, research findings or facts.
11. Do not claim that a topic is trending or popular without actual data.
12. Do not guarantee views, rankings or YouTube recommendations.

DIVERSITY REQUIREMENT:

Make the five ideas different in their approach.
Where appropriate, include a mix of:
- Common mistakes and misconceptions.
- Practical tips and demonstrations.
- Explanations of causes and mechanisms.
- Frequently asked audience questions.
- Evidence-informed educational topics.

LANGUAGE REQUIREMENTS:

For English:
Use fluent, natural and professional spoken English.

For Urdu:
Use natural Pakistani Urdu in Urdu script.
Avoid Roman Urdu, Hindi vocabulary and awkward translations.

HEALTH AND PHYSIOTHERAPY SAFETY:

If the topic involves health or physiotherapy:
- Use medically responsible and evidence-aware language.
- Do not diagnose viewers.
- Do not promise cures or guaranteed pain relief.
- Do not suggest that one exercise is suitable for everyone.
- Mention when individual assessment may be necessary.
- Avoid unsupported claims about bones, muscles, discs or posture.

OUTPUT FORMAT:

IDEA 1
TITLE:
VIEWER PROBLEM:
OPENING HOOK:
THREE KEY POINTS:
WHY THIS IDEA IS VALUABLE:

Repeat this exact structure for IDEA 2, IDEA 3,
IDEA 4 and IDEA 5.

FINAL QUALITY CHECK:
Before responding, check that all five ideas are distinct,
useful, accurate, grammatically correct and appropriate
for the specified audience and language.

Return only the five completed ideas.
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
You are a senior YouTube content strategist, professional
video scriptwriter, healthcare communication specialist,
and short-form video producer.

Your task is to create ONE outstanding, original,
publication-ready YouTube video package.

PROJECT DETAILS:
CHANNEL: {channel}
MAIN TOPIC: {topic}
SELECTED IDEA: {selected_idea}
TARGET AUDIENCE: {audience}
LANGUAGE: {language}
VIDEO FORMAT: {video_format}
PRESENTATION STYLE: {style}

==================================================
1. LANGUAGE AND COMMUNICATION QUALITY
==================================================

ENGLISH:
- Use fluent, natural, conversational English.
- Sound like an experienced human presenter.
- Use simple but professional vocabulary.
- Avoid robotic, repetitive and textbook-style sentences.
- Make every sentence easy to speak aloud.

URDU:
- Write entirely in Urdu script.
- Use natural Pakistani Urdu.
- Avoid Hindi vocabulary and Indian-style expressions.
- Do not translate English sentence structures literally.
- Use fluent, grammatically correct spoken Urdu.
- Make narration sound natural and engaging.

Never mix languages unnecessarily.

==================================================
2. CONTENT STRATEGY
==================================================

Before writing:
- Understand the viewer's actual problem.
- Identify the most useful and interesting angle.
- Create a clear central message.
- Avoid generic advice.
- Make the content specific to the selected idea.
- Do not invent statistics, studies or quotations.
- Do not repeat the same information.

The content must provide genuine educational value.

==================================================
3. PROFESSIONAL SCRIPT STRUCTURE
==================================================

For YouTube Shorts:

Target duration: 45–60 seconds.
Target narration: approximately 110–140 words,
adjusted naturally for the selected language.

Follow this structure:

A. HOOK (0–3 seconds)
Open with a compelling question, surprising fact
or relatable problem.

B. PROBLEM (3–12 seconds)
Describe the viewer's experience.

C. EXPLANATION (12–27 seconds)
Explain the relevant concept clearly and accurately.

D. PRACTICAL SOLUTION (27–48 seconds)
Give 2–3 useful, realistic and safe recommendations.

E. CLOSING (48–60 seconds)
Deliver a memorable takeaway and natural CTA.

Do not force this timing if it makes narration unnatural.

For LONG VIDEOS:
- Create a strong opening.
- Introduce the topic and learning objectives.
- Organize information into logical sections.
- Explain concepts with relevant examples.
- Include practical recommendations.
- Add smooth transitions.
- Finish with a useful summary and CTA.
- Avoid unnecessary repetition and filler.

==================================================
4. HEALTHCARE AND PHYSIOTHERAPY ACCURACY
==================================================

If the topic involves health, medicine or physiotherapy:

- Use responsible, evidence-informed educational language.
- Never diagnose the viewer.
- Never promise a cure or guaranteed result.
- Never exaggerate symptoms or medical risks.
- Do not invent research findings or statistics.
- Do not present one posture or exercise as suitable
  for every person.
- Explain uncertainty where appropriate.
- Distinguish established facts from general suggestions.
- Recommend individual assessment when appropriate.
- Mention urgent medical assessment for relevant
  warning signs when the topic requires it.

For musculoskeletal topics:
- Recognize that pain can have multiple causes.
- Avoid claiming that posture alone causes pain.
- Encourage comfortable movement and appropriate
  activity rather than fear of movement.
- Give exercise instructions only when they are
  relevant and reasonably safe for the audience.

Include a concise educational disclaimer.

==================================================
5. SCENE-BY-SCENE VIDEO PRODUCTION PLAN
==================================================

Create a detailed production table with these columns:

1. Scene number
2. Timestamp
3. Duration
4. Voiceover narration
5. Visual description
6. Camera angle or animation
7. On-screen caption
8. Transition or editing instruction

Requirements:
- Divide the video into meaningful scenes.
- Synchronize each scene with its narration.
- Give every scene a distinct visual purpose.
- Suggest realistic, professional visuals.
- Use appropriate anatomical graphics when useful.
- Specify close-ups, wide shots and camera movement.
- Keep on-screen captions short and readable.
- Never put long paragraphs on screen.
- Do not display captions unrelated to narration.
- Maintain consistent characters and visual style.
- Avoid unnecessary scene changes.

For healthcare animations, use clean and educational
visuals. Avoid frightening or misleading anatomy.

==================================================
6. VOICEOVER AND EDITING
==================================================

Provide:
- Complete narration separately from visual directions.
- Recommended narration tone and speaking speed.
- Background music mood.
- Sound effect suggestions where useful.
- Caption emphasis for important words.
- Editing and pacing recommendations.

Voiceover must be ready for text-to-speech
or recording without needing major rewriting.

==================================================
7. YOUTUBE PUBLISHING PACKAGE
==================================================

Provide:

VIDEO TITLE:
One compelling, accurate and searchable title.

ALTERNATIVE TITLES:
Three additional title options.

DESCRIPTION:
A natural, useful description relevant to the topic.
Avoid keyword stuffing.

HASHTAGS:
Five to eight relevant hashtags.

THUMBNAIL CONCEPT:
Describe the composition, subject, expression,
background, lighting and visual contrast.

THUMBNAIL TEXT:
Suggest 2–5 short, readable words.

PINNED COMMENT:
Write one useful question that encourages
genuine discussion.

CALL TO ACTION:
Use a natural channel-specific CTA.
For PhysioFix 60, use the channel name correctly.

==================================================
8. FINAL QUALITY CONTROL
==================================================

Before returning the result, check:

- Is the opening interesting?
- Is the information accurate and responsible?
- Does the script directly address the selected idea?
- Is the narration natural and grammatically correct?
- Are practical recommendations useful?
- Do scenes match the narration?
- Are timestamps realistic?
- Are captions short and synchronized?
- Is the title honest and engaging?
- Is there unnecessary repetition?
- Is the final package ready for production?

If any part is weak, improve it before returning.

IMPORTANT OUTPUT RULES:
- Use clear section headings.
- Use professional formatting.
- Do not expose your internal reasoning.
- Do not add generic filler.
- Do not claim guaranteed YouTube rankings or views.
- Return the complete finished video package.

Your final result must be original, accurate,
engaging, professionally structured and ready
for a real YouTube production workflow.
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
