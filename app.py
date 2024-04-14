import streamlit as st
import pandas as pd
from datetime import datetime
from db import *

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="🏨 Hotel Management System", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .stApp {
        background: 
            linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.60)),
            url("https://weblium.com/blog/wp-content/uploads/2019/09/photo-1533135091724-62cc5402aa20-1344x734.jpeg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background:
            linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.60)),
            url("https://weblium.com/blog/wp-content/uploads/2019/09/photo-1533135091724-62cc5402aa20-1344x734.jpeg") !important;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }
    /* Super slim, never-scroll Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(40,40,45,0.89), rgba(20,20,25,0.95));
        padding-top: 15px;
        color: #ffffff !important;
        backdrop-filter: blur(3px);
        border-right: 1px solid #4448;
        min-height: 100vh;
        width: 190px !important;
        max-width: 200px !important;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
    }
    /* Compact radio labels and pop on hover */
    section[data-testid="stSidebar"] label {
        color: #e0e5ec !important;
        font-size: 14px !important; /* was 16/17px, now smaller */
        padding: 5px 4px 5px 4px !important;
        border-radius: 6px;
        transition: 0.22s;
        margin-bottom: 1px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        min-height: 0;
        line-height: 1.2;
    }
    section[data-testid="stSidebar"] label:hover {
        background: #2ac4f833 !important;
        color: #fff !important;
        box-shadow: 0 2px 9px #2ac4f888;
        transform: scale(1.06);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 3px !important;
        padding-bottom: 3px !important;
    }
    /* Remove sidebar divider line (optional, makes it cleaner) */
    .css-1vq4p4l { display: none !important; }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
section[data-testid="stSidebar"] label {
    display: flex !important;
    align-items: center;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box;
    justify-content: flex-start;
    padding-left: 10px !important;
    padding-right: 10px !important;
}
section[data-testid="stSidebar"] span[data-testid="stRadioLabel"] {
    flex: 1 1 auto !important;
    width: 100% !important;
    text-align: left !important;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)
#gliched font css
st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #1f77b4;
    font-size: 10px;
    font-weight: bold;
    margin-bottom: 50px;
    position: relative;
    display: inline-block;
}
.section-title {
    color: #2ca02c;
    font-size: 10px;
    font-weight: bold;
    margin-top: 50px;
}

.glitch {
    position: relative;
    text-align: center;
    color: #1f77b4;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 30px;
    display: inline-block;
}
.glitch::before, .glitch::after {
    content: attr(data-text);
    position: absolute;
    left: 0; top: 0;
    width: 100%; height: 100%;
    opacity: 0.6;
    pointer-events: none;
}
.glitch::before {
    color: #f0f;
    z-index: 1;
    clip-path: polygon(0 2%,100% 0,98% 100%,0 100%);
    transform: translate(2px,0) skew(-2deg);
    opacity: 0.6;
    animation: glitchTop 1.1s infinite linear alternate-reverse;
}
.glitch::after {
    color: #0ff;
    z-index: 2;
    clip-path: polygon(2% 0,100% 0,100% 98%,0 100%);
    transform: translate(-2px,0) skew(2deg);
    opacity: 0.6;
    animation: glitchBot 0.9s infinite linear alternate-reverse;
}
@keyframes glitchTop {
    0% { transform: translate(1px, -1px) skew(-1deg);}
    15% { transform: translate(-3px, 2px) skew(-3deg);}
    34% { transform: translate(2px, 1px) skew(-1deg);}
    49% { transform: translate(-1px, -2px) skew(-2deg);}
    62% { transform: translate(2px, 1px) skew(1deg);}
    83% { transform: translate(-1px, 2px) skew(2deg);}
    100% { transform: translate(2px, -1px) skew(-1deg);}
}
@keyframes glitchBot {
    0% { transform: translate(-1px, 1px) skew(1deg);}
    13% { transform: translate(2px, -1px) skew(2deg);}
    34% { transform: translate(-2px, 1px) skew(3deg);}
    48% { transform: translate(1px, 2px) skew(1deg);}
    61% { transform: translate(-2px, -1px) skew(-3deg);}
    87% { transform: translate(2px, 1px) skew(1deg);}
    100% { transform: translate(-1px, 1px) skew(2deg);}
}
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None
# ==================== LOGIN PAGE ====================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glitch" data-text="🏨 Hotel Management System">🏨 Hotel Management System</div>', unsafe_allow_html=True)
        st.markdown("---")

        username = st.text_input("👤 Username", value="", key="login_user", placeholder="Enter username")
        password = st.text_input("🔐 Password", value="", type="password", key="login_pass", placeholder="Enter password")

        if st.button("🔓 Login", use_container_width=True):
            # Always fetch directly from session state!
            uname = st.session_state.get("login_user", "")
            pwd = st.session_state.get("login_pass", "")
            # Workaround: If browser autofill didn't register, try importing from local variables too (rarely helps, but can't hurt)
            if not uname: uname = username
            if not pwd: pwd = password

            if not uname or not pwd:
                st.error("❌ Please enter both username and password!")
            else:
                user = validate_user(uname, pwd)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = uname
                    st.success("✅ Login successful! Refreshing...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials! Default: admin/admin123")

        st.markdown("---")
        st.info("📌 Default Login: **admin** / **admin123**")

