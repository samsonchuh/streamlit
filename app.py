import streamlit as st
import datetime
import calendar
import pandas as pd
import numpy as np
import os
from db_utils import get_db_connection, ensure_users_table, add_user, update_user, delete_user, get_all_users, ensure_auth_table, check_login, register_user

st.set_page_config(layout="wide")

def tab_str_input():
    st.header("String Input Test App")
    user_input = st.text_input("Enter a string:")
    msg = ""
    if st.button("Check", key="check1"):
        if not user_input:
            msg = "Error: Please enter a string."
            st.error(msg)
        else:
            msg = f"You entered: {user_input}"
            st.success(msg)
    else:
        st.info("Please enter a string and click 'Check'.")

def tab_date_picker():
    st.header("Date Picker Test")
    date = st.date_input("Pick a date:")
    st.write(f"Selected date: {date}")

def tab_slider():
    st.header("Slider Test")
    value = st.slider("Select a value", 0, 100, 50)
    st.write(f"Slider value: {value}")

def tab_checkbox():
    st.header("Checkbox Test")
    checked = st.checkbox("Check me!")
    st.write(f"Checked: {checked}")

def tab_radio():
    st.header("Radio Test")
    option = st.radio("Choose one:", ["Option 1", "Option 2", "Option 3"])
    st.write(f"Selected: {option}")

def tab_selectbox():
    st.header("Selectbox Test")
    select = st.selectbox("Pick an item:", ["Apple", "Banana", "Cherry"])
    st.write(f"Selected: {select}")

def tab_file_uploader():
    st.header("File Uploader Test")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        st.write(f"Uploaded file: {uploaded_file.name}")
    else:
        st.info("No file uploaded yet.")

def tab_image():
    st.header("Image Test")
    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png",
        caption="Streamlit Logo",
        use_column_width=True
    )

def tab_chart():
    st.header("Chart Test")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["A", "B", "C"]
    )
    st.line_chart(chart_data)

def tab_markdown():
    st.header("Markdown Test")
    st.markdown("""
    # Markdown Example
    - **Bold**
    - *Italic*
    - [Streamlit Website](https://streamlit.io)
    > Blockquote
    """)

def tab_calendar():
    st.header("Calendar View")
    today = datetime.date.today()
    current_year = today.year
    months = [calendar.month_name[m] for m in range(1, 13)]
    st.subheader("Tasks")
    if 'tasks' not in st.session_state:
        st.session_state['tasks'] = []
    with st.form("add_task_form"):
        task_date = st.date_input("Task Date", value=today, key="task_date")
        task_name = st.text_input("Task Name", key="task_name")
        submitted = st.form_submit_button("Add Task")
        if submitted and task_name:
            st.session_state['tasks'].append({'date': task_date, 'name': task_name})
            st.success(f"Task '{task_name}' added for {task_date}")
    if st.session_state['tasks']:
        st.write("### Task List")
        for t in st.session_state['tasks']:
            st.write(f"- {t['date']}: {t['name']}")
    else:
        st.info("No tasks added yet.")
    task_dates = set(t['date'] for t in st.session_state['tasks'])
    for i, month in enumerate(months):
        if i % 3 == 0:
            cols = st.columns(3)
        with cols[i % 3]:
            st.markdown(f"### {month} {current_year}")
            cal = calendar.monthcalendar(current_year, i+1)
            cal_str = "| Mo | Tu | We | Th | Fr | Sa | Su |\n|----|----|----|----|----|----|----|\n"
            for week in cal:
                week_str = "|"
                for day in week:
                    cell = ""
                    if day == 0:
                        cell = " "
                    else:
                        cell_date = datetime.date(current_year, i+1, day)
                        if cell_date == today:
                            cell = f"**<span style='color:red'>{day}</span>**"
                        elif cell_date in task_dates:
                            cell = f"**<span style='background-color:yellow'>{day}</span>**"
                        else:
                            cell = f"{day}"
                    week_str += f" {cell} |"
                cal_str += week_str + "\n"
            st.markdown(cal_str, unsafe_allow_html=True)

def tab_tree():
    st.header("Tree Structure Test")
    st.write("Below is a sample tree structure with 3 levels: Country > Province > City")
    tree_data = {
        "China": {
            "Guangdong": ["Guangzhou", "Shenzhen", "Dongguan"],
            "Zhejiang": ["Hangzhou", "Ningbo", "Wenzhou"]
        },
        "USA": {
            "California": ["Los Angeles", "San Francisco", "San Diego"],
            "Texas": ["Houston", "Dallas", "Austin"]
        }
    }
    nav_col, content_col = st.columns([0.3, 0.7])
    with nav_col:
        st.subheader("Navigation")
        def render_nav(data, path=None):
            if path is None:
                path = []
            for key, value in data.items():
                node_path = path + [key]
                node_id = "/".join(node_path)
                if isinstance(value, dict):
                    expanded = st.expander(f"{key}", expanded=False)
                    with expanded:
                        render_nav(value, node_path)
                    if st.button(f"Select {key}", key=f"select_{node_id}"):
                        st.session_state['selected_node'] = node_path
                elif isinstance(value, list):
                    exp = st.expander(f"{key}", expanded=False)
                    with exp:
                        for item in value:
                            item_path = node_path + [item]
                            item_id = "/".join(item_path)
                            if st.button(f"Select {item}", key=f"select_{item_id}"):
                                st.session_state['selected_node'] = item_path
        if 'selected_node' not in st.session_state:
            st.session_state['selected_node'] = []
        render_nav(tree_data)
    with content_col:
        st.subheader("Node Details")
        selected = st.session_state.get('selected_node', [])
        if not selected:
            st.info("Select a node from the navigation area to see details.")
        else:
            node = tree_data
            for part in selected:
                if isinstance(node, dict):
                    node = node.get(part, {})
                elif isinstance(node, list):
                    break
            st.markdown(f"### Path: {' / '.join(selected)}")
            st.markdown("---")
            if isinstance(node, dict):
                st.markdown(f"**Type:** Group/Branch")
                st.markdown(f"**Children:** {', '.join(node.keys()) if node else 'None'}")
            elif isinstance(node, list):
                st.markdown(f"**Type:** List/Leaf")
                st.markdown(f"**Items:** {', '.join(node)}")
            else:
                st.markdown(f"**Value:** {node}")

def tab_table():
    st.header("Table Test: China Provinces Population & GDP")
    data = [
        ["Guangdong", 126012510, 129118.58],
        ["Shandong", 101527453, 87435.95],
        ["Henan", 98821739, 58900.97],
        ["Jiangsu", 84748016, 122875.60],
        ["Sichuan", 83674866, 56749.77],
        ["Hebei", 74610235, 40394.26],
        ["Hunan", 66444864, 48717.81],
        ["Anhui", 61027171, 42961.19],
        ["Hubei", 57752557, 53734.82],
        ["Zhejiang", 65403097, 78984.00],
        ["Guangxi", 50126804, 26500.37],
        ["Yunnan", 48300000, 28983.00],
        ["Jiangxi", 45188635, 32047.70],
        ["Liaoning", 42591407, 28980.00],
        ["Fujian", 41540000, 53104.00],
        ["Shaanxi", 39528999, 32777.54],
        ["Heilongjiang", 31850000, 15900.00],
        ["Shanxi", 34915616, 23200.00],
        ["Chongqing", 32054159, 29129.03],
        ["Jilin", 23800000, 13000.00],
        ["Gansu", 25019831, 11200.00],
        ["Inner Mongolia", 24049155, 20600.00],
        ["Xinjiang", 25852345, 15900.00],
        ["Shanghai", 24870895, 44652.80],
        ["Beijing", 21893095, 43798.00],
        ["Tianjin", 13866009, 15695.00],
        ["Hainan", 10230000, 6818.22],
        ["Ningxia", 7202654, 4658.00],
        ["Qinghai", 6030000, 3610.00],
        ["Tibet", 3648100, 2132.63]
    ]
    df = pd.DataFrame(data, columns=["Province", "Population", "GDP (100M RMB)"])
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "Province": st.column_config.TextColumn(
                "Province",
                help="Province name",
                width="small",
                pinned=True
            ),
            "Population": st.column_config.NumberColumn(
                "Population",
                help="Population count",
                width="medium",
                format="compact"
            ),
            "GDP (100M RMB)": st.column_config.NumberColumn(
                "GDP (100M RMB)",
                help="GDP in 100 million RMB",
                width="large",
                format="accounting",
            )
        },
        column_order=["Province", "Population", "GDP (100M RMB)"]
    )
    st.caption(":moon: For a true dark background, enable Streamlit's dark theme in the app settings (top-right menu).\n\n:bookmark_tabs: Paging is enabled by default for st.dataframe when the table is large.")

