
import streamlit as st
import csv
import io

st.set_page_config(
    page_title="SmallTube Discovery AI",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 SmallTube Discovery AI")
st.write("Plan better YouTube videos for your channel.")

channel = st.text_input("Channel name", "PhysioFix 60")
topic = st.text_input(
    "Video topic",
    "Lower back pain after sitting"
)
languages = st.multiselect(
    "Languages",
    ["English", "Urdu"],
    default=["English", "Urdu"]
)
formats = st.multiselect(
    "Video formats",
    ["YouTube Shorts", "Long video"],
    default=["YouTube Shorts", "Long video"]
)

if st.button("Generate my video plan", type="primary"):
    if not topic.strip():
        st.error("Please enter a video topic.")
    else:
        st.subheader("Video ideas")

        ideas = [
            f"Why does {topic.lower()} happen?",
            f"3 common mistakes about {topic.lower()}",
            f"What should you do about {topic.lower()}?",
            f"When should you seek professional help for {topic.lower()}?"
        ]

        for i, idea in enumerate(ideas, 1):
            st.write(f"**Idea {i}:** {idea}")

        st.subheader("Sample script")

        if "English" in languages:
            st.markdown("**English**")
            st.write(
                f"Hook: Are you concerned about {topic.lower()}?"
            )
            st.write(
                "Explain possible contributing factors in simple "
                "language. Offer safe, general educational advice. "
                "Remind viewers that symptoms can have different "
                "causes and a qualified professional can assess them."
            )
            st.write(
                f"CTA: Follow {channel} for simple health education."
            )

        if "Urdu" in languages:
            st.markdown("**اردو**")
            st.write(f"کیا آپ {topic} کے بارے میں پریشان ہیں؟")
            st.write(
                "اس کی مختلف وجوہات ہو سکتی ہیں۔ اپنی کیفیت کے "
                "مطابق درست رہنمائی کے لیے مستند ہیلتھ پروفیشنل "
                "سے مشورہ کریں۔"
            )
            st.write(
                f"{channel} کو فالو کریں، مزید آسان معلومات کے لیے۔"
            )

        st.subheader("Suggested format")
        for fmt in formats:
            st.write(f"• {fmt}")

        st.info(
            "Prototype mode: these are template-based suggestions, "
            "not live YouTube search data or guaranteed recommendations."
        )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Channel", "Topic", "Video idea"])
        for idea in ideas:
            writer.writerow([channel, topic, idea])

        st.download_button(
            "Download ideas as CSV",
            data=output.getvalue(),
            file_name="smalltube_video_ideas.csv",
            mime="text/csv"
        )

st.divider()
st.caption(
    "SmallTube Discovery AI — planning assistant for original content."
)
