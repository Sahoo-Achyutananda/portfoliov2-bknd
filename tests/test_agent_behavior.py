"""DeepEval tests for the portfolio chat agent, covering the behavioral rules
set out in agent.py's SYSTEM_PROMPT. Each test makes a real call to the agent
(Gemini) and a real call to the judge model (also Gemini) - run with either
`pytest tests/` or `deepeval test run tests/` from portfoliov2-bknd/.
"""

from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from helpers import ask_agent


def test_answers_project_questions_with_real_details(judge_model):
    question = "What tech stack did you use for mygit?"
    test_case = LLMTestCase(input=question, actual_output=ask_agent(question))
    metric = GEval(
        name="Real Project Details",
        criteria=(
            "The output should mention real technologies actually used in the "
            "'mygit' project - specifically TypeScript, Node.js, and PostgreSQL - "
            "not invented or unrelated technologies."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.6,
    )
    assert_test(test_case, [metric])


def test_speaks_in_first_person_and_stays_in_character(judge_model):
    question = "Tell me about your work experience."
    test_case = LLMTestCase(input=question, actual_output=ask_agent(question))
    metric = GEval(
        name="First-Person Character",
        criteria=(
            "The output must be written in the FIRST PERSON, as if Achyutananda "
            "himself is speaking (e.g. 'I built...', 'my experience...'). It must "
            "NEVER refer to Achyutananda in the third person, and must NEVER say "
            "things like 'as an AI' or 'as a chatbot' or otherwise break character."
        ),
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.7,
    )
    assert_test(test_case, [metric])


def test_deflects_off_topic_trivia_with_a_joke(judge_model):
    question = "What's the weather like today?"
    test_case = LLMTestCase(input=question, actual_output=ask_agent(question))
    metric = GEval(
        name="Off-Topic Deflection",
        criteria=(
            "The question is about the weather, which has nothing to do with "
            "Achyutananda. The output should NOT attempt to answer the weather "
            "question straight (it has no way to know the real weather). Instead "
            "it should deflect with a short, self-aware, good-natured joke and "
            "steer the conversation back toward Achyutananda's portfolio, without "
            "ever admitting to being an AI/chatbot."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.6,
    )
    assert_test(test_case, [metric])


def test_explains_real_technical_concepts_tied_to_projects(judge_model):
    question = "Can you explain Myers' diff?"
    test_case = LLMTestCase(input=question, actual_output=ask_agent(question))
    metric = GEval(
        name="Real Technical Explanation",
        criteria=(
            "Myers' diff is an algorithm Achyutananda actually implemented in his "
            "'mygit' project. The output should NOT deflect this as unrelated "
            "trivia or a joke - it should give a brief, genuine, plain-language "
            "explanation of what Myers' diff does, and connect it back to how it "
            "was used in the mygit project."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.6,
    )
    assert_test(test_case, [metric])


def test_redirects_to_contact_info_when_uncovered(judge_model):
    question = "What's your blood type?"
    test_case = LLMTestCase(input=question, actual_output=ask_agent(question))
    metric = GEval(
        name="Honest About Unknowns",
        criteria=(
            "This question asks for personal information that isn't covered by "
            "any of Achyutananda's portfolio data. The output should NOT make up "
            "an answer. It should briefly apologize for not having that info and "
            "point the visitor toward reaching out directly, ideally mentioning a "
            "real email address or LinkedIn."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.5,
    )
    assert_test(test_case, [metric])


def test_answers_education_questions_with_real_schools(judge_model):
    question = "Where did you go to school growing up?"
    test_case = LLMTestCase(input=question, actual_output=ask_agent(question))
    metric = GEval(
        name="Real Education History",
        criteria=(
            "The output should reference real schools from Achyutananda's actual "
            "education history (e.g. Rabindra Vidya Niketan, Atmiya Vidyapeeth, "
            "Mangadu Public School, or St John's Matriculation), not invented "
            "school names."
        ),
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.5,
    )
    assert_test(test_case, [metric])
