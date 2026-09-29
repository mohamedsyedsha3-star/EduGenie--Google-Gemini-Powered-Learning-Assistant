const form = document.getElementById("eduForm");

const taskSelect = document.getElementById("task");

const levelContainer =
    document.getElementById("levelContainer");

const levelSelect =
    document.getElementById("level");

const inputText =
    document.getElementById("inputText");

const characterCount =
    document.getElementById("characterCount");

const submitButton =
    document.getElementById("submitButton");

const buttonText =
    document.getElementById("buttonText");

const spinner =
    document.getElementById("spinner");

const resultSection =
    document.getElementById("resultSection");

const resultTitle =
    document.getElementById("resultTitle");

const resultContent =
    document.getElementById("resultContent");

const copyButton =
    document.getElementById("copyButton");


const endpointMap = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
};


const titleMap = {
    qa: "Answer",
    explain: "Explanation",
    quiz: "Practice Quiz",
    summarize: "Summary",
    learn: "Recommended Learning Path"
};


const buttonMap = {
    qa: "Ask EduGenie",
    explain: "Explain Concept",
    quiz: "Generate Quiz",
    summarize: "Summarize Text",
    learn: "Create Learning Path"
};


taskSelect.addEventListener(
    "change",
    updateTaskUI
);


inputText.addEventListener(
    "input",
    updateCharacterCount
);


form.addEventListener(
    "submit",
    handleSubmit
);


copyButton.addEventListener(
    "click",
    copyResult
);


function updateTaskUI() {

    const task = taskSelect.value;

    buttonText.textContent =
        buttonMap[task];

    if (task === "learn") {

        levelContainer.classList.remove(
            "hidden"
        );

        inputText.placeholder =
            "Example: SQL";

    } else {

        levelContainer.classList.add(
            "hidden"
        );

        if (task === "qa") {

            inputText.placeholder =
                "Example: Which is the largest ocean?";

        } else if (task === "explain") {

            inputText.placeholder =
                "Example: Explain photosynthesis";

        } else if (task === "quiz") {

            inputText.placeholder =
                "Paste a topic or study passage here...";

        } else if (task === "summarize") {

            inputText.placeholder =
                "Paste the paragraph or educational passage here...";
        }
    }
}


function updateCharacterCount() {

    characterCount.textContent =
        inputText.value.length;
}


async function handleSubmit(event) {

    event.preventDefault();

    const task = taskSelect.value;

    const text = inputText.value.trim();

    if (!text) {

        showError(
            "Please enter some content first."
        );

        return;
    }


    setLoading(true);

    hideResult();


    try {

        const body = task === "learn"
            ? {
                topic: text,
                level: levelSelect.value
            }
            : {
                text: text
            };


        const response = await fetch(
            endpointMap[task],
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(body)
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "The server returned an error."
            );
        }


        showResult(
            task,
            data.result
        );


    } catch (error) {

        showError(
            error.message ||
            "Something went wrong."
        );

    } finally {

        setLoading(false);
    }
}


function showResult(task, result) {

    resultSection.classList.remove(
        "hidden"
    );

    resultTitle.textContent =
        titleMap[task];


    if (task === "quiz") {

        renderQuiz(result);

    } else {

        resultContent.innerHTML = "";

        const textElement =
            document.createElement("div");

        textElement.className =
            "result-text";

        textElement.textContent =
            result;

        resultContent.appendChild(
            textElement
        );
    }


    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function renderQuiz(questions) {

    resultContent.innerHTML = "";

    questions.forEach(
        (question, questionIndex) => {

            const questionDiv =
                document.createElement("div");

            questionDiv.className =
                "quiz-question";


            const heading =
                document.createElement("h3");

            heading.textContent =
                `${questionIndex + 1}. ${question.question}`;


            questionDiv.appendChild(
                heading
            );


            const optionsDiv =
                document.createElement("div");

            optionsDiv.className =
                "quiz-options";


            const feedback =
                document.createElement("div");

            feedback.className =
                "quiz-feedback";


            question.options.forEach(
                option => {

                    const button =
                        document.createElement(
                            "button"
                        );

                    button.type =
                        "button";

                    button.className =
                        "quiz-option";

                    button.textContent =
                        option;


                    button.addEventListener(
                        "click",
                        () => {

                            checkQuizAnswer(
                                button,
                                option,
                                question.answer,
                                optionsDiv,
                                feedback
                            );

                        }
                    );


                    optionsDiv.appendChild(
                        button
                    );
                }
            );


            questionDiv.appendChild(
                optionsDiv
            );

            questionDiv.appendChild(
                feedback
            );


            resultContent.appendChild(
                questionDiv
            );
        }
    );
}


function checkQuizAnswer(
    clickedButton,
    selected,
    correct,
    optionsContainer,
    feedback
) {

    const allButtons =
        optionsContainer.querySelectorAll(
            ".quiz-option"
        );


    allButtons.forEach(
        button => {
            button.disabled = true;

            if (
                button.textContent ===
                correct
            ) {
                button.classList.add(
                    "correct"
                );
            }
        }
    );


    if (selected === correct) {

        clickedButton.classList.add(
            "correct"
        );

        feedback.textContent =
            "✓ Correct!";

        feedback.className =
            "quiz-feedback feedback-correct";

    } else {

        clickedButton.classList.add(
            "incorrect"
        );

        feedback.textContent =
            `✗ Incorrect. Correct answer: ${correct}`;

        feedback.className =
            "quiz-feedback feedback-incorrect";
    }
}


function showError(message) {

    resultSection.classList.remove(
        "hidden"
    );

    resultTitle.textContent =
        "Something went wrong";

    resultContent.innerHTML = "";


    const error =
        document.createElement("div");

    error.className =
        "error";

    error.textContent =
        message;


    resultContent.appendChild(
        error
    );


    resultSection.scrollIntoView({
        behavior: "smooth"
    });
}


function hideResult() {

    resultSection.classList.add(
        "hidden"
    );
}


function setLoading(loading) {

    submitButton.disabled =
        loading;

    spinner.classList.toggle(
        "hidden",
        !loading
    );


    if (loading) {

        buttonText.textContent =
            "EduGenie is thinking...";

    } else {

        const task =
            taskSelect.value;

        buttonText.textContent =
            buttonMap[task];
    }
}


async function copyResult() {

    const text =
        resultContent.innerText;


    if (!text) {
        return;
    }


    try {

        await navigator.clipboard.writeText(
            text
        );

        copyButton.textContent =
            "Copied!";

        setTimeout(
            () => {
                copyButton.textContent =
                    "Copy";
            },
            1500
        );

    } catch (error) {

        copyButton.textContent =
            "Copy failed";

        setTimeout(
            () => {
                copyButton.textContent =
                    "Copy";
            },
            1500
        );
    }
}


updateTaskUI();
updateCharacterCount();
