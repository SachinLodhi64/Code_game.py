import streamlit as st
import base64

# ============ SAMPLE DATABASE ============
users = {
    "user1": {"password": "pass1", "gameid": "GID001"},
    "user2": {"password": "pass2", "gameid": "GID002"}
}

tasks = [
    {"title": "MS Excel", "subtasks": [
        {"name": "Filter the Data", "dataset": "Demo_Client_Data_Filter_Excel.pdf", "guide": """Steps to Perform Filter Function in Excel:

1. Open Excel and paste the dataset into a worksheet.
2. Highlight the top row (headings).
3. Go to the 'Data' tab on the ribbon.
4. Click on 'Filter'.
5. Use dropdown to filter or sort.

Examples:
- Filter by PRD3344
- City contains 'Delhi'
- Sort by Order ID
        """},
        {"name": "Concatenate the Data", "dataset": "Concatenate_Excel_Practice_Dataset.pdf", "guide": """Steps to Perform Concatenation in Excel:

1. Open Excel and enter the data into columns A, B, and C.
2. In D2: =A2 & " " & B2 or =CONCATENATE(A2, " ", B2)
3. In E2: =A2 & " " & B2 & " from " & C2
4. Press Enter and drag down to copy.
        """},
        {"name": "Data Visualization", "dataset": "Data_Visualization_Dataset.pdf", "guide": """Steps to Create Charts in Excel:

✅ Pie Chart (Sales by Product)
- Select Product & Sales columns
- Insert → Pie Chart → Add labels/colors

✅ Bar Chart (Revenue by Region)
- Select Region & Revenue columns
- Insert → Bar Chart → Customize titles/legend

✅ Bubble Chart (Sales vs Revenue vs Rating)
- X = Sales, Y = Revenue, Size = Rating
- Insert → Scatter → Bubble Chart
        """}
    ]},
    {"title": "MS Advanced Excel", "subtasks": [
        {"name": "Using Macros", "dataset": None, "guide": """Steps to Perform Macros Task:

1. Enable Developer Tab in Excel.
2. Insert sample data into SalesData sheet.
3. Record a macro named HighlightHighSales.
4. Use VBA editor to add macro code.
5. Run the macro.
        """},
        {"name": "Prepare Advance Search Tool", "dataset": None, "guide": "Follow provided example and create a search tool in Excel."},
        {"name": "Prepare Dashboard to Add/Search/Delete Data", "dataset": None, "guide": "Design an Excel dashboard with data entry, search, and delete features."}
    ]},
    {"title": "MS Power BI", "subtasks": [
        {"name": "Prepare the Data Set in Query Set", "dataset": None, "guide": "Import and clean data in Power Query."},
        {"name": "Filter the Data", "dataset": None, "guide": "Apply filters in Power BI to refine visuals."},
        {"name": "Dashboard Making", "dataset": None, "guide": "Create a Power BI dashboard with charts and KPIs."}
    ]},
    {"title": "Coding", "subtasks": [
        {"name": "Java Code for Magical Number", "dataset": None, "guide": "Write a Java program to find magical numbers."},
        {"name": "C Code for Sorting Array", "dataset": None, "guide": "Implement sorting in C."},
        {"name": "Python Code for Calculator", "dataset": None, "guide": "Create a simple Python calculator."}
    ]},
    {"title": "Soft Skills", "subtasks": [
        {"name": "Prepare Your Introduction", "dataset": None, "guide": "Record and present your self-introduction."},
        {"name": "Interview", "dataset": None, "guide": "Simulate an interview session."},
        {"name": "Written Exercise", "dataset": None, "guide": "Write an essay or business email."}
    ]},
    {"title": "Digital Marketing", "subtasks": [
        {"name": "Prepare the SEO", "dataset": None, "guide": "Perform keyword research and optimization."},
        {"name": "Ad Run", "dataset": None, "guide": "Create and run a test ad."},
        {"name": "Design Post", "dataset": None, "guide": "Design a social media post."}
    ]}
]

