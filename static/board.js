const $form = $('#gameform');
const $response = $('#userresponse');
const $submit = $('#submitbtn');

const $timer = $('#timer')
const $score = $('#score');
const $logs = $('#gamelog');

let score = 0;
let timeLeft = 60;

const seenWords = new Set();

const BASE_URL = "http://127.0.0.1:5000/";

async function checkIfCorrect(word){
    const response = await axios({
        url: `${BASE_URL}/response`,
        method: "GET",
        params: {word: word},
    });
    return response;
}

async function handleClick(evnt){
    evnt.preventDefault();
    user_data = $response.val();
    
    const response = await checkIfCorrect(user_data);
    let result = response.data.result;

    if (timeLeft > 0){
        if (result === "ok" && !seenWords.has(user_data)){
            score += user_data.length;
            seenWords.add(user_data);
        } else if (seenWords.has(user_data)) {
            result = "already-found"
        }
    } else {
        result = "time-ran-out";
    };

    $logs.prepend(`<li>${user_data}: ${result}</li>`);
    $score.text(`Score: ${score}`);
};

async function finishGame(){
    const response = await axios({
        url: `${BASE_URL}/finish`,
        method: "POST",
        data: { score: score },
    });
}

timer = setInterval(() => {
    if (timeLeft <= 0){
        clearInterval(timer);
        finishGame();
    }
    $timer.text(`Time Left: ${timeLeft}`);
    timeLeft -= 1;
}, 1000);

$submit.click(handleClick);