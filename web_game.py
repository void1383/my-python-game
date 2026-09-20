import streamlit as st

st.title("Guess")

# -------------------------
# PLAYER 1
# -------------------------

if "secret" not in st.session_state:

    secret_text = st.text_input(
        "Player 1, enter a secret number from 1 to 1000:",
        type="password"
    )

    start_button = st.button("Start Game")

    if start_button:

        if secret_text:

            try:
                secret_number = int(secret_text)

                if 1 <= secret_number <= 1000:
                    st.session_state.secret = secret_number
                    st.session_state.tries = 0
                    st.rerun()

                else:
                    st.error("Please enter a number from 1 to 1000!")

            except ValueError:
                st.error("Please enter a valid number!")

        else:
            st.warning("Player 1, enter a number first!")


# -------------------------
# PLAYER 2
# -------------------------

if "secret" in st.session_state:

    st.success("Game started! Player 2, start guessing.")

    guess_text = st.text_input(
        "Player 2, enter your guess:"
    )

    guess_button = st.button("Check Guess")

    if guess_button:

        if guess_text:

            try:
                guess = int(guess_text)

                if 1 <= guess <= 1000:

                    st.session_state.tries += 1

                    if guess == st.session_state.secret:
                        st.success("Player 2 won! 🎉")

                    elif guess > st.session_state.secret:
                        st.warning("Your guess is too high!")

                    else:
                        st.warning("Your guess is too low!")

                    if (
                        st.session_state.tries >= 10
                        and guess != st.session_state.secret
                    ):
                        st.success("Player 1 won! 🎉")

                else:
                    st.error("Please enter a number from 1 to 1000!")

            except ValueError:
                st.error("Please enter a valid number!")

        else:
            st.warning("Enter your guess first!")

    st.write("Tries:", st.session_state.tries, "/ 10")

    # -------------------------
    # NEW GAME
    # -------------------------

    new_button = st.button("New Game")

    if new_button:
        del st.session_state.secret
        st.session_state.tries = 0
        st.rerun()