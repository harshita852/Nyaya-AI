
import streamlit as st
import json

from ai_engine import analyze_complaint
from document import generate_document


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Nyaya AI",
    page_icon="⚖️",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "problem_input" not in st.session_state:
    st.session_state["problem_input"] = ""

if "result" not in st.session_state:
    st.session_state["result"] = None


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("⚖️ Nyaya AI")

    st.caption("Your everyday legal assistant")

    st.divider()

    st.subheader("Settings")

    language = st.selectbox(
        "Response language",
        ["English", "Hindi", "Hinglish"]
    )

    st.divider()

    st.subheader("About")

    st.write(
        """
        Nyaya AI helps ordinary Indians understand
        consumer-related legal problems, explore
        possible remedies and prepare complaints.
        """
    )

    st.divider()

    st.caption(
        "This application provides general legal "
        "information and is not a substitute for "
        "professional legal advice."
    )


# ==================================================
# HEADER
# ==================================================

st.title("⚖️ Nyaya AI")

st.markdown(
    "### Understand your rights. Know your options. Take action."
)

st.write(
    """
    Describe your consumer problem in your own words.

    Our AI assistant will analyze your situation,
    explain possible legal options and help you
    prepare a formal complaint.
    """
)

st.divider()


# ==================================================
# SAMPLE COMPLAINT
# ==================================================

sample = (
    "I purchased a smartphone worth Rs. 25000 "
    "from an online shopping website on 10 October. "
    "The phone arrived with a defective display. "
    "I contacted customer support multiple times "
    "but they have refused to replace it or issue "
    "a refund. I have the invoice and screenshots "
    "of my conversations with customer support."
)


# ==================================================
# COMPLAINT INPUT
# ==================================================

st.subheader("1. Describe Your Problem")

col1, col2 = st.columns([1, 5])

with col1:

    if st.button("Load Sample Complaint"):

        st.session_state["problem_input"] = sample

        st.rerun()


problem = st.text_area(
    "Tell us what happened",
    height=200,
    key="problem_input",
    placeholder=(
        "Describe your consumer problem here. "
        "Include relevant dates, amounts, companies "
        "and any communication you have had."
    )
)


# ==================================================
# ANALYZE COMPLAINT
# ==================================================

if st.button(
    "Analyze My Case",
    type="primary",
    use_container_width=True
):

    if not problem.strip():

        st.warning(
            "Please describe your problem first."
        )

    else:

        with st.spinner(
            "Analyzing your complaint using AI..."
        ):

            try:

                result = analyze_complaint(
                    problem,
                    language
                )

                if not isinstance(result, dict):
                    raise ValueError(
                        "Invalid AI response format."
                    )

                required_fields = [
                    "case_type",
                    "summary",
                    "facts",
                    "timeline",
                    "missing_information",
                    "legal_position",
                    "possible_actions",
                    "evidence_required",
                    "sources",
                    "complaint_draft",
                    "disclaimer"
                ]

                for field in required_fields:

                    if field not in result:
                        result[field] = (
                            [] if field in [
                                "facts",
                                "timeline",
                                "missing_information",
                                "possible_actions",
                                "evidence_required",
                                "sources"
                            ] else ""
                        )

                # Reset previous complaint editor
                st.session_state.pop(
                    "complaint_editor",
                    None
                )

                st.session_state["result"] = result

                st.success(
                    "Your complaint has been analyzed successfully!"
                )

            except Exception as error:

                error_message = str(error).upper()

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):

                    st.error(
                        "Gemini is temporarily experiencing "
                        "high demand. Please try again shortly."
                    )

                elif (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):

                    st.error(
                        "API request limit reached. "
                        "Please try again later."
                    )

                else:

                    st.error(
                        f"Unable to analyze your complaint: {error}"
                    )


# ==================================================
# DISPLAY ANALYSIS
# ==================================================

result = st.session_state.get("result")


