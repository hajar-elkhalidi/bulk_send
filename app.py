import streamlit as st
import os

st.set_page_config(page_title="Bulk Email Sender", page_icon="📧")
st.title("📧 Bulk Email Sender via Robot Framework")

# --- UI ---
sender_email = st.text_input("Votre adresse Gmail", key="sender_email")
app_password = st.text_input(
    "App Password", 
    type="password",
    help="Générez-le depuis https://myaccount.google.com/apppasswords après avoir activé la validation en deux étapes.",
    key="app_password"
)
subject = st.text_input("Sujet de l’email", key="subject")
body = st.text_area("Corps du message", key="body")
attachment = st.file_uploader("Fichier à joindre (PDF uniquement)", type=["pdf"], key="attachment")
recipients = st.text_area("Adresses des destinataires (une par ligne)", key="recipients")

# --- Validation ---
if st.button("📤 Envoyer les emails"):

    # --- 1. Écriture des fichiers ---
    with open("resources/credentials.resource", "w", encoding="utf-8") as f:
        f.write("*** Variables ***\n")
        f.write(f"${{email}}    {sender_email}\n")
        f.write(f"${{app_pass}}    {app_password}\n")

    with open("resources/email.resource", "w", encoding="utf-8") as f:
        f.write("*** Variables ***\n")
        f.write(f"${{EMAIL_SUBJECT}}    {subject}\n")
        f.write(f"${{EMAIL_BODY}}       {body}\n")
        f.write(f"${{ATTACHMENT_PATH}}  files/dummy.pdf\n")

    if attachment:
        with open("files/dummy.pdf", "wb") as f:
            f.write(attachment.read())

    recipient_list = recipients.strip().split("\n")
    with open("resources/recipients_emails.resource", "w", encoding="utf-8") as f:
        f.write("*** Variables ***\n")
        f.write("@{RECIPIENTS}    " + "    ".join(recipient_list) + "\n")

    # --- 2. Exécution du Robot Framework ---
    result = os.system("robot send_email.robot")

    # --- 3. Message + RESET ---
    if result == 0:
        st.success("📨 Emails envoyés avec succès !")

        # ✅ Clear complet du formulaire (pas de .pop, pas d’erreur)
        st.session_state.clear()
        st.rerun()

    else:
        st.error("❌ Une erreur est survenue lors de l’envoi.")