#Import the necessary libraries
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import BaseOutputParser

#Setup the API key
os.environ["GOOGLE_API_KEY"] = st.secrets['GOOGLE_API_KEY']

#Setup the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def analyse_svg_elements(svg_text, llm):
    """
    Reads the svg file as a text file then Analyse and understand the elements of the SVG file.

    Args:
        svg_path (str): The path to the svg file.

    Returns:
        svg_text(str): The text version of the svg file.
        analysis_report(str): A report of the elements in the svg file.
    """

    # Create chat prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at analyzing SVG files. 
        Describe the visual elements, shapes, colors, text, and overall design present in the SVG."""),
        ("human", """SVG Content:

        {svg_content}
        """)
            ])

    # Create chain
    chain = prompt | llm

    #invoke the chain
    response = chain.invoke({
        "svg_content": svg_text
        })
    
    return svg_text, response.content

# Define your custom output parser
class SvgOutputParser(BaseOutputParser[str]):
    """
    Parses the LLM output to extract the SVG code block.
    """
    def parse(self, text: str) -> str:
        """Parses the input text and returns the SVG code."""
        # Use regex to find the SVG content. re.DOTALL makes '.' match newlines.
        match = re.search(r'<svg.*</svg>', text, re.DOTALL)
        if not match:
            raise ValueError("Failed to find SVG code in the LLM output.")
        # Return the matched SVG code
        return match.group(0).strip()


# Update the SVG file (XML format) with appropriate ids where required. (LLM)

def update_svg_with_ids(svg_txt, analysis_report, llm):
    """
    Update the svg file with appropriate ids where required.

    Args:
        svg_txt (str): The text version of the svg file.
        analysis_report (str): A report of the elements in the svg file.

    Returns:
        updted_svg_text(str): The updated text version of the svg file.
    """

    # Create chat prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at updating SVG files. 
        Analyse the SVG content and update the file with appropriate ids where required based on the analysis report.
        output should only include the xml text which can be saved as a svg image"""),
        ("human", """SVG text:

        {svg_txt}
        """)
            ])

    # Instantiate the parser
    svg_parser = SvgOutputParser()

    # Create chain
    chain = prompt | llm | svg_parser

    #invoke the chain
    response = chain.invoke({
        "svg_txt": svg_txt
        })

    return response



# Create a new SVG (XML) with the animation prompt. (LLM)

def animate_svg(updated_svg_text, analysis_report, user_prompt, llm):
    """
    Create a new SVG file with animation.

    Args:
        updated_svg_text (str): The text version of the svg file with updated ids.
        analysis_report (str): A report of the elements in the svg file.
        user_prompt (str): Animation prompt from the user

    Returns:
        animated_svg(str): The updated text version of the svg file with animation.
    """

    system_prompt_text = """
You are an expert SVG Animation Engineer. Your sole function is to take a static SVG, an analysis of its components, and a user's animation request, and then produce a new, animated SVG. You will use SVG's native SMIL animation technology to achieve this.

**Your Goal:** To intelligently inject SMIL animation tags (`<animate>`, `<animateTransform>`, etc.) into the provided `svg_text` to bring the user's vision to life, returning a single, self-contained, animated SVG file.

---

**INPUTS:**

1.  **`svg_text`**: A string containing the complete XML content of the original, static SVG.
2.  **`analysis_report`**: A structured description of the SVG, identifying key shapes, paths, groups, and their corresponding IDs. This is your map to the SVG's structure.
3.  **`user_prompt`**: A natural language instruction from the user describing the desired animation.

---

**YOUR PROCESS:**

1.  **Synthesize Information:** Carefully read the `user_prompt` and cross-reference it with the `analysis_report`. Your first step is to identify exactly which elements (e.g., `<path id="line1">`, `<circle id="dot">`) are the targets for animation.

2.  **Devise an Animation Plan:**
    * **Choose the Right Tool:** You MUST use SMIL. This ensures the SVG is self-contained. Do not use CSS or JavaScript.
        * Use `<animate>` for attributes like `d`, `points`, `fill`, `stroke-opacity`, `x`, `y`, `r`.
        * Use `<animateTransform>` for transformations like `translate`, `scale`, or `rotate`.
    * **Determine Attributes:** Based on the user's prompt (e.g., "make it move," "change color," "spin around"), determine the specific SVG attribute to animate (e.g., `transform`, `fill`, `d`).
    * **Define Keyframes:** Plan the animation's values. Use a `values` attribute with a semicolon-separated list for a multi-step animation (e.g., `values="0; 10; 0"`). The animation should start and end in the SVG's original state to ensure a seamless loop.
    * **Set Timing:**
        * **Duration (`dur`)**: Choose a reasonable duration, typically between `1.5s` and `3s`, for a pleasant viewing experience.
        * **Looping (`repeatCount`)**: Always set this to `"indefinite"` for a continuous animation.
        * **Staggering (`begin`)**: If animating multiple elements, apply small delays to each subsequent element (e.g., `begin="0s"`, `begin="0.2s"`, `begin="0.4s"`) to create a more dynamic and professional-looking effect.

3.  **Construct the Final SVG:**
    * Take the original `svg_text` as your base.
    * Carefully insert the planned `<animate.../>` tags as children of their target elements.
    * **Crucially, do not alter any other part of the SVG.** Preserve all existing elements, attributes, and formatting.

---

**OUTPUT REQUIREMENTS:**

* Your entire response MUST be the final, complete, and valid SVG/XML code.
* Enclose the code in a single markdown code block.
* **DO NOT** include any conversational text, explanations, or apologies before or after the code block. Your output is the code and nothing else.
"""

    # The human-readable message template that will contain the dynamic inputs.
    human_message_template = """
Here is the SVG and the animation request. Please generate the animated SVG.

**SVG Text:**
```xml
{svg_text}
```

**Analysis Report:**
```
{analysis_report}
```

**User Animation Prompt:**
```
{user_prompt}
```
"""


    # Create the ChatPromptTemplate from the system and human message strings.
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_text),
        ("human", human_message_template)
    ])

    # Instantiate the parser
    svg_parser = SvgOutputParser()

    # Create chain
    chain = prompt | llm | svg_parser

    #invoke the chain
    response = chain.invoke({
        "svg_text": updated_svg_text,
        "analysis_report": analysis_report,
        "user_prompt": user_prompt
        })

    return response

#function to write the file to local
def write_svg(svg_text, output_name):
    """
    Write the new animated SVG file to the given path

    Args:
        svg_text (str): This is the animated SVG (XML format) created by llm
        output_name (str): The desired name for the svg file. Add the custom path if required.

    Returns:
        None
    """

    #add the extension to the output name
    output_name = f"{output_name}.svg"

    #write the file to path
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(svg_text)