# ==================== MAIN APP ====================
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {st.session_state.username}!")
        st.markdown("---")

        menu = st.radio("📋 Menu", [
            "Dashboard",
            "Guests",
            "Rooms",
            "Bookings",
            "Payments",
            "Staff",
            "Service Request",
            "Amenity",
            "Travel Package",
            "Room Maintenance",
            "Review"
        ])

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    # ==================== DASHBOARD ====================
    if menu == "Dashboard":
        st.markdown('<div class="glitch" data-text="💻Dashboard">💻Dashboard</div>', unsafe_allow_html=True)
        try:
            guests = fetch_all_guests()
            rooms = fetch_all_rooms()
            bookings = fetch_all_bookings()
            payments = fetch_all_payments()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👥 Total Guests", len(guests))
            with col2:
                st.metric("🛏️ Total Rooms", len(rooms))
            with col3:
                st.metric("📅 Total Bookings", len(bookings))
            with col4:
                st.metric("💰 Total Payments", len(payments))

            st.markdown("---")

            # Recent Bookings
            st.subheader("📅 Recent Bookings")
            if bookings:
                df_bookings = pd.DataFrame(bookings, columns=["BookingID", "Guest Name", "Room", "Check-In", "Check-Out"])
                st.dataframe(df_bookings, use_container_width=True)
            else:
                st.info("No bookings found")

            import pandas as pd
            import datetime

            # Pie chart for occupancy (rooms)
            rooms = fetch_all_rooms()
            if rooms:
                total_rooms = len(rooms)
                occupied = sum(1 for r in rooms if str(r[4]) == "0")
                available = total_rooms - occupied
                occupancy_df = pd.DataFrame({
                    'Status': ['Occupied', 'Available'],
                    'Count': [occupied, available]
                })
                st.write("### Room Occupancy")
                st.plotly_chart({
                    "data": [{"type": "pie", "labels": occupancy_df['Status'], "values": occupancy_df['Count'], "hole": 0.3}],
                    "layout": {"height": 280}
                })

            # Bookings per month (line chart)
            bookings = fetch_all_bookings()
            if bookings:
                # Get month from checkin date
                df = pd.DataFrame(bookings, columns=["BookingID","Guest","Room","CheckIn","CheckOut"])
                df["CheckIn"] = pd.to_datetime(df["CheckIn"])
                bookings_by_month = df["CheckIn"].dt.month.value_counts().sort_index()
                st.write("### Bookings per Month")
                st.line_chart(bookings_by_month)

            # Revenue per month (bar chart)
            payments = fetch_all_payments()
            if payments:
                # Assume column 0=ID, 1=Guest, 2=Room, 3=Amount, 4=Method
                dfp = pd.DataFrame(payments, columns=["PaymentID","Guest","Room","Amount","Method"])
                # Let's assume PaymentID increments with month as a hack (real one needs payment date)
                dfp["Month"] = (dfp["PaymentID"] % 12) + 1
                revenue_by_month = dfp.groupby("Month")["Amount"].sum()
                st.write("### Revenue per Month")
                st.bar_chart(revenue_by_month)


        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")

    # ==================== GUESTS ====================
    elif menu == "Guests":
        st.markdown('<div class="glitch" data-text="👥 Guest Management">👥 Guest Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Guest", "📋 View Guests", "✏️ Update Guest", "🗑️ Delete Guest"])

        # Add Guest
        with tab1:
            st.subheader("Add New Guest")
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Guest Name", key="add_guest_name")
            with col2:
                email = st.text_input("Email", key="add_guest_email")
            with col3:
                phone = st.text_input("Phone", key="add_guest_phone")

            if st.button("➕ Add Guest", key="btn_add_guest", use_container_width=True):
                if not name or not email or not phone:
                    st.error("❌ All fields are required!")
                else:
                    success, message = insert_guest(name, email, phone)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

        # View Guests
        with tab2:
            st.subheader("All Guests")
            guests = fetch_all_guests()
            if guests:
                df = pd.DataFrame(guests, columns=["ID", "Name", "Email", "Phone"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No guests found")

        # Update Guest
        with tab3:
            st.subheader("Update Guest Information")
            guests = fetch_all_guests()
            if guests:
                guest_options = [(g[0], f"{g[0]} - {g[1]}") for g in guests]
                selected_guest = st.selectbox("Select Guest", guest_options, format_func=lambda x: x[1], key="update_guest")

                if selected_guest:
                    guest_id = selected_guest[0]
                    guest_data = [g for g in guests if g[0] == guest_id][0]

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        new_name = st.text_input("Name", value=guest_data[1], key="upd_guest_name")
                    with col2:
                        new_email = st.text_input("Email", value=guest_data[2], key="upd_guest_email")
                    with col3:
                        new_phone = st.text_input("Phone", value=guest_data[3], key="upd_guest_phone")

                    if st.button("✏️ Update Guest", key="btn_upd_guest", use_container_width=True):
                        success, message = update_guest(guest_id, new_name, new_email, new_phone)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            else:
                st.info("No guests to update")

        # Delete Guest
        with tab4:
            st.subheader("Delete Guest")
            guests = fetch_all_guests()
            if guests:
                guest_options = [(g[0], f"{g[0]} - {g[1]}") for g in guests]
                selected_guest = st.selectbox("Select Guest to Delete", guest_options, format_func=lambda x: x[1], key="del_guest")

                confirm = st.checkbox("I confirm deletion", key="conf_del_guest")
                if confirm:
                    if st.button("🗑️ Delete Guest", key="btn_del_guest", use_container_width=True):
                        success, message = delete_guest_by_id(selected_guest[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select guest and check confirmation box to enable delete button")
            else:
                st.info("No guests to delete")

    # ==================== ROOMS ====================
    elif menu == "Rooms":
        st.markdown('<div class="glitch" data-text="🛏️ Room Management">🛏️ Room Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Room", "📋 View Rooms", "✏️ Update Room", "🗑️ Delete Room"])

        # Add Room
        with tab1:
            st.subheader("Add New Room")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                room_number = st.text_input("Room Number", key="add_room_number")
            with col2:
                room_type = st.text_input("Room Type (Single/Double/Suite)", key="add_room_type")
            with col3:
                price = st.number_input("Price per Night", min_value=0.0, key="add_room_price")
            with col4:
                is_available = st.checkbox("Available", value=True, key="add_room_avail")

            if st.button("➕ Add Room", key="btn_add_room", use_container_width=True):
                if not room_number or not room_type:
                    st.error("❌ Room Number and Type are required!")
                else:
                    success, message = insert_room(room_number, room_type, price, is_available)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

        # View Rooms
        with tab2:
            st.subheader("All Rooms")
            rooms = fetch_all_rooms()
            if rooms:
                df = pd.DataFrame(rooms, columns=["ID", "Room Number", "Type", "Price", "Available"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No rooms found")

        # Update Room
        with tab3:
            st.subheader("Update Room")
            rooms = fetch_all_rooms()
            if rooms:
                room_options = [(r[0], f"{r[0]} - {r[1]}") for r in rooms]
                selected_room = st.selectbox("Select Room", room_options, format_func=lambda x: x[1], key="update_room")

                if selected_room:
                    room_id = selected_room[0]
                    room_data = [r for r in rooms if r[0] == room_id][0]

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        new_room_number = st.text_input("Room Number", value=room_data[1], key="upd_room_number")
                    with col2:
                        new_room_type = st.text_input("Type", value=room_data[2], key="upd_room_type")
                    with col3:
                        new_price = st.number_input("Price", value=float(room_data[3]), key="upd_room_price")
                    with col4:
                        new_available = st.checkbox("Available", value=bool(room_data[4]), key="upd_room_avail")

                    if st.button("✏️ Update Room", key="btn_upd_room", use_container_width=True):
                        success, message = update_room(room_id, new_room_number, new_room_type, new_price, new_available)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            else:
                st.info("No rooms to update")

        # Delete Room
        with tab4:
            st.subheader("Delete Room")
            rooms = fetch_all_rooms()
            if rooms:
                room_options = [(r[0], f"{r[0]} - {r[1]}") for r in rooms]
                selected_room = st.selectbox("Select Room to Delete", room_options, format_func=lambda x: x[1], key="del_room")

                confirm = st.checkbox("I confirm deletion", key="conf_del_room")
                if confirm:
                    if st.button("🗑️ Delete Room", key="btn_del_room", use_container_width=True):
                        success, message = delete_room(selected_room[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select room and check confirmation box to enable delete button")
            else:
                st.info("No rooms to delete")

    # ==================== BOOKINGS ====================
    elif menu == "Bookings":
        st.markdown('<div class="glitch" data-text="📅 Booking Management">📅 Booking Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Create Booking", "📋 View Bookings", "✏️ Update Booking", "❌ Delete Booking"])

        # Create Booking
        with tab1:
            st.subheader("Create New Booking")
            guests = get_guest_options()
            available_rooms = get_available_rooms()

            if guests and available_rooms:
                col1, col2 = st.columns(2)
                with col1:
                    guest_options = [(g[0], g[1]) for g in guests]
                    selected_guest = st.selectbox("Select Guest", guest_options, format_func=lambda x: x[1], key="book_guest")
                    guest_id = selected_guest[0]

                with col2:
                    room_options = [(r[0], r[1]) for r in available_rooms]
                    selected_room = st.selectbox("Select Available Room", room_options, format_func=lambda x: x[1], key="book_room")
                    room_id = selected_room[0]

                col3, col4 = st.columns(2)
                with col3:
                    checkin = st.date_input("Check-In Date", key="book_checkin")
                with col4:
                    checkout = st.date_input("Check-Out Date", key="book_checkout")

                if st.button("➕ Create Booking", key="btn_create_book", use_container_width=True):
                    if checkin >= checkout:
                        st.error("❌ Check-Out date must be after Check-In date!")
                    else:
                        success, message = insert_booking(guest_id, room_id, checkin, checkout)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Need at least one guest and one available room to create booking")

        # View Bookings
        with tab2:
            st.subheader("All Bookings")
            bookings = fetch_all_bookings()
            if bookings:
                df = pd.DataFrame(bookings, columns=["Booking ID", "Guest Name", "Room", "Check-In", "Check-Out"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No bookings found")

        # Update Booking
        with tab3:
            st.subheader("Update Booking")
            bookings = get_booking_options()
            if bookings:
                booking_options = [(b[0], f"Booking {b[0]} - {b[1]} - {b[2]}") for b in bookings]
                selected_booking = st.selectbox("Select Booking", booking_options, format_func=lambda x: x[1], key="upd_booking")

                booking_id = selected_booking[0]
                details = get_booking_price_details(booking_id)

                if details:
                    col1, col2 = st.columns(2)
                    with col1:
                        new_checkin = st.date_input("New Check-In", value=details[0], key="upd_book_checkin")
                    with col2:
                        new_checkout = st.date_input("New Check-Out", value=details[1], key="upd_book_checkout")

                    if st.button("✏️ Update Booking", key="btn_upd_book", use_container_width=True):
                        if new_checkin >= new_checkout:
                            st.error("❌ Check-Out must be after Check-In!")
                        else:
                            success, message = update_booking(booking_id, new_checkin, new_checkout)
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
            else:
                st.info("No bookings to update")

        # Delete Booking
        with tab4:
            st.subheader("Delete Booking")
            bookings = get_booking_options()
            if bookings:
                booking_options = [(b[0], f"Booking {b[0]} - {b[1]} - {b[2]}") for b in bookings]
                selected_booking = st.selectbox("Select Booking to Delete", booking_options, format_func=lambda x: x[1], key="del_booking")

                confirm = st.checkbox("I confirm deletion", key="conf_del_booking")
                if confirm:
                    if st.button("🗑️ Delete Booking", key="btn_del_booking", use_container_width=True):
                        success, message = delete_booking(selected_booking[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select booking and check confirmation box to enable delete button")
            else:
                st.info("No bookings to delete")

    # ==================== PAYMENTS ====================
    elif menu == "Payments":
        st.markdown('<div class="glitch" data-text="💰 Payment Management">💰 Payment Management</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["➕ Record Payment", "📋 View Payments"])

        # Record Payment
        with tab1:
            st.subheader("Record New Payment")
            bookings = get_booking_options()

            if bookings:
                booking_options = [(b[0], f"{b[0]} - {b[1]} - {b[2]}") for b in bookings]
                selected_booking = st.selectbox("Select Booking", booking_options, format_func=lambda x: x[1], key="pay_booking")

                booking_id = selected_booking[0]
                details = get_booking_price_details(booking_id)

                if details:
                    checkin, checkout, price = details
                    num_days = (checkout - checkin).days
                    total_amount = num_days * float(price)

                    st.info(f"💡 Booking Period: {num_days} days | Room Price: ₹{price}/night | Total: ₹{total_amount}")

                    col1, col2 = st.columns(2)
                    with col1:
                        amount = st.number_input("Payment Amount", min_value=0.0, value=float(total_amount), key="pay_amount")
                    with col2:
                        method = st.selectbox("Payment Method", ["Cash", "Card", "UPI", "Check"], key="pay_method")

                    if st.button("➕ Record Payment", key="btn_record_pay", use_container_width=True):
                        success, message = insert_payment(booking_id, amount, method)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            else:
                st.warning("⚠️ No bookings available")

        # View Payments
        with tab2:
            st.subheader("All Payments")
            payments = fetch_all_payments()
            if payments:
                df = pd.DataFrame(payments, columns=["Payment ID", "Guest Name", "Room", "Amount", "Method"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No payments found")

    # ==================== STAFF ====================
    elif menu == "Staff":
        st.markdown('<div class="glitch" data-text="👨‍💼 Staff Management">👨‍💼 Staff Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["➕ Add Staff", "📋 View Staff", "🗑️ Delete Staff"])

        # Add Staff
        with tab1:
            st.subheader("Add New Staff Member")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                name = st.text_input("Staff Name", key="add_staff_name")
            with col2:
                role = st.text_input("Role (Manager/Receptionist/etc)", key="add_staff_role")
            with col3:
                phone = st.text_input("Phone", key="add_staff_phone")
            with col4:
                email = st.text_input("Email", key="add_staff_email")

            if st.button("➕ Add Staff", key="btn_add_staff", use_container_width=True):
                if not name or not role:
                    st.error("❌ Name and Role are required!")
                else:
                    success, message = insert_staff(name, role, phone, email)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

        # View Staff
        with tab2:
            st.subheader("All Staff Members")
            staff = fetch_all_staff()
            if staff:
                df = pd.DataFrame(staff, columns=["ID", "Name", "Role", "Phone", "Email"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No staff found")

        # Delete Staff
        with tab3:
            st.subheader("Delete Staff Member")
            staff = fetch_all_staff()
            if staff:
                staff_options = [(s[0], f"{s[0]} - {s[1]}") for s in staff]
                selected_staff = st.selectbox("Select Staff to Delete", staff_options, format_func=lambda x: x[1], key="del_staff")

                confirm = st.checkbox("I confirm deletion", key="conf_del_staff")
                if confirm:
                    if st.button("🗑️ Delete Staff", key="btn_del_staff", use_container_width=True):
                        success, message = delete_staff(selected_staff[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select staff and check confirmation box to enable delete button")
            else:
                st.info("No staff to delete")

    # ==================== SERVICE REQUEST ====================
    elif menu == "Service Request":
        st.markdown('<div class="glitch" data-text="🔧 Service Request Management">🔧 Service Request Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["➕ Create Request", "📋 View Requests", "🗑️ Delete Request"])

        # Create Request
        with tab1:
            st.subheader("Create Service Request")
            guests = get_guest_options()
            rooms = get_room_options()

            if guests and rooms:
                col1, col2, col3 = st.columns(3)
                with col1:
                    guest_options = [(g[0], g[1]) for g in guests]
                    selected_guest = st.selectbox("Select Guest", guest_options, format_func=lambda x: x[1], key="sr_guest")
                    guest_id = selected_guest[0]

                with col2:
                    room_options = [(r[0], r[1]) for r in rooms]
                    selected_room = st.selectbox("Select Room", room_options, format_func=lambda x: x[1], key="sr_room")
                    room_id = selected_room[0]

                with col3:
                    service_type = st.selectbox("Service Type", ["Housekeeping", "Maintenance", "Room Service", "Laundry", "Other"], key="sr_type")

                if st.button("➕ Create Request", key="btn_create_sr", use_container_width=True):
                    success, message = insert_service_request(guest_id, room_id, service_type)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Need at least one guest and one room")

        # View Requests
        with tab2:
            st.subheader("All Service Requests")
            requests = fetch_all_service_requests()
            if requests:
                df = pd.DataFrame(requests, columns=["ID", "Guest", "Room", "Service Type", "Status", "Time"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No service requests found")

        # Delete Request
        with tab3:
            st.subheader("Delete Service Request")
            requests = fetch_all_service_requests()
            if requests:
                request_options = [(r[0], f"Request {r[0]} - {r[1]} - {r[3]}") for r in requests]
                selected_request = st.selectbox("Select Request to Delete", request_options, format_func=lambda x: x[1], key="del_sr")

                confirm = st.checkbox("I confirm deletion", key="conf_del_sr")
                if confirm:
                    if st.button("🗑️ Delete Request", key="btn_del_sr", use_container_width=True):
                        success, message = delete_service_request(selected_request[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select request and check confirmation box to enable delete button")
            else:
                st.info("No requests to delete")

    # ==================== AMENITY ====================
    elif menu == "Amenity":
        st.markdown('<div class="glitch" data-text="🏊 Amenity Management">🏊 Amenity Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Amenity", "📋 View Amenities", "🔗 Assign to Room", "🗑️ Delete Amenity"])

        # Add Amenity
        with tab1:
            st.subheader("Add New Amenity")
            amenity_name = st.text_input("Amenity Name (Pool/WiFi/Gym/etc)", key="add_amenity_name")

            if st.button("➕ Add Amenity", key="btn_add_amenity", use_container_width=True):
                if not amenity_name:
                    st.error("❌ Amenity name is required!")
                else:
                    success, message = insert_amenity(amenity_name)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

        # View Amenities
        with tab2:
            st.subheader("All Amenities")
            amenities = fetch_all_amenities()
            if amenities:
                df = pd.DataFrame(amenities, columns=["ID", "Name"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No amenities found")

        # Assign to Room
        with tab3:
            st.subheader("Assign Amenity to Room")
            rooms = get_room_options()
            amenities = fetch_all_amenities()

            if rooms and amenities:
                col1, col2 = st.columns(2)
                with col1:
                    room_options = [(r[0], r[1]) for r in rooms]
                    selected_room = st.selectbox("Select Room", room_options, format_func=lambda x: x[1], key="assign_room")
                    room_id = selected_room[0]

                with col2:
                    amenity_options = [(a[0], a[1]) for a in amenities]
                    selected_amenity = st.selectbox("Select Amenity", amenity_options, format_func=lambda x: x[1], key="assign_amenity")
                    amenity_id = selected_amenity[0]

                if st.button("🔗 Assign Amenity", key="btn_assign_amenity", use_container_width=True):
                    success, message = assign_amenity_to_room(room_id, amenity_id)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

                st.markdown("---")
                st.subheader("Room-Amenity Mappings")
                mappings = fetch_room_amenities()
                if mappings:
                    df = pd.DataFrame(mappings, columns=["Room Number", "Amenity Name"])
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ Need at least one room and one amenity")

        # Delete Amenity
        with tab4:
            st.subheader("Delete Amenity")
            amenities = fetch_all_amenities()
            if amenities:
                amenity_options = [(a[0], a[1]) for a in amenities]
                selected_amenity = st.selectbox("Select Amenity to Delete", amenity_options, format_func=lambda x: x[1], key="del_amenity")

                confirm = st.checkbox("I confirm deletion", key="conf_del_amenity")
                if confirm:
                    if st.button("🗑️ Delete Amenity", key="btn_del_amenity", use_container_width=True):
                        success, message = delete_amenity(selected_amenity[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select amenity and check confirmation box to enable delete button")
            else:
                st.info("No amenities to delete")

    # ==================== TRAVEL PACKAGE ====================
    elif menu == "Travel Package":
        st.markdown('<div class="glitch" data-text="✈️ Travel Package Management">✈️ Travel Package Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["➕ Add Package", "📋 View Packages", "🗑️ Delete Package"])

        # Add Package
        with tab1:
            st.subheader("Add Travel Package")
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Package Title", key="add_pkg_title")
                description = st.text_area("Description", key="add_pkg_desc", height=100)
            with col2:
                price = st.number_input("Price", min_value=0.0, key="add_pkg_price")
                duration = st.number_input("Duration (Days)", min_value=1, key="add_pkg_duration", step=1)

            if st.button("➕ Add Package", key="btn_add_pkg", use_container_width=True):
                if not title or not description:
                    st.error("❌ Title and Description are required!")
                else:
                    success, message = insert_travel_package(title, description, price, int(duration))
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

        # View Packages
        with tab2:
            st.subheader("All Packages")
            packages = fetch_all_travel_packages()
            if packages:
                for pkg in packages:
                    with st.expander(f"📦 {pkg[1]} - ₹{pkg[3]} - {pkg[4]} days"):
                        st.write(f"**Description:** {pkg[2]}")
                        st.write(f"**Price:** ₹{pkg[3]}")
                        st.write(f"**Duration:** {pkg[4]} days")
            else:
                st.info("No travel packages found")

        # Delete Package
        with tab3:
            st.subheader("Delete Package")
            packages = fetch_all_travel_packages()
            if packages:
                pkg_options = [(p[0], f"{p[0]} - {p[1]}") for p in packages]
                selected_pkg = st.selectbox("Select Package to Delete", pkg_options, format_func=lambda x: x[1], key="del_pkg")

                confirm = st.checkbox("I confirm deletion", key="conf_del_pkg")
                if confirm:
                    if st.button("🗑️ Delete Package", key="btn_del_pkg", use_container_width=True):
                        success, message = delete_travel_package(selected_pkg[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select package and check confirmation box to enable delete button")
            else:
                st.info("No packages to delete")

    # ==================== ROOM MAINTENANCE ====================
    elif menu == "Room Maintenance":
        st.markdown('<div class="glitch" data-text="🔧 Room Maintenance">🔧 Room Maintenance</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["➕ Log Issue", "📋 View Logs", "🗑️ Delete Log"])

        # Log Issue
        with tab1:
            st.subheader("Log Maintenance Issue")
            rooms = get_room_options()

            if rooms:
                room_options = [(r[0], r[1]) for r in rooms]
                selected_room = st.selectbox("Select Room", room_options, format_func=lambda x: x[1], key="maint_room")
                room_id = selected_room[0]

                issue = st.text_area("Issue Description", key="maint_issue", height=100)
                reported_date = st.date_input("Reported Date", key="maint_date")

                if st.button("➕ Log Issue", key="btn_log_maint", use_container_width=True):
                    if not issue:
                        st.error("❌ Issue description is required!")
                    else:
                        success, message = insert_maintenance_log(room_id, issue, reported_date)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            else:
                st.warning("⚠️ No rooms available")

        # View Logs
        with tab2:
            st.subheader("Maintenance Logs")
            logs = fetch_maintenance_logs()
            if logs:
                df = pd.DataFrame(logs, columns=["ID", "Room", "Issue", "Date", "Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No maintenance logs found")

        # Delete Log
        with tab3:
            st.subheader("Delete Maintenance Log")
            logs = fetch_maintenance_logs()
            if logs:
                log_options = [(l[0], f"ID {l[0]} - {l[1]} - {l[3]}") for l in logs]
                selected_log = st.selectbox("Select Log to Delete", log_options, format_func=lambda x: x[1], key="del_maint")

                confirm = st.checkbox("I confirm deletion", key="conf_del_maint")
                if confirm:
                    if st.button("🗑️ Delete Log", key="btn_del_maint", use_container_width=True):
                        success, message = delete_maintenance_log(selected_log[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select log and check confirmation box to enable delete button")
            else:
                st.info("No logs to delete")

    # ==================== REVIEW ====================
    elif menu == "Review":
        st.markdown('<div class="glitch" data-text="⭐ Review Management">⭐ Review Management</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["➕ Add Review", "📋 View Reviews", "🗑️ Delete Review"])

        # Add Review
        with tab1:
            st.subheader("Add New Review")
            guests = get_guest_options()
            rooms = get_room_options()

            if guests and rooms:
                col1, col2 = st.columns(2)
                with col1:
                    guest_options = [(g[0], g[1]) for g in guests]
                    selected_guest = st.selectbox("Select Guest", guest_options, format_func=lambda x: x[1], key="rev_guest")
                    guest_id = selected_guest[0]

                with col2:
                    room_options = [(r[0], r[1]) for r in rooms]
                    selected_room = st.selectbox("Select Room", room_options, format_func=lambda x: x[1], key="rev_room")
                    room_id = selected_room[0]

                rating = st.slider("Rating", 1, 5, 5, key="rev_rating")
                comment = st.text_area("Comment", key="rev_comment", height=100)
                review_date = st.date_input("Review Date", key="rev_date")

                if st.button("➕ Add Review", key="btn_add_rev", use_container_width=True):
                    if not comment:
                        st.error("❌ Comment is required!")
                    else:
                        success, message = insert_review(guest_id, room_id, rating, comment, review_date)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Need at least one guest and one room")

        # View Reviews
        with tab2:
            st.subheader("All Reviews")
            reviews = fetch_all_reviews()
            if reviews:
                df = pd.DataFrame(reviews, columns=["ID", "Guest", "Room", "Rating", "Comment", "Date"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No reviews found")

        # Delete Review
        with tab3:
            st.subheader("Delete Review")
            reviews = fetch_all_reviews()
            if reviews:
                review_options = [(r[0], f"Review {r[0]} - {r[1]} - {r[2]}") for r in reviews]
                selected_review = st.selectbox("Select Review to Delete", review_options, format_func=lambda x: x[1], key="del_rev")

                confirm = st.checkbox("I confirm deletion", key="conf_del_rev")
                if confirm:
                    if st.button("🗑️ Delete Review", key="btn_del_rev", use_container_width=True):
                        success, message = delete_review(selected_review[0])
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.info("✓ Select review and check confirmation box to enable delete button")
            else:
                st.info("No reviews to delete")
