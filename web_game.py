import streamlit as st
import random

st.set_page_config(
    page_title="GUESS",
    page_icon="🎯",
    layout="centered"
)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "game_started": False,
    "game_over": False,
    "pass_screen": False,
    "tries": 0,
    "history": [],
    "player1_score": 0,
    "player2_score": 0,
    "player1_name": "Player 1",
    "player2_name": "Player 2",
    "best_score": None,
    "hint_used": False,
    "hint_text": "",
    "match_type": "Single Round",
    "match_over": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# FUNCTIONS
# ==========================================

def reset_round():
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.pass_screen = False
    st.session_state.tries = 0
    st.session_state.history = []
    st.session_state.hint_used = False
    st.session_state.hint_text = ""


def reset_match():
    reset_round()
    st.session_state.player1_score = 0
    st.session_state.player2_score = 0
    st.session_state.match_over = False


def wins_needed():
    if st.session_state.match_type == "Best of 3":
        return 2

    elif st.session_state.match_type == "Best of 5":
        return 3

    return 1


def check_match_winner():
    needed = wins_needed()

    if st.session_state.player1_score >= needed:
        st.session_state.match_over = True
        return st.session_state.player1_name

    if st.session_state.player2_score >= needed:
        st.session_state.match_over = True
        return st.session_state.player2_name

    return None


