import streamlit as st
from supabase import create_client, Client

# Connect to Supabase
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
supabase: Client = create_client(url, key)

st.title("Supabase Notes App (Full CRUD)")

# --- Search Bar ---
search_query = st.text_input("Search notes:")

# Fetch notes from Supabase
if search_query.strip():
    notes_response = (
        supabase.table("notes")
        .select("*")
        .ilike("content", f"%{search_query}%")
        .order("created_at", desc=True)
        .execute()
    )
else:
    notes_response = supabase.table("notes").select("*").order("created_at", desc=True).execute()

notes = notes_response.data

# --- Display notes in a table with edit/delete buttons ---
st.subheader("Existing Notes")
if notes:
    for note in notes:
        note_id = note["id"]
        note_content = note["content"]
        note_created = note["created_at"]

        # Container for each note
        with st.container():
            st.markdown(f"**Created At:** {note_created}")
            note_area = st.text_area(f"Note ID {note_id}", value=note_content, key=f"note_{note_id}")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Update", key=f"update_{note_id}"):
                    supabase.table("notes").update({"content": note_area}).eq("id", note_id).execute()
                    st.success("Note updated!")
                    st.experimental_rerun()
            with col2:
                if st.button("Delete", key=f"delete_{note_id}"):
                    supabase.table("notes").delete().eq("id", note_id).execute()
                    st.warning("Note deleted!")
                    st.experimental_rerun()
else:
    st.write("No notes found.")

# --- Add a new note ---
st.subheader("Add a new note")
note_input = st.text_area("Enter a note", key="new_note")
if st.button("Add note"):
    if note_input.strip():
        supabase.table("notes").insert({"content": note_input}).execute()
        st.success("Note added!")
        st.experimental_rerun()
