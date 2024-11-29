import os
import zipfile
import streamlit as st
from streamlit_option_menu import option_menu
from src.categorizer_func import read_prompt,generate_text,encode_image_to_base64,resize_image
import json
from src.categorizer_db import upload_to_blob,initialize_cosmos,insert_metadata_to_cosmos,search_cosmos_nested_field
from uuid import uuid4

import streamlit as st
from PIL import Image
import requests
from io import BytesIO

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
            for file_name in os.listdir(extract_path):
                file_path = os.path.join(extract_path, file_name)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            zip_ref.extractall(extract_path)

        image_files = [os.path.join(extract_path, f) for f in os.listdir(extract_path) if f.lower().endswith(("jpg", "jpeg", "png"))]

        if st.button("Generate Metadata for all images"):
            st.write("Results:")
            for image_path in image_files:
                resize_image(image_path)

                image_base_64=encode_image_to_base64(image_path)
                container = initialize_cosmos()
                blob_url = upload_to_blob(image_path)


                with st.spinner("processing...."):
                    response=generate_text(instructions,image_base_64)

                image_id = str(uuid4())
                insert_metadata_to_cosmos(container, image_id, blob_url, json.loads(response))


                st.write(f"{os.path.basename(image_path)} generated successfully!!!")
                data = json.loads(response)

                col1,col2=st.columns(2)

                with col1:
                    st.image(image_path, caption="Uploaded Image")

                with col2:
                    

                    st.json(data)








if selected == 'Searching of Categories':

    

    st.title("Search for Images by GPT Response")

    # User inputs
    field_path = st.selectbox(
        "Select a Field to Search", 
        ["gpt_response.meal_type", "gpt_response.seasonal_evergreen", "gpt_response.departments"]
    )
    field_value = st.text_input("Enter Value to Search (e.g., Mother's Day)")

    if st.button("Search"):
        if field_value.strip():
            # Query Cosmos DB
            results = search_cosmos_nested_field(field_path, field_value)

            if results:
                st.write(f"Found {len(results)} result(s) where {field_path} contains '{field_value}'.")

                for result in results:
                    blob_url = result.get("blob_url")
                    gpt_response = result.get("gpt_response", {})

                    # Fetch and display image
                    response = requests.get(blob_url)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, caption=blob_url, use_column_width=True)

                    # Display GPT response
                    st.json(gpt_response)
            else:
                st.write(f"No results found where {field_path} contains '{field_value}'.")
        else:
            st.write("Please enter a value to search.")




