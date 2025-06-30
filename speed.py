import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every second to handle timers
st_autorefresh(interval=1000, key="auto_refresh")

# List of 75 sample sentences
sentences = [
    "The quick brown fox jumps over the lazy dog",
    "A journey of a thousand miles begins with a single step",
    "Practice makes perfect in all things you do",
    "The sun sets slowly behind the mountain",
    "A clear sky on a warm summer day",
    "Stars twinkle brightly in the night sky",
    "The river flows gently through the valley",
    "Birds chirp happily in the early morning",
    "A warm breeze rustles the autumn leaves",
    "The moon casts a silver glow over the lake",
    "Children play joyfully in the green meadow",
    "The old oak tree stands tall and strong",
    "Waves crash softly against the sandy shore",
    "A quiet village rests at the foot of the hill",
    "The smell of fresh bread fills the kitchen",
    "Clouds drift lazily across the blue sky",
    "The wind whispers secrets to the ancient trees",
    "A cozy fireplace warms the small cabin",
    "The bright flowers bloom in the garden",
    "A lone wolf howls under the starry night",
    "Leaves crunch beneath your feet in the fall",
    "Raindrops create ripples in the puddles",
    "The fireflies dance in the dark summer night",
    "Snowflakes land softly on the window ledge",
    "The lighthouse guides ships through thick fog",
    "Footprints vanish slowly in the shifting sand",
    "Lanterns glow warmly during the evening festival",
    "The kitten purrs while curled on the couch",
    "Books lined neatly on the dusty old shelf",
    "Freshly brewed coffee fills the morning air",
    "The hiker reaches the summit with joy",
    "Ocean waves sing a lullaby to the shore",
    "Golden rays peek through the tall trees",
    "Wind chimes sing with the passing breeze",
    "The puppy chases butterflies in the yard",
    "Footsteps echo in the quiet hallway",
    "The lantern flickers in the silent night",
    "A feather floats gently to the ground",
    "The violinist plays a haunting tune",
    "Morning dew glistens on the green grass",
    "Sunlight dances on the rippling lake surface",
    "Thunder rumbles through the evening sky",
    "The cat stretches lazily on the windowsill",
    "Campfire smoke curls into the cool air",
    "The waterfall thunders down the rocky cliff",
    "Soft snow blankets the quiet countryside",
    "The owl hoots in the stillness of night",
    "The tent flaps in the mountain wind",
    "The sky turns pink at the break of dawn",
    "Raindrops race down the glass like tears",
    "The child laughs as the kite takes flight",
    "The candle flickers in the dark hallway",
    "The wind scatters petals across the path",
    "The engine hums softly on the quiet road",
    "Sunbeams warm the sleepy forest floor",
    "The fog rolls in over the harbor",
    "The plane cuts through clouds in the sky",
    "The horse gallops across the open field",
    "The dancer spins gracefully on the stage",
    "The treehouse creaks in the summer breeze",
    "The librarian sorts books in silent rows",
    "The cafe buzzes with morning chatter",
    "The stars shimmer above the desert sands",
    "The artist dips the brush into bright paint",
    "Leaves swirl in circles on the pavement",
    "The breeze carries laughter across the park"
]

# Initialize session state
if "status" not in st.session_state:
    st.session_state.status = "idle"
    st.session_state.sentences = random.sample(sentences, 8)
    st.session_state.full_text = " ".join(st.session_state.sentences)
    st.session_state.countdown_start = None
    st.session_state.typing_start = None
    st.session_state.input_text = ""

# UI Header
st.title("⌨️ Typing Speed Test")
st.markdown("#### 🚀 Instructions:")
st.markdown("- Click **Start Typing** to begin a 3-second countdown.")
st.markdown("- Typing is disabled during the countdown.")
st.markdown("- The test will auto-end after **60 seconds**.")
st.markdown("- **You should press CTRL+ENTER at last **2 seconds** or **ANYTIME** to validate the Typed text.**")
st.markdown("- You will get extra **2 seconds** to put your cursor on the typing box.")

st.markdown("---")

# Start Button
if st.session_state.status == "idle":
    if st.button("🚀 Start Typing"):
        st.session_state.status = "countdown"
        st.session_state.countdown_start = time.time()
        st.rerun()

# Countdown Phase
if st.session_state.status == "countdown":
    time_passed = time.time() - st.session_state.countdown_start
    countdown_left = 3 - int(time_passed)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📜 Type these 8 sentences:")
        for i, s in enumerate(st.session_state.sentences, 1):
            st.markdown(f"**{i}.** {s}")

    with col2:
        st.markdown("### ✍️ Typing Box (Disabled)")
        st.text_area("Waiting for countdown to end...", value="", height=250, disabled=True, label_visibility="collapsed")

    if countdown_left > 0:
        st.warning(f"⏳ Typing will begin in {countdown_left} seconds...")
    else:
        st.session_state.status = "typing"
        st.session_state.typing_start = time.time()
        st.rerun()

# Typing Phase
elif st.session_state.status == "typing":
    elapsed = time.time() - st.session_state.typing_start
    remaining = 62 - int(elapsed)

    if remaining <= 0:
        st.session_state.status = "submitted"
        st.rerun()
    else:
        st.info(f"⏱️ Time Remaining: {remaining} seconds")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📜 Type these 8 sentences:")
            for i, s in enumerate(st.session_state.sentences, 1):
                st.markdown(f"**{i}.** {s}")

        with col2:
            st.markdown("### ✍️ Start Typing Below")
            st.caption(
                "Need to press CTRL+ENTER at last **2 seconds** or **ANY POINT** to validate the Typed text."
                " \n Auto-submits in 60 seconds.")
            # Update the input text in session state as the user types
            st.session_state.input_text = st.text_area(
                "Typing Box:",
                value=st.session_state.input_text,
                height=250,
                key="typing_box",
                label_visibility="collapsed"
            )

# Submission Phase
elif st.session_state.status == "submitted":
    typed_words = st.session_state.input_text.split()
    target_words = st.session_state.full_text.split()

    correct = sum(1 for a, b in zip(typed_words, target_words) if a == b)
    total_typed = len(typed_words)
    wpm = correct
    accuracy = (correct / total_typed * 100) if total_typed else 0

    st.success("✅ Test Completed!")
    st.info(f"📝 Words Typed: {total_typed}")
    st.success(f"✅ Correct Words: {correct}")
    st.warning(f"🚀 WPM: {wpm}")
    st.info(f"🎯 Accuracy: {accuracy:.2f}%")

    if st.button("🔁 Try Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
