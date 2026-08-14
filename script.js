// script.js

document.getElementById("mbti-test").addEventListener("submit", function(event) {
    event.preventDefault(); // Sayfanın yeniden yüklenmesini engelle

    let result = {
        E: 0,
        I: 0,
        S: 0,
        N: 0,
        T: 0,
        F: 0,
        J: 0,
        P: 0
    };

    // Sorulara verilen cevaplardaki değeri al ve puanları artır
    const questions = [
        "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8",
        "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16",
        "q17", "q18", "q19", "q20", "q21", "q22", "q23", "q24",
        "q25", "q26", "q27", "q28", "q29", "q30"
    ];
    
    questions.forEach(function(question) {
        let answer = document.querySelector(`input[name="${question}"]:checked`);
        if (answer) {
            result[answer.value]++;
        }
    });

    // Sonuçları hesapla
    let mbtiType = '';
    mbtiType += result.E > result.I ? 'E' : 'I';
    mbtiType += result.S > result.N ? 'S' : 'N';
    mbtiType += result.T > result.F ? 'T' : 'F';
    mbtiType += result.J > result.P ? 'J' : 'P';

    // Sonuçları ekranda göster
    document.getElementById("result").textContent = "Senin MBTI Tipin: " + mbtiType;
});
