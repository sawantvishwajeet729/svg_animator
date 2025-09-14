import streamlit as st
import base64
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from src import *

#Setup the API key
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

#Setup the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# --- Page Configuration ---
st.set_page_config(
    page_title="SVG Animator AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Helper Functions ---

def render_svg(svg_string: str):
    """
    Renders an SVG string in the Streamlit app.
    This function handles the necessary encoding to display SVGs properly.
    """
    # b64-encode the SVG string
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")
    # Add the b64 encoded string to the html img tag
    html = f'<div style="text-align: center; border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9;"><img src="data:image/svg+xml;base64,{b64}" width="300" height="300"/></div>'
    st.write(html, unsafe_allow_html=True)


def llm_backend(svg_content: str, user_prompt: str) -> str:
    """
    --- THIS IS A SIMULATED BACKEND ---
    In a real application, this function would:
    1. Send the `svg_content` and `prompt` to your backend server.
    2. The backend would interact with an LLM (e.g., via an API).
    3. The LLM would process the request and return a new SVG string with animation tags.
    4. This function would return that new SVG string.
    
    For demonstration, this function waits for a few seconds and then returns a
    pre-defined animated SVG. It ignores the actual input content.
    """
    #get the analysis and svg text from the svg
    svg_text, analysis_report = analyse_svg_elements(svg_content, llm)

    #update the ids in svg_text
    updated_svg_text = update_svg_with_ids(svg_text, analysis_report, llm)

    #animate the svg using llm
    animated_svg = animate_svg(updated_svg_text=updated_svg_text, analysis_report=analysis_report, user_prompt=user_prompt, llm=llm)

    return animated_svg


# --- Main Application UI ---

st.title("🎨 SVG Animator AI")
st.markdown("Upload your static `.svg` file, describe the animation you want, and let our AI bring it to life!")

# Initialize session state to hold the animated SVG result
if 'animated_svg' not in st.session_state:
    st.session_state.animated_svg = None

st.sidebar.header("How it works")
st.sidebar.info(
    "1. **Upload SVG**: Choose a `.svg` file from your computer.\n"
    "2. **Describe Animation**: Write a clear prompt (e.g., 'make the circle bounce').\n"
    "3. **Generate**: Click the button to send your request to the AI.\n"
    "4. **View & Download**: See the result and download your new animated SVG."
)
st.sidebar.warning("For better results use svg files from https://fonts.google.com/icons.")


# --- Step 1: File Uploader ---
st.header("Step 1: Upload your SVG File")
uploaded_file = st.file_uploader(
    "Choose a .svg file",
    type="svg",
    help="Only .svg files are accepted"
)

# Main container to hold the logic after a file is uploaded
if uploaded_file is not None:
    
    # Read the uploaded SVG content
    try:
        svg_content = uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading or decoding file: {e}")
        st.stop()

    # Create two columns for a better layout
    col1, col2 = st.columns(2)

    with col1:
        # --- Step 2: Display Uploaded SVG ---
        st.subheader("Your Uploaded Image")
        render_svg(svg_content)

    with col2:
        # --- Step 3: Text Box for Animation Prompt ---
        st.subheader("Step 2: Describe the Animation")
        animation_prompt = st.text_area(
            "Enter your animation prompt:",
            placeholder="e.g., 'Make the rectangle rotate 360 degrees indefinitely.'\n'Cause the star to pulse in size.'\n'Change the circle's color from blue to green.'",
            height=150
        )
        
        # Generate Animation Button
        if st.button("✨ Generate Animation", type="primary", use_container_width=True):
            if animation_prompt:
                # --- THIS IS WHERE YOU CALL YOUR BACKEND ---
                # The result from the backend is stored in session state
                st.session_state.animated_svg = llm_backend(svg_content, animation_prompt)
            else:
                st.warning("Please enter an animation prompt before generating.")

# Check if an animated SVG has been generated and stored in session state
if st.session_state.animated_svg:
    st.divider()
    st.header("Step 3: Your Animated Result")

    # --- Step 4: Display the Animated SVG ---
    render_svg(st.session_state.animated_svg)
    
    st.success("Animation generated successfully!")

    # --- Step 5: Download Button ---
    st.download_button(
        label="📥 Download Animated SVG",
        data=st.session_state.animated_svg,
        file_name="animated_image.svg",
        mime="image/svg+xml",
        use_container_width=True
    )