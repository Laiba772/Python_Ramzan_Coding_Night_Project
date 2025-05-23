import streamlit as st
import math

# Set the page configuration
st.set_page_config(
    page_title="Advanced Calculator",  # Page title
    page_icon="📱",                    # Page icon
    layout="centered",                 # Layout style
    initial_sidebar_state="auto"       # Sidebar state
)

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            background-color: #f2f2f2;
        }
        .stSelectbox>div>div>input {
            background-color: #f2f2f2;
        }
        .stTitle {
            color: #FF4B4B;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Set page title and description
    st.title("Advanced Calculator")
    st.write("Enter two numbers and choose an operation")

    # Create two columns for number inputs
    col1, col2 = st.columns(2)

    # Input fields for numbers
    with col1:
        num1 = st.number_input("Enter first number", value=0.0)
    with col2:
        num2 = st.number_input("Enter second number", value=0.0)

    # Operation selection
    operation = st.selectbox(
        "Choose operation",
        ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)", 
         "Square Root (√)", "Exponentiation (^)","Modulus (%)", "Percentage (%)"],
    )

    # Calculate button with custom styling
    if st.button("Calculate"):
        try:
            if operation == "Addition (+)":
                result = num1 + num2
                symbol = "+"
            elif operation == "Subtraction (-)":
                result = num1 - num2
                symbol = "-"
            elif operation == "Multiplication (×)":
                result = num1 * num2
                symbol = "×"
            elif operation == "Division (÷)":
                if num2 == 0:
                    st.error("Error: Division by zero!")
                    return
                result = num1 / num2
                symbol = "÷"
            elif operation == "Square Root (√)":
                if num1 < 0:
                    st.error("Error: Cannot calculate the square root of a negative number!")
                    return
                result = math.sqrt(num1)
                symbol = "√"
            elif operation == "Exponentiation (^)":
                result = num1 ** num2
                symbol = "^"
            elif operation == "Modulus (%)":
                result = num1 % num2
                symbol = "%"
            elif operation == "Percentage (%)":
                result = (num1 / num2) * 100
                symbol = "%"

            # Display result with styling
            st.success(f"{num1} {symbol} {num2} = {result}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