group_tasks = [
    {"title": "Group Task", "subtasks": [{"name": "Prepare Dashboard for Data Set (Manager Review)", "dataset": None, "guide": "Prepare a comprehensive dashboard for manager review."}]},
    {"title": "Group Task", "subtasks": [{"name": "Prepare Python Taxation Tool with Bank Statement Reader", "dataset": None, "guide": "Develop a Python tool to read bank statements and calculate totals."}]},
    {"title": "Group Task", "subtasks": [{"name": "Prepare Excel ERP Dashboard for Data Set", "dataset": None, "guide": "Create an ERP dashboard in Excel for managing data."}]}
]

cross_task = {
    "title": "Cross-Team Task",
    "subtasks": [{"name": "Prepare the strategy for the product launch and propose it", "dataset": None, "guide": "Write a strategy document for launching a product."}]
}

# ============ SESSION STATE ============
if "username" not in st.session_state:
    st.session_state.username = None
if "login_days" not in st.session_state:
    st.session_state.login_days = {}
if "user_progress" not in st.session_state:
    st.session_state.user_progress = {}
if "user_rewards" not in st.session_state:
    st.session_state.user_rewards = {}
if "day_view" not in st.session_state:
    st.session_state.day_view = None

# ============ FUNCTIONS ============
def update_day(username):
    for i in range(10):
        if not st.session_state.user_progress[username][i]["done"]:
            st.session_state.login_days[username] = i + 1
            return
    st.session_state.login_days[username] = 10

def download_button(file_path, label):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}">{label}</a>'
        st.markdown(href, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Dataset not found.")

# ============ PAGES ============
def login():
    st.title("Corporate Simulation Game")
    uname = st.text_input("Username")
    gid = st.text_input("Game ID")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if uname in users and users[uname]['password'] == pwd and users[uname]['gameid'] == gid:
            st.session_state.username = uname
            st.session_state.login_days[uname] = 1
            st.session_state.user_rewards[uname] = 0
            st.session_state.user_progress[uname] = {i: {"sub": [False, False, False], "done": False} for i in range(10)}
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

def task_overview(username):
    st.header(f"Welcome {username}")
    update_day(username)
    st.write(f"**Day {st.session_state.login_days[username]} of 10**")
    st.write(f"**Rewards:** {st.session_state.user_rewards[username]} pts")

    cols = st.columns(4)
    for i in range(10):
        is_unlocked = i == 0 or st.session_state.user_progress[username][i - 1]["done"]
        task_text = (
            tasks[i]["title"] if i < 6 else
            group_tasks[i - 6]["title"] if i < 9 else
            cross_task["title"]
        )
        color = "✅" if st.session_state.user_progress[username][i]["done"] else ("🔓" if is_unlocked else "🔒")
        with cols[i % 4]:
            st.markdown(f"**Day {i+1}: {task_text} {color}**")
            if is_unlocked and not st.session_state.user_progress[username][i]["done"]:
                if st.button(f"Open Task {i+1}"):
                    st.session_state.day_view = i
                    st.experimental_rerun()

def task_detail(username, day):
    if day < 6:
        task = tasks[day]
    elif day < 9:
        task = group_tasks[day - 6]
    else:
        task = cross_task

    st.subheader(f"Day {day+1}: {task['title']}")

    for i, sub in enumerate(task["subtasks"]):
        status = "✔" if st.session_state.user_progress[username][day]["sub"][i] else "✖"
        st.markdown(f"**{sub['name']} {status}**")
        st.info(sub["guide"])
        if sub["dataset"]:
            download_button(sub["dataset"], "Download Dataset")
        uploaded = st.file_uploader(f"Upload file for: {sub['name']}", key=f"file_{i}")
        if st.button(f"Mark Complete: {sub['name']}", key=f"btn_{i}"):
            st.session_state.user_progress[username][day]["sub"][i] = True
            if all(st.session_state.user_progress[username][day]["sub"][:len(task["subtasks"])]):
                st.session_state.user_progress[username][day]["done"] = True
                st.session_state.user_rewards[username] += 50
                st.success(f"Completed Day {day+1}! Earned 50 points.")
                if day == 9:
                    st.balloons()
                    st.success("🎉 Game Over! You completed all 10 days.")
            st.experimental_rerun()

    if st.button("Back to Overview"):
        st.session_state.day_view = None
        st.experimental_rerun()

# ============ MAIN ============
if st.session_state.username is None:
    login()
else:
    if st.session_state.day_view is not None:
        task_detail(st.session_state.username, st.session_state.day_view)
    else:
        task_overview(st.session_state.username)
