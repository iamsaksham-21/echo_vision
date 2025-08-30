// the instant welcome voice at the beginning.
window.addEventListener('DOMContentLoaded', () => {
    const welcomeMessage = "Hey there. I'm EchoVision at your service today.";
    const speech = new SpeechSynthesisUtterance(welcomeMessage);
    speech.rate = 1;
    speech.pitch = 1.2;

    let hasSpoken = false; // ✅ Prevent multiple speeches

    const speakOnce = () => {
      if (hasSpoken) return; // stop if already spoken
      hasSpoken = true;

      const voices = speechSynthesis.getVoices();
      const selectedVoice = voices.find(voice => voice.name === 'Samantha');


      if (selectedVoice) {
        speech.voice = selectedVoice;
      }

      window.speechSynthesis.speak(speech);
    };

    // Handle when voices are ready
    if (speechSynthesis.getVoices().length === 0) {
      speechSynthesis.onvoiceschanged = speakOnce;
    } else {
      speakOnce();
    }
  });


  //Activate voice running
  window.onload = function () {
    // Put your speech recognition code here 👇
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = function (event) {
        const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
        console.log("Heard:", transcript);

        const triggerWords = ["get started", "start now", "walle", "hello"];
        if (triggerWords.includes(transcript)) {
          const button = document.getElementById("getStartedBtn");
          if (button) button.click();
          else console.error("Button not found!");
        }
      };

      recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);
      };

      recognition.start();
    } else {
      alert("Speech Recognition is not supported in your browser. Try Chrome!");
    }
  }

  //FLASK INTEGRATION
  // function startAssistant() {
  //   fetch('http://127.0.0.1:5000/start-assistant')
  //     .then(response => response.text())
  //     .then(data => console.log(data))
  //     .catch(error => console.error('Error:', error));
  // }
  // If you're using a button with id="getStartedBtn", this will trigger startAssistant() when clicked
  document.getElementById("getStartedBtn").addEventListener("click", startAssistant);
  function startAssistant() {
    fetch("http://127.0.0.1:5000/start-assistant", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        console.log("Assistant started:", data);
    })
    .catch(error => console.error("Error:", error));
}