def tab_database():
    st.header("Database Test (SQLite)")
    db_path = os.path.join(os.path.dirname(__file__), "test_db.sqlite3")
    conn = get_db_connection(db_path)
    ensure_users_table(conn)
    # Add user form
    with st.form("add_user_form"):
        name = st.text_input("Name")
        chinese_name = st.text_input("Chinese Name (中文名)")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        birthday = st.date_input("Birthday")
        skills_input = st.text_input("Skills (comma separated, e.g. Python,SQL,数据分析)")
        submitted = st.form_submit_button("Add User")
        if submitted and name:
            skills = ','.join([s.strip() for s in skills_input.split(',') if s.strip()]) if skills_input else ''
            add_user(conn, name, chinese_name, age, birthday.strftime('%Y-%m-%d'), skills)
            st.success(f"User '{name}' added.")
    # Show users
    st.write("### Users Table")
    users_df = get_all_users(conn)
    if not users_df.empty and 'skills' in users_df.columns:
        users_df['skills'] = users_df['skills'].fillna('').apply(lambda x: '  '.join([f'`{s.strip()}`' for s in x.split(',') if s.strip()]))
    for idx, row in users_df.iterrows():
        cols = st.columns([2, 2, 1.5, 2, 2, 2, 1, 1])
        cols[0].write(row['name'])
        cols[1].write(row.get('chinese_name', ''))
        cols[2].write(row['age'])
        cols[3].write(row['birthday'])
        cols[4].write(row['skills'])
        edit_key = f"edit_{row['id']}"
        delete_key = f"delete_{row['id']}"
        if cols[5].button("Edit", key=edit_key):
            st.session_state['edit_user_id'] = row['id']
            st.session_state['edit_user_data'] = row
        if cols[6].button("Delete", key=delete_key):
            st.session_state['delete_user_id'] = row['id']
    if 'edit_user_id' in st.session_state:
        user_id = st.session_state['edit_user_id']
        user_data = st.session_state['edit_user_data']
        st.info(f"Editing user: {user_data['name']}")
        with st.form("edit_user_form"):
            name = st.text_input("Name", value=user_data['name'])
            chinese_name = st.text_input("Chinese Name (中文名)", value=user_data.get('chinese_name', ''))
            age = st.number_input("Age", min_value=0, max_value=120, step=1, value=int(user_data['age']))
            birthday = st.date_input("Birthday", value=datetime.datetime.strptime(user_data['birthday'], '%Y-%m-%d').date() if user_data['birthday'] else datetime.date.today())
            skills_input = st.text_input("Skills (comma separated)", value=user_data['skills'].replace('`', '').replace('  ', ',') if user_data['skills'] else '')
            submitted = st.form_submit_button("Update User")
            if submitted and name:
                skills = ','.join([s.strip() for s in skills_input.split(',') if s.strip()]) if skills_input else ''
                update_user(conn, user_id, name, chinese_name, age, birthday.strftime('%Y-%m-%d'), skills)
                st.success(f"User '{name}' updated.")
                del st.session_state['edit_user_id']
                del st.session_state['edit_user_data']
                st.rerun()
        if st.button("Cancel Edit", key="cancel_edit"):
            del st.session_state['edit_user_id']
            del st.session_state['edit_user_data']
            st.rerun()
    if 'delete_user_id' in st.session_state:
        user_id = st.session_state['delete_user_id']
        st.warning("Are you sure you want to delete this user?")
        col1, col2 = st.columns(2)
        if col1.button("Yes, Delete", key="confirm_delete"):
            delete_user(conn, user_id)
            st.success("User deleted.")
            del st.session_state['delete_user_id']
            st.rerun()
        if col2.button("Cancel", key="cancel_delete"):
            del st.session_state['delete_user_id']
            st.rerun()
    conn.close()

def main():
    st.title("Demo App")
    db_path = os.path.join(os.path.dirname(__file__), "test_db.sqlite3")
    conn = get_db_connection(db_path)
    ensure_auth_table(conn)
    # --- Login/Register UI ---
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'login_username' not in st.session_state:
        st.session_state['login_username'] = ''
    if not st.session_state['logged_in']:
        login_tab, register_tab = st.tabs(["Login", "Register"])
        with login_tab:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pw")
            if st.button("Login"):
                if check_login(conn, login_username, login_password):
                    st.session_state['logged_in'] = True
                    st.session_state['login_username'] = login_username
                    st.success(f"Welcome, {login_username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with register_tab:
            st.subheader("Register")
            reg_username = st.text_input("New Username", key="reg_user")
            reg_password = st.text_input("New Password", type="password", key="reg_pw")
            reg_password2 = st.text_input("Confirm Password", type="password", key="reg_pw2")
            if st.button("Register"):
                if not reg_username or not reg_password:
                    st.error("Username and password required.")
                elif reg_password != reg_password2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(conn, reg_username, reg_password)
                    if ok:
                        st.success("Registration successful. Please login.")
                    else:
                        st.error(msg or "Registration failed.")
        conn.close()
        return
    # --- Logout button ---
    st.sidebar.write(f"Logged in as: {st.session_state['login_username']}")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['login_username'] = ''
        st.rerun()
    conn.close()
    # --- Main Tabs ---
    tab_names = [
        "Str Input Test", "Date Picker Test", "Slider Test", "Checkbox Test", "Radio Test",
        "Selectbox Test", "File Uploader Test", "Image Test", "Chart Test", "Markdown Test", "Calendar View", "Tree Structure Test", "Table Test", "Database Test"
    ]
    tabs = st.tabs(tab_names)
    tab_functions = [
        tab_str_input, tab_date_picker, tab_slider, tab_checkbox, tab_radio,
        tab_selectbox, tab_file_uploader, tab_image, tab_chart, tab_markdown,
        tab_calendar, tab_tree, tab_table, tab_database
    ]
    for i, tab_func in enumerate(tab_functions):
        with tabs[i]:
            tab_func()

if __name__ == "__main__":
    main()