if result:

    st.divider()

    st.header("2. Your Case Analysis")

    # --------------------------------------------------
    # CASE OVERVIEW
    # --------------------------------------------------

    st.subheader("Case Overview")

    st.write(
        result.get(
            "summary",
            "No summary available."
        )
    )

    st.caption(
        f"Category: {result.get('case_type', 'Unknown')}"
    )

    st.divider()

    # --------------------------------------------------
    # TABS
    # --------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "Legal Analysis",
            "Evidence & Timeline",
            "Complaint Letter"
        ]
    )

    # ==================================================
    # TAB 1: LEGAL ANALYSIS
    # ==================================================

    with tab1:

        st.subheader("Legal Position")

        st.write(
            result.get(
                "legal_position",
                "No legal analysis available."
            )
        )

        st.divider()

        st.subheader("Possible Actions")

        actions = result.get(
            "possible_actions",
            []
        )

        if actions:

            for action in actions:

                st.markdown(f"- {action}")

        else:

            st.info("No actions suggested.")

        st.divider()

        st.subheader("Missing Information")

        missing = result.get(
            "missing_information",
            []
        )

        if missing:

            for item in missing:

                st.warning(item)

        else:

            st.success(
                "No major missing information identified."
            )

        st.divider()

        st.subheader("Legal Sources")

        sources = result.get(
            "sources",
            []
        )

        if sources:

            for source in sources:

                title = source.get(
                    "title",
                    "Legal Reference"
                )

                url = source.get("url", "")

                relevance = source.get(
                    "relevance",
                    ""
                )

                if url.startswith("https://"):

                    st.markdown(
                        f"**[{title}]({url})**"
                    )

                else:

                    st.markdown(f"**{title}**")

                st.caption(relevance)

        else:

            st.info(
                "No specific legal sources were provided."
            )

    # ==================================================
    # TAB 2: EVIDENCE AND TIMELINE
    # ==================================================

    with tab2:

        st.subheader("Extracted Facts")

        facts = result.get("facts", [])

        if facts:

            for fact in facts:

                st.markdown(f"- {fact}")

        else:

            st.info("No facts extracted.")

        st.divider()

        st.subheader("Event Timeline")

        timeline = result.get("timeline", [])

        if timeline:

            for event in timeline:

                st.markdown(f"- {event}")

        else:

            st.info("No timeline available.")

        st.divider()

        st.subheader("Evidence Required")

        evidence = result.get(
            "evidence_required",
            []
        )

        if evidence:

            for item in evidence:

                st.markdown(f"- {item}")

        else:

            st.info(
                "No evidence requirements identified."
            )

    # ==================================================
    # TAB 3: COMPLAINT GENERATOR
    # ==================================================

    with tab3:

        st.subheader("Generated Complaint")

        complaint = result.get(
            "complaint_draft",
            ""
        )

        if complaint:

            final_complaint = st.text_area(
                "Review and edit your complaint",
                value=complaint,
                height=350,
                key="complaint_editor"
            )

            try:

                doc = generate_document(
                    final_complaint
                )

                st.download_button(
                    label="Download Complaint (.docx)",
                    data=doc,
                    file_name="nyaya_consumer_complaint.docx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    use_container_width=True
                )

            except Exception as error:

                st.error(
                    f"Document generation failed: {error}"
                )

        else:

            st.warning(
                "No complaint draft was generated."
            )

    # ==================================================
    # RAW AI OUTPUT
    # ==================================================

    st.divider()

    with st.expander("View and Download Raw AI Output"):

        st.json(result)

        st.download_button(
            label="Download Analysis JSON",
            data=json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            ),
            file_name="case_analysis.json",
            mime="application/json"
        )

    # ==================================================
    # DISCLAIMER
    # ==================================================

    st.divider()

    st.warning(
        result.get(
            "disclaimer",
            "Nyaya AI provides general legal information, "
            "not professional legal advice. Verify all "
            "information before taking legal action."
        )
    )
