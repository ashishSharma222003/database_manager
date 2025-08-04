import streamlit as st
from connector import DatabaseConnector

st.title("SQL Schema Annotator")

# Database connection inputs
st.sidebar.header("Database Connection")
db_type = st.sidebar.selectbox("DB Type", ["postgresql", "mysql", "sqlite"])

if db_type != "sqlite":
    db_user = st.sidebar.text_input("User")
    db_password = st.sidebar.text_input("Password", type="password")
    db_host = st.sidebar.text_input("Host", value="localhost")
    db_port = st.sidebar.number_input("Port", value=5432)
else:
    db_user = ""
    db_password = ""
    db_host = ""
    db_port = ""
db_name = st.sidebar.text_input("Database Name")
safe_mode = st.sidebar.checkbox("Safe Mode", value=True)

if st.sidebar.button("Connect"):
    connector = DatabaseConnector(db_type, db_user, db_password, db_host, db_port, db_name, safe_mode)
    try:
        connector.connect()
        st.success("Connected to database!")
        tables = connector.get_tables()
        schema = connector.get_schema()
        st.session_state["schema"] = schema
        st.session_state["tables"] = tables
    except Exception as e:
        st.error(f"Connection failed: {e}")

if "schema" in st.session_state:
    schema = st.session_state["schema"]
    connector = DatabaseConnector(db_type, db_user, db_password, db_host, db_port, db_name, safe_mode)
    summarized = connector.summarize_schema(schema)
    st.subheader("Summarized Schema (JSON)")
    st.json(summarized)
    table_options = list(summarized.keys())
    selected_table = st.selectbox("Select a table to annotate", table_options)
    st.header("Annotate Tables and Columns")
    annotations = {}
    # Only show annotation fields for the selected table
    details = schema[selected_table]
    table_desc = st.text_input(f"Description for table '{selected_table}'", key=f"table_{selected_table}")
    col_descs = {}
    for col in [list(c.keys())[0] for c in details["columns"]]:
        col_desc = st.text_input(f"Description for column '{selected_table}.{col}'", key=f"col_{selected_table}_{col}")
        col_descs[col] = col_desc
    annotations[selected_table] = {"table_description": table_desc, "columns": col_descs}
    if st.button("Save Annotations"):
        if "annotations" not in st.session_state:
            st.session_state["annotations"] = {}
        st.session_state["annotations"].update(annotations)
        st.success("Annotations saved! You can now use them for vector DB upload.")
        st.write(st.session_state["annotations"])
