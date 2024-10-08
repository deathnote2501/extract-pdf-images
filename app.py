import streamlit as st
import pdfplumber
import os
import tempfile
import base64
from PIL import Image

# Define the password
PASSWORD = st.secrets["PASSWORD"]

def extract_images_from_pdf(file):
    images = []
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            for img in page.images:
                # Extract the image object using the object ID
                image_data = page.extract_image(img['object_id'])
                if image_data:
                    # Get the image bytes and format
                    img_bytes = image_data['image']
                    img_ext = image_data['format']
                    
                    # Convert the bytes into a PIL image
                    pil_image = Image.open(io.BytesIO(img_bytes))
                    images.append((pil_image, f"page_{i+1}.{img_ext}"))
    return images

def save_images(images):
    temp_files = []
    for i, (img, name) in enumerate(images):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{name}")
        img.save(temp_file.name)
        temp_files.append(temp_file.name)
    return temp_files

def main():
    st.title("Extraction des images depuis un PDF")
    st.write("Par Jérome IAvarone")

    # Password input
    password = st.text_input("Entrez le mot de passe :", type="password")

    if password == PASSWORD:
        st.write("")
        st.write("Chargez votre fichier PDF ci-dessous :")

        uploaded_file = st.file_uploader("", type=["pdf"])
        
        if st.button("Extraire les images"):
            if not uploaded_file:
                st.warning("Chargez un fichier PDF.")
            else:
                images = extract_images_from_pdf(uploaded_file)

                if images:
                    st.success(f"{len(images)} images extraites avec succès :)")
                    temp_files = save_images(images)

                    for temp_file in temp_files:
                        with open(temp_file, 'rb') as f:
                            b64 = base64.b64encode(f.read()).decode()
                            href = f'<a href="data:image/png;base64,{b64}" download="{os.path.basename(temp_file)}" style="font-size:20px;">>> Télécharger l\'image {os.path.basename(temp_file)}</a>'
                            st.markdown(href, unsafe_allow_html=True)
                else:
                    st.warning("Aucune image trouvée dans le PDF.")
        
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<p style='text-align: center;'>© 2024 Jérome IAvarone - jerome.iavarone@gmail.com</p>", unsafe_allow_html=True)

    elif password:
        st.error("Mot de passe incorrect")

if __name__ == "__main__":
    main()
