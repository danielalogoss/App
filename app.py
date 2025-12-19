import base64
from pathlib import Path

import streamlit as st

# ------------------ Page config (MUST be first Streamlit call) ------------------
st.set_page_config(
    page_title="Multi-Cat Care Planner",
    page_icon="🐾",
    layout="wide",
)

# ------------------ Helpers ------------------
def load_css():
    css_path = Path(__file__).parent / "styles.css"
    if not css_path.exists():
        st.error(f"styles.css not found at: {css_path}")
        st.stop()
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def set_background(image_rel_path: str):
    """
    Cloud-proof background loader. Path is resolved relative to this file.
    If missing, the app continues without crashing.
    """
    image_path = Path(__file__).parent / image_rel_path
    if not image_path.exists():
        st.warning(f"Background image not found: {image_path} (running without it)")
        return

    img_bytes = image_path.read_bytes()
    ext = image_path.suffix.lower().replace(".", "")
    mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
    encoded = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/{mime};base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------ Load styling ------------------
load_css()

# IMPORTANT: match your repo folder name exactly.
# If your folder is named "Assets" (capital A), keep this:
set_background("Assets/background6.jpg")
# If you rename the folder to lowercase "assets", change to:
# set_background("assets/background6.jpg")


# ------------------ State init ------------------
if "cats" not in st.session_state:
    st.session_state.cats = []  # [{"name":..., "type":..., "age":..., "notes":...}]
if "page" not in st.session_state:
    st.session_state.page = "Home"  # Home / FAQ's / Feral care / AddCat / <cat name>


# ------------------ Sidebar (Home + Cats + Feral care + FAQ's) ------------------
st.sidebar.header("🐱 Your Planner")

cat_pages = [c["name"] for c in st.session_state.cats]
nav_options = ["Home"] + cat_pages + ["Feral care", "FAQ's"]

# If on AddCat (not in sidebar), keep sidebar showing Home
sidebar_current = st.session_state.page if st.session_state.page in nav_options else "Home"

sidebar_choice = st.sidebar.radio(
    "Go to",
    nav_options,
    index=nav_options.index(sidebar_current),
    key="sidebar_nav",
)

# Only let the sidebar overwrite page if we're currently on a sidebar page
if st.session_state.page in nav_options:
    st.session_state.page = sidebar_choice

st.sidebar.divider()
if not st.session_state.cats:
    st.sidebar.caption("No cats yet — add one from Home.")