# ==========================================
# DARK MODE
# ==========================================

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */

    .stApp {
        background:
            radial-gradient(
                circle at top,
                #1c1c24 0%,
                #0e0e12 45%,
                #070709 100%
            );
        color: #f5f5f5;
    }


    /* NORMAL TEXT */

    h1, h2, h3, h4, h5, p, label {
        color: #f5f5f5 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #b8b8c0 !important;
    }


    /* RADIO BUTTON TEXT */

    div[role="radiogroup"] label {
        color: white !important;
    }


    /* =====================================
       INPUT BOXES
       ===================================== */

    div[data-baseweb="input"] > div {
        background-color: #f1f1f1 !important;
        border: 1px solid #777777 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] input {
        background-color: #f1f1f1 !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        caret-color: #000000 !important;

        font-weight: 600 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #555555 !important;

        -webkit-text-fill-color: #555555 !important;

        opacity: 1 !important;
    }


    /* PASSWORD INPUT */

    input[type="password"] {
        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        caret-color: #000000 !important;
    }


    /* PASSWORD EYE ICON */

    div[data-baseweb="input"] svg {
        fill: #333333 !important;
        color: #333333 !important;
    }


    /* =====================================
       BUTTONS
       ===================================== */

    .stButton > button {
        background-color: #3a3a42 !important;

        color: white !important;

        border: 1px solid #55555f !important;

        border-radius: 12px !important;

        font-weight: 700 !important;

        min-height: 45px;
    }

    .stButton > button p {
        color: white !important;
    }

    .stButton > button:hover {
        background-color: #4a4a54 !important;

        color: white !important;

        border-color: #70707c !important;
    }

    .stButton > button:active {
        background-color: #2f2f36 !important;

        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# TITLE
# ==========================================

st.markdown(
    """
    <h1 style="
        text-align:center;
        color:white !important;
        font-size:60px;
        font-weight:800;
        margin-bottom:30px;
    ">
        🎯 GUESS
    </h1>
    """,
    unsafe_allow_html=True
)


# ==========================================
# START SCREEN
# ==========================================

if (
    not st.session_state.game_started
    and not st.session_state.pass_screen
):

    # --------------------------------------
    # DIFFICULTY
    # --------------------------------------

    st.subheader("🎚️ Difficulty")

    difficulty = st.radio(
        "Choose difficulty:",
        ["Easy", "Medium", "Hard"],
        horizontal=True
    )

    if difficulty == "Easy":
        max_number = 100
        max_tries = 10

    elif difficulty == "Medium":
        max_number = 1000
        max_tries = 12

    else:
        max_number = 10000
        max_tries = 16


    # --------------------------------------
    # RANGE + ATTEMPTS
    # --------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔢 Number Range")
        st.write(f"**1 - {max_number}**")

    with col2:
        st.markdown("#### ❤️ Attempts")
        st.write(f"**{max_tries}**")

    st.write("")


    # --------------------------------------
    # GAME MODE
    # --------------------------------------

    st.subheader("🎮 Game Mode")

    mode = st.radio(
        "Choose game mode:",
        [
            "👥 Player vs Player",
            "🤖 Player vs Computer"
        ],
        horizontal=True
    )


    # --------------------------------------
    # MATCH TYPE
    # --------------------------------------

    st.subheader("⚔️ Match Type")

    match_type = st.radio(
        "Choose how many rounds to play:",
        [
            "Single Round",
            "Best of 3",
            "Best of 5"
        ],
        horizontal=True
    )

    st.session_state.match_type = match_type

    if match_type == "Single Round":

        st.caption(
            "🏆 Win 1 round to win the match."
        )

    elif match_type == "Best of 3":

        st.caption(
            "🏆 First player to win 2 rounds wins the match."
        )

    else:

        st.caption(
            "🏆 First player to win 3 rounds wins the match."
        )


    # ======================================
    # PLAYER VS PLAYER
    # ======================================

    if mode == "👥 Player vs Player":

        st.subheader("👤 Players")

        player1_name = st.text_input(
            "Player 1 name:",
            value=st.session_state.player1_name
        )

        player2_name = st.text_input(
            "Player 2 name:",
            value=st.session_state.player2_name
        )

        secret_text = st.text_input(
            f"{player1_name}, enter a secret number "
            f"from 1 to {max_number}:",
            type="password"
        )

        start_button = st.button(
            "🔒 Lock Number",
            use_container_width=True
        )

        if start_button:

            try:

                secret_number = int(secret_text)

                if 1 <= secret_number <= max_number:

                    st.session_state.player1_name = (
                        player1_name.strip()
                        if player1_name.strip()
                        else "Player 1"
                    )

                    st.session_state.player2_name = (
                        player2_name.strip()
                        if player2_name.strip()
                        else "Player 2"
                    )

                    st.session_state.secret = secret_number

                    st.session_state.max_number = max_number

                    st.session_state.max_tries = max_tries

                    st.session_state.difficulty = difficulty

                    st.session_state.mode = mode

                    st.session_state.tries = 0

                    st.session_state.history = []

                    st.session_state.hint_used = False

                    st.session_state.hint_text = ""

                    st.session_state.game_over = False

                    st.session_state.pass_screen = True

                    st.rerun()

                else:

                    st.error(
                        f"Enter a number from 1 to {max_number}!"
                    )

            except ValueError:

                st.error(
                    "Please enter a valid number!"
                )


    # ======================================
    # PLAYER VS COMPUTER
    # ======================================

    else:

        st.subheader("👤 Player")

        player_name = st.text_input(
            "Your name:",
            value=st.session_state.player2_name
        )

        st.info(
            f"🤖 Computer will secretly choose "
            f"a number from 1 to {max_number}."
        )

        start_button = st.button(
            "▶️ Start Game",
            use_container_width=True
        )

        if start_button:

            st.session_state.player2_name = (
                player_name.strip()
                if player_name.strip()
                else "Player"
            )

            st.session_state.player1_name = "Computer"

            st.session_state.secret = random.randint(
                1,
                max_number
            )

            st.session_state.max_number = max_number

            st.session_state.max_tries = max_tries

            st.session_state.difficulty = difficulty

            st.session_state.mode = mode

            st.session_state.tries = 0

            st.session_state.history = []

            st.session_state.hint_used = False

            st.session_state.hint_text = ""

            st.session_state.game_over = False

            st.session_state.game_started = True

            st.rerun()


# ==========================================
# PASS DEVICE SCREEN
# ==========================================

if (
    st.session_state.pass_screen
    and not st.session_state.game_started
):

    player2 = st.session_state.player2_name

    st.markdown(
        "<h1 style='text-align:center;'>🔐</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center;'>NUMBER LOCKED</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <p style="
            text-align:center;
            font-size:22px;
            font-weight:bold;
            margin-top:25px;
        ">
            {player2}, your mission starts now. 🎯
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            font-size:17px;
            color:#bdbdc6 !important;
        ">
            Find the secret number before you run out of chances.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    ready_button = st.button(
        "🎮 START GUESSING",
        use_container_width=True
    )

    if ready_button:

        st.session_state.pass_screen = False

        st.session_state.game_started = True

        st.rerun()


# ==========================================
# ACTIVE GAME
# ==========================================

if st.session_state.game_started:

    max_number = st.session_state.max_number

    max_tries = st.session_state.max_tries

    player1 = st.session_state.player1_name

    player2 = st.session_state.player2_name

    attempts_left = (
        max_tries - st.session_state.tries
    )


    # --------------------------------------
    # GAME INFO
    # --------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            "##### 🎚️ Difficulty"
        )

        st.write(
            f"**{st.session_state.difficulty}**"
        )

    with col2:

        st.markdown(
            "##### ❤️ Attempts"
        )

        st.write(
            f"**{attempts_left}**"
        )

    with col3:

        st.markdown(
            "##### 🥇 Best"
        )

        if st.session_state.best_score is None:

            st.write("**—**")

        else:

            st.write(
                f"**{st.session_state.best_score}**"
            )


    # --------------------------------------
    # MATCH
    # --------------------------------------

    st.subheader(
        f"⚔️ {st.session_state.match_type}"
    )

    needed = wins_needed()

    if st.session_state.match_type != "Single Round":

        st.caption(
            f"🏆 First to {needed} round wins."
        )


    # --------------------------------------
    # SCORE
    # --------------------------------------

    st.subheader("🏆 Score")

    score1, score2 = st.columns(2)

    with score1:

        st.markdown(
            f"### {player1}"
        )

        st.write(
            f"**{st.session_state.player1_score}**"
        )

    with score2:

        st.markdown(
            f"### {player2}"
        )

        st.write(
            f"**{st.session_state.player2_score}**"
        )


    st.caption(
        f"🔢 Number range: 1 - {max_number}"
    )


    # ======================================
    # GUESSING
    # ======================================

    if not st.session_state.game_over:

        st.subheader(
            f"🎯 {player2}'s Turn"
        )

        guess_text = st.text_input(
            f"Enter your guess (1 - {max_number}):",
            key="guess_input"
        )

        button1, button2 = st.columns(2)

        with button1:

            check_button = st.button(
                "🎯 Check Guess",
                use_container_width=True
            )

        with button2:

            hint_button = st.button(
                "💡 Hint",
                use_container_width=True,
                disabled=st.session_state.hint_used
            )


        # ----------------------------------
        # HINT
        # ----------------------------------

        if hint_button:

            st.session_state.hint_used = True

            if st.session_state.secret % 2 == 0:

                st.session_state.hint_text = (
                    "💡 The secret number is EVEN."
                )

            else:

                st.session_state.hint_text = (
                    "💡 The secret number is ODD."
                )


        if st.session_state.hint_used:

            st.info(
                st.session_state.hint_text
            )

            st.caption(
                "One hint is allowed per round."
            )


        # ----------------------------------
        # CHECK GUESS
        # ----------------------------------

        if check_button:

            try:

                guess = int(guess_text)

                if 1 <= guess <= max_number:

                    st.session_state.tries += 1

                    st.session_state.history.append(
                        guess
                    )

                    difference = abs(
                        guess -
                        st.session_state.secret
                    )


                    # CORRECT GUESS

                    if guess == st.session_state.secret:

                        st.session_state.player2_score += 1

                        st.session_state.game_over = True

                        if (
                            st.session_state.best_score is None
                            or
                            st.session_state.tries
                            < st.session_state.best_score
                        ):

                            st.session_state.best_score = (
                                st.session_state.tries
                            )

                        st.success(
                            f"🏆 {player2} wins the round!"
                        )


                    # WRONG GUESS

                    else:

                        if guess > st.session_state.secret:

                            st.warning(
                                "⬇️ Too high!"
                            )

                        else:

                            st.warning(
                                "⬆️ Too low!"
                            )


                        percentage = (
                            difference / max_number
                        )

                        if percentage <= 0.02:

                            st.success(
                                "🔥 Very Close!"
                            )

                        elif percentage <= 0.10:

                            st.info(
                                "🟡 Close!"
                            )

                        else:

                            st.info(
                                "❄️ Far Away!"
                            )


                        # OUT OF ATTEMPTS

                        if (
                            st.session_state.tries
                            >= max_tries
                        ):

                            st.session_state.player1_score += 1

                            st.session_state.game_over = True

                            if (
                                st.session_state.mode
                                == "👥 Player vs Player"
                            ):

                                st.error(
                                    f"🏆 {player1} wins the round!"
                                )

                            else:

                                st.error(
                                    "🤖 Computer wins the round!"
                                )

                else:

                    st.error(
                        f"Enter a number from "
                        f"1 to {max_number}!"
                    )

            except ValueError:

                st.error(
                    "Please enter a valid number!"
                )


    # ======================================
    # GUESS HISTORY
    # ======================================

    if st.session_state.history:

        st.subheader(
            "📜 Guess History"
        )

        history_text = " → ".join(
            str(number)
            for number in st.session_state.history
        )

        st.write(
            history_text
        )


    # ======================================
    # ROUND / MATCH OVER
    # ======================================

    if st.session_state.game_over:

        match_winner = check_match_winner()

        st.divider()

        st.write(
            f"🔐 Secret number: "
            f"**{st.session_state.secret}**"
        )

        st.write(
            f"🎯 Guesses used: "
            f"**{st.session_state.tries}**"
        )


        # MATCH WINNER

        if match_winner:

            st.success(
                f"🏆 {match_winner} WINS THE MATCH!"
            )

            st.markdown(
                f"""
                <h2 style="
                    text-align:center;
                    margin-top:25px;
                ">
                    🏆 {match_winner}
                </h2>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <p style="
                    text-align:center;
                    font-size:20px;
                ">
                    Match Champion
                </p>
                """,
                unsafe_allow_html=True
            )

            new_match_button = st.button(
                "🔄 New Match",
                use_container_width=True
            )

            if new_match_button:

                reset_match()

                st.rerun()


        # NEXT ROUND

        else:

            st.info(
                f"⚔️ Match continues — "
                f"first to {needed} wins!"
            )

            next_round_button = st.button(
                "➡️ Next Round",
                use_container_width=True
            )

            if next_round_button:

                reset_round()

                st.rerun()


# ==========================================
# BOTTOM TEXT
# ==========================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:70px;
        margin-bottom:20px;
        font-size:20px;
        font-weight:bold;
        color:white;
    ">
        Think. Guess. Win. 🔥
    </div>
    """,
    unsafe_allow_html=True
)