import streamlit as st
from supabase import create_client, Client

# Connect to Supabase
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
supabase: Client = create_client(url, key)

st.title("Supabase Notes App with Search")

# --- Search Bar ---
search_query = st.text_input("Search notes:")

# Fetch notes from Supabase
if search_query.strip():
    # Filter using case-insensitive match
    notes_response = supabase.table("notes").select("*").ilike("content", f"%{search_query}%").order("created_at", desc=True).execute()
else:
    notes_response = supabase.table("notes").select("*").order("created_at", desc=True).execute()

notes = notes_response.data

# Display notes in a table at the top
if notes:
    st.subheader("Existing Notes")
    st.table([{"Created At": note["created_at"], "Content": note["content"]} for note in notes])
else:
    st.write("No notes found.")

# --- Add a new note ---
st.subheader("Add a new note")
note_input = st.text_area("Enter a note")
if st.button("Add note"):
    if note_input.strip():
        supabase.table("notes").insert({"content": note_input}).execute()
        st.success("Note added!")
        st.experimental_rerun()  # Refresh the app to show new note