# ------------------ HOME ------------------
if st.session_state.page == "Home":
    st.markdown('<div class="surface">', unsafe_allow_html=True)

    st.markdown(
        """
        <h1>🐈 Multi-Cat Care Planner</h1>
        <p class="small">
            Track feeding, medicine, behaviour — especially helpful for multi-cat/feral care.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="card">🍽 Feeding</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">💊 Meds & Vet</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card">🧼 Litter & Supplies</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="card">🐾 Feral care</div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1, 2])

    with left:
        if st.button("Get started", type="primary", use_container_width=True):
            st.session_state.page = "AddCat"
            st.rerun()

    with right:
        st.info("Click **Get started** to add your first cat.")

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------ ADD CAT (NOT in sidebar) ------------------
if st.session_state.page == "AddCat":
    st.header("Add a cat")
    st.caption("After saving, the cat will appear in the sidebar.")

    with st.form("add_cat_form", clear_on_submit=True):
        name = st.text_input("Cat name", placeholder="e.g., Mango")
        status = st.selectbox("Type", ["Owned", "Feral", "Foster"], index=1)
        age = st.text_input("Age", placeholder="e.g., 3")
        notes = st.text_area("Notes", placeholder="Diet, allergies, temperament, etc.")
        submitted = st.form_submit_button("Save cat")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    if submitted:
        name_clean = name.strip()

        if not name_clean:
            st.error("Please enter a cat name.")
        elif name_clean in [c["name"] for c in st.session_state.cats]:
            st.error("That cat name already exists. Use a unique name.")
        else:
            st.session_state.cats.append(
                {"name": name_clean, "type": status, "age": age.strip(), "notes": notes.strip()}
            )
            st.session_state.page = name_clean  # jump to cat page
            st.rerun()


# ------------------ FAQ's ------------------
if st.session_state.page == "FAQ's":
    st.title("FAQ's")
    st.caption("General Questions.")

    with st.expander("Should my cat be attacking me especially at night?"):
        st.write(
            "Simple response - NO. Your cats behaviour is a tell sign of underlying issues especially if the cat has a "
            "feral background. Attacking, especially at night could be a symptom of single cat syndrome which describes "
            "behavioral issues in solo-raised kittens, like rough play biting, excessive vocalizing, clinginess, or "
            "destruction, because they miss learning bite inhibition from littermates. Solutions include enrichment "
            "activities, lots of play or simply adopting another cat."
        )

    with st.expander("Why is my cat eating plastic and other inedible things?"):
        st.write(
            "Cats eat inedible things due to pica, which is chewing or eating non-food items like fabric, plastic, or soil, "
            "that can lead to serious health issues like intestinal blockages. Causes range from stress and boredom to "
            "medical conditions such as hyperthyroidism, anemia, or nutritional deficiencies. Solutions include changing "
            "your cat’s diet and seeing a vet to understand the cause.\n\n"
            "WARNING: monitor closely — intestinal blockages can be deadly. Common dangerous items: wet wipes, tissue, "
            "cotton, hair bands."
        )

    with st.expander("Why is my cat constantly hiding?"):
        st.write(
            "If your cat was feral at one point, hiding can be normal. Over time, this may improve. Avoid forcing "
            "interaction; some cats are naturally more timid. Also, kittens can inherit wary behaviour from feral mothers."
        )

    with st.expander("When to see a vet?"):
        st.write(
            "If you've recently caught a feral cat, keep it separated from other pets. Feral cats can carry worms, fleas, "
            "and diseases. See a vet as soon as possible.\n\n"
            "Note: if you treat one cat for fleas/worms, ask your vet about treating all cats in the household."
        )

    with st.expander("Why does my cat have spots on its chin/around its mouth?"):
        st.write(
            "This is often feline acne. Keep food and water bowls clean, consider stainless steel bowls, and keep the area dry."
        )

    with st.expander("Why is my cat's belly so round?"):
        st.write(
            "If it’s very firm or your cat seems unwell, see a vet. A round belly can be parasites, diet issues, or other causes."
        )

    with st.expander("What are the litter box basics?"):
        st.write(
            "A common guideline is one litter box per cat (plus one extra if possible). Scoop daily and change litter regularly."
        )

    with st.expander("What should I do if my cat doesn't like my new kitten?"):
        st.write(
            "Slow introductions are best: separate spaces, scent swapping, supervised short meetings. Don’t force contact."
        )

    with st.expander("How to discipline my cat?"):
        st.write(
            "Try to change the environment instead (cat-proofing), reward good behaviour, and redirect with play. Avoid punishment."
        )


# ------------------ CAT PAGES ------------------
cat_names = [c["name"] for c in st.session_state.cats]
if st.session_state.page in cat_names:
    cat = next(c for c in st.session_state.cats if c["name"] == st.session_state.page)

    st.title(f"🐱 {cat['name']}")

    tabs = st.tabs(["Profile", "🍽 Feeding", "💊 Meds", "🩺 Vet", "🧼 Litter & Supplies"])

    # Profile
    with tabs[0]:
        st.write(f"**Type:** {cat.get('type', '—')}")
        st.write(f"**Age:** {cat.get('age', '—') or '—'}")
        st.write(f"**Notes:** {cat.get('notes', '—') or '—'}")

    # Feeding
    with tabs[1]:
        cat.setdefault("feeding", {"food": "", "schedule": "", "notes": ""})
        cat["feeding"]["food"] = st.text_input("Food type", cat["feeding"]["food"], key=f"{cat['name']}_food")
        cat["feeding"]["schedule"] = st.text_input("Schedule", cat["feeding"]["schedule"], key=f"{cat['name']}_schedule")
        cat["feeding"]["notes"] = st.text_area("Notes", cat["feeding"]["notes"], key=f"{cat['name']}_feed_notes")

    # Meds
    with tabs[2]:
        cat.setdefault("meds", [])
        med = st.text_input("Medication name", key=f"{cat['name']}_med")
        dose = st.text_input("Dosage", key=f"{cat['name']}_dose")
        freq = st.text_input("Frequency", key=f"{cat['name']}_freq")

        if st.button("Add medication", key=f"{cat['name']}_add_med"):
            if med.strip():
                cat["meds"].append({"name": med.strip(), "dosage": dose.strip(), "frequency": freq.strip()})

        if cat["meds"]:
            st.table(cat["meds"])

    # Vet
    with tabs[3]:
        cat.setdefault("vet", [])
        visit_date = st.date_input("Visit date", key=f"{cat['name']}_vet_date")
        reason = st.text_input("Reason", key=f"{cat['name']}_vet_reason")

        if st.button("Add vet visit", key=f"{cat['name']}_add_vet"):
            cat["vet"].append({"date": str(visit_date), "reason": reason.strip()})

        if cat["vet"]:
            st.table(cat["vet"])

    # Litter
    with tabs[4]:
        cat.setdefault("litter", {"type": "", "last_cleaned": "", "notes": ""})
        cat["litter"]["type"] = st.text_input("Litter type", cat["litter"]["type"], key=f"{cat['name']}_litter")
        cat["litter"]["last_cleaned"] = st.text_input(
            "Last cleaned", cat["litter"]["last_cleaned"], key=f"{cat['name']}_cleaned"
        )
        cat["litter"]["notes"] = st.text_area("Notes", cat["litter"]["notes"], key=f"{cat['name']}_litter_notes")

    st.divider()

    if st.button("Delete this cat"):
        st.session_state.cats = [c for c in st.session_state.cats if c["name"] != cat["name"]]
        st.session_state.page = "Home"
        st.rerun()


# ------------------ FERAL CARE (GLOBAL) ------------------
if st.session_state.page == "Feral care":
    st.title("🐾 Feral Cat Care")

    st.markdown(
        """
### Feeding feral cats
- Consistent feeding times
- Remove food after 30–45 minutes
- Avoid free-feeding

### Shelter
- Insulated boxes
- Dry bedding (straw, not blankets)

### Medical & TNR
- Trap–Neuter–Return basics
- Post-surgery monitoring
- When to intervene

### Behavior & Safety
- Avoid direct handling
- Watch body language
- Gradual trust building
"""
    )

    st.info("This section is educational and applies to all feral cats.")
