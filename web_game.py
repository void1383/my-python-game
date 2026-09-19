import streamlit as st

st.title("guess")

secret_text = st.text_input("Player 1, enter a secret number from 1 to 100:")
start_button = st.button("Start Game")

if start_button:
    st.session_state.secret = int(secret_text)
    st.session_state.tries = 0
    st.success("Game started!")

if "secret" in st.session_state:
    guess_text = st.text_input("Player 2, enter your guess:")
    guess = int(guess_text) if guess_text else 0
    guess_button = st.button("Check Guess")
    if guess_button:
        st.session_state.tries += 1
        if guess == st.session_state.secret:
            st.success("player 2 won!")

        elif guess > st.session_state.secret:
            st.warning("Your guess is too high!")
        else:
            st.warning("Your guess is too low!")
        if st.session_state.tries >= 10 and guess != st.session_state.secret:
                st.success("Player 1, you won!")
        new_button = st.button("New Game")
        if new_button:
            del st.session_state.secret
            st.session_state.tries = 0
            st.rerun()