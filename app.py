from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flowers For You?</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    body {
      background-color: #ffeef2;
      overflow: hidden;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .card-container {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transition: opacity 0.8s ease;
    }
    .card {
      background: white;
      padding: 40px 50px;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(255, 105, 180, 0.2);
      text-align: center;
    }
    .heart-icon {
      font-size: 50px;
      margin-bottom: 20px;
      animation: pulse 1.5s infinite;
    }
    h1 {
      color: #d63384;
      margin-bottom: 30px;
      font-size: 2rem;
    }
    .btn-group {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
    }
    .btn {
      padding: 12px 35px;
      font-size: 1.1rem;
      font-weight: 600;
      border: none;
      border-radius: 50px;
      cursor: pointer;
      transition: transform 0.2s ease, font-size 0.2s ease, padding 0.2s ease, background-color 0.3s ease;
    }
    .yes-btn {
      background-color: #ff477e;
      color: white;
      box-shadow: 0 5px 15px rgba(255, 71, 126, 0.4);
    }
    .yes-btn:hover {
      transform: scale(1.05);
    }
    .no-btn {
      background-color: #e2e8f0;
      color: #64748b;
      position: absolute;
      left: 58%;
      top: 60%;
      transition: left 0.1s ease-out, top 0.1s ease-out, transform 0.2s ease, padding 0.2s ease, font-size 0.2s ease;
    }
    .no-btn.tiny-final {
      position: static !important; 
      background-color: #f1f5f9;
      color: #94a3b8;
      padding: 4px 10px !important;
      font-size: 0.65rem !important;
      font-weight: 400;
      box-shadow: none;
    }
    .fade-out {
      opacity: 0;
      pointer-events: none;
    }
    .hidden {
      display: none;
      opacity: 0;
      flex-direction: column;
      align-items: center;
      transition: opacity 1s ease-in;
    }
    .show-screen {
      display: flex !important;
      opacity: 1;
    }
    .garden-message, .sad-message {
      text-align: center;
      animation: fadeInUp 1s ease;
    }
    .sad-message h1 {
      color: #64748b;
    }
    .flower {
      position: relative;
      width: 100px;
      height: 250px;
      margin-top: 50px;
      animation: sway 3s ease-in-out infinite alternate;
    }
    .petal {
      position: absolute;
      background: #ff70a6;
      border-radius: 50%;
      width: 50px;
      height: 50px;
    }
    .petal-1 { top: 0; left: 25px; }
    .petal-2 { top: 25px; left: 50px; }
    .petal-3 { top: 50px; left: 25px; }
    .petal-4 { top: 25px; left: 0; }
    .center {
      position: absolute;
      top: 25px;
      left: 25px;
      background: #ffd166;
      width: 50px;
      height: 50px;
      border-radius: 50%;
    }
    .stem {
      position: absolute;
      top: 95px;
      left: 47px;
      width: 6px;
      height: 150px;
      background: #06d6a0;
      border-radius: 3px;
    }
    .leaf {
      position: absolute;
      top: 140px;
      left: 53px;
      width: 40px;
      height: 20px;
      background: #06d6a0;
      border-radius: 0 20px 0 20px;
    }
    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.15); }
      100% { transform: scale(1); }
    }
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes sway {
      0% { transform: rotate(-2deg); transform-origin: bottom center; }
      100% { transform: rotate(2deg); transform-origin: bottom center; }
    }
  </style>
</head>
<body>

  <div id="background" class="card-container">
    <div class="card">
      <div class="heart-icon">❤️</div>
      <h1>Flowers For You?</h1>
      <div class="btn-group">
        <button id="yesBtn" class="btn yes-btn">Yes</button>
        <button id="noBtn" class="btn no-btn">No</button>
      </div>
    </div>
  </div>

  <div id="flowerContainer" class="hidden">
    <div class="garden-message">
      <h1>I coded you a whole garden! 💐</h1>
      <p>Because you deserve all the flowers in the world.</p>
    </div>
    <div class="flower">
      <div class="petal petal-1"></div>
      <div class="petal petal-2"></div>
      <div class="petal petal-3"></div>
      <div class="petal petal-4"></div>
      <div class="center"></div>
      <div class="stem"></div>
      <div class="leaf"></div>
    </div>
  </div>

  <div id="sadContainer" class="hidden">
    <div class="sad-message">
      <h1>Im sorry... 💔</h1>
      <p style="color: #64748b; font-size: 1.2rem; margin-top: 15px;">ill leave you alone now but i will still listen...</p>
    </div>
  </div>

  <script>
    const noBtn = document.getElementById("noBtn");
    const yesBtn = document.getElementById("yesBtn");
    const background = document.getElementById("background");
    const flowerContainer = document.getElementById("flowerContainer");
    const sadContainer = document.getElementById("sadContainer");

    let yesScale = 1; 
    let escapeCount = 0;
    const maxEscapes = 5; 

    if (noBtn && background && yesBtn) {
      const moveNoBtn = (event) => {
        if (escapeCount >= maxEscapes) return;
        escapeCount++;

        if (escapeCount >= maxEscapes) {
          noBtn.classList.add("tiny-final");
        } else {
          const left = 12 + Math.random() * 70; 
          const top = 15 + Math.random() * 70;
          noBtn.style.left = left + '%';
          noBtn.style.top = top + '%';
        }

        yesScale += 0.25;
        yesBtn.style.transform = 'scale(' + yesScale + ')';
      };

      noBtn.addEventListener("mouseenter", moveNoBtn);
      noBtn.addEventListener("click", (event) => {
        event.preventDefault();
        if (escapeCount >= maxEscapes) {
          background.classList.add("fade-out");
          setTimeout(() => {
            background.style.display = "none";
            sadContainer.classList.add("show-screen");
          }, 800);
        } else {
          moveNoBtn();
        }
      });
    }

    if (yesBtn && background && flowerContainer) {
      yesBtn.addEventListener("click", () => {
        background.classList.add("fade-out");
        setTimeout(() => {
          background.style.display = "none";
          flowerContainer.classList.add("show-screen");
        }, 800); 
      });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(debug=True)
