import os
import zipfile
import streamlit as st
from streamlit_option_menu import option_menu
from src.categorizer_func import read_prompt,generate_text,encode_image_to_base64,resize_image


st.set_page_config(page_title="Alberson's Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")


with st.sidebar:
    selected = option_menu('Albertson Image category Prediction System',

                           ['Image Categorization predictor',
                            'Searching of Categories',
                            ],
                           menu_icon='robot',
                           icons=[ 'tags-fill', 'person'],
                           default_index=0)
    
if selected == 'Image Categorization predictor':

    st.title("Image Categorization Predictor")

    st.write(
    """
    This app uses OpenAI GPT-4o to analyze an image and generate a JSON metadata file based on the provided instructions.
    """
    )

    uploaded_zip = st.file_uploader("Upload a zip file containing images", type=["zip"])
    prompt_path ="Prompt_Albertsons.txt"

    if uploaded_zip and prompt_path:
        instructions=read_prompt(prompt_path)
        with zipfile.ZipFile(uploaded_zip,"r") as zip_ref:
            extract_path="temp_images"
            zip_ref.extractall(extract_path)

        image_files = [os.path.join(extract_path, f) for f in os.listdir(extract_path) if f.lower().endswith(("jpg", "jpeg", "png"))]

        if st.button("Generate Metadata for all images"):
            st.write("Results:")
            for image_path in image_files:
                resize_image(image_path)

                image_base_64=encode_image_to_base64(image_path)
                with st.spinner("processing...."):
                    response=generate_text(instructions,image_base_64)

                st.write(f"{os.path.basename(image_path)} generated successfully!!!")

                col1,col2=st.columns(2)

                with col1:
                    st.image(image_path, caption="Uploaded Image", use_column_width=True)

                with col2:
                    st.text(response)









if selected == 'Searching of Categories':

    st.title("In progress......")



