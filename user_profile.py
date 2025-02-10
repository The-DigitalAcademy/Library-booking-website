import streamlit as st

def show():
    st.title("User Profile")

    # Sample user data (replace with actual user session data)
    user_data = {
        "Name": "John Doe",
        "Email": "johndoe@example.com",
        "Membership": "Premium Member",
        "Borrowed Books": ["The Great Gatsby", "To Kill a Mockingbird"]
    }

    # Display profile icon at the top of the profile
    st.markdown('<h3><i class="fa fa-user-circle" style="font-size: 50px;"></i> Profile</h3>', unsafe_allow_html=True)

    # Display user details
    for key, value in user_data.items():
        st.write(f"**{key}:** {value}")

    # Add an edit icon (pen) next to the editable fields
    st.markdown('<h4><i class="fa fa-pencil" style="font-size: 20px; color: blue;"></i> Edit Profile</h4>', unsafe_allow_html=True)
    
    # Option to update password
    if st.button("Update Password"):
        st.write("Feature coming soon!")

if __name__ == "__main__":
    show()