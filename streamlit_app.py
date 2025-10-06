import streamlit as st
from supabase import create_client, Client

# Connect to Supabase
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
supabase: Client = create_client(url, key)

st.title("Supabase Notes App")

# Add a new note
note_input = st.text_area("Enter a note")
if st.button("Add note"):
    if note_input.strip():
        supabase.table("notes").insert({"content": note_input}).execute()
        st.success("Note added!")
        st.experimental_rerun()

# Fetch and display notes
notes = supabase.table("notes").select("*").order("created_at", desc=True).execute()
for note in notes.data:
    st.write(f"- {note['created_at']} — {note['content']}")
