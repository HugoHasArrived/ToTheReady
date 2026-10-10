import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ==================== FRONTEND WEB CODE ====================
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flowers For You?</title>
  <style>
    /* ==================== MONOCHROME GLOBAL STYLES ==================== */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background-color: #fafafa;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    /* ==================== BLACK & WHITE TAB CARD ==================== */
    .card-container {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .card {
      background: #ffffff;
      padding: 50px 60px;
      border: 1px solid #e5e5e5;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
      text-align: center;
      max-width: 440px;
      width: 90%;
    }

    .heart-icon {
      font-size: 32px;
      margin-bottom: 24px;
      color: #111111;
      display: inline-block;
      animation: heartbeat 2s infinite ease-in-out;
    }

    h1 {
      color: #111111;
      font-size: 1.75rem;
      font-weight: 600;
      letter-spacing: -0.025em;
      margin-bottom: 32px;
    }

    /* Tab-style clean aligned button group */
    .btn-group {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      min-height: 80px; /* Pre-allocates space so the interface doesn't jump */
    }

    .btn {
      font-size: 0.95rem;
      font-weight: 500;
      border: 1px solid #111111;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Black Tab Style */
    .yes-btn {
      background-color: #111111;
      color: #ffffff;
      padding: 12px 32px;
    }

    .yes-btn:hover {
      background-color: #222222;
      transform: translateY(-1px);
    }

    /* White Tab Style */
    .no-btn {
      background-color: #ffffff;
      color: #111111;
      padding: 12px 32px;
      position: relative; /* Stays locked in place inside the group */
    }

    .no-btn:hover {
      background-color: #f5f5f5;
    }

    .fade-out {
      opacity: 0;
      pointer-events: none;
    }

    /* ==================== CONTAINER TRANSITIONS ==================== */
    .hidden {
      display: none;
      opacity: 0;
      flex-direction: column;
      align-items: center;
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .show-screen {
      display: flex !important;
      opacity: 1;
    }

    .garden-message, .sad-message {
      text-align: center;
      padding: 20px;
    }

    .garden-message h1 {
      color: #111111;
    }

    .sad-message h1 {
      color: #666666;
    }

    .subtitle {
      color: #666666;
      font-size: 1.1rem;
      margin-top: 12px;
      font-weight: 400;
    }

    /* ==================== MONOCHROME FLOWER ANIMATION ==================== */
    .flower {
      position: relative;
      width: 100px;
      height: 220px;
      margin-top: 40px;
      animation: sway 4s ease-in-out infinite alternate;
    }

    .petal {
      position: absolute;
      background: #111111;
      border-radius: 50%;
      width: 44px;
      height: 44px;
    }

    .petal-1 { top: 0; left: 28px; }
    .petal-2 { top: 28px; left: 56px; }
    .petal-3 { top: 56px; left: 28px; }
    .petal-4 { top: 28px; left: 0; }

    .center {
      position: absolute;
      top: 28px;
      left: 28px;
      background: #ffffff;
      border: 1px solid #111111;
      width: 44px;
      height: 44px;
      border-radius: 50%;
    }

    .stem {
      position: absolute;
      top: 100px;
      left: 49px;
      width: 2px;
      height: 120px;
      background: #111111;
    }

    .leaf {
      position: absolute;
      top: 140px;
      left: 50px;
      width: 30px;
      height: 15px;
      background: #ffffff;
      border: 1px solid #111111;
      border-radius: 0 15px 0 15px;
    }

    /* ==================== ANIMATIONS ==================== */
    @keyframes heartbeat {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.1); }
    }

    @keyframes sway {
      0% { transform: rotate(-3deg); transform-origin: bottom center; }
      100% { transform: rotate(3deg); transform-origin: bottom center; }
    }
  </style>
</head>
<body>

  <!-- Screen 1: The Initial Request Interface -->
  <div id="background" class="card-container">
    <div class="card">
      <div class="heart-icon">🖤</div>
      <h1>Flowers For You?</h1>
      <div class="btn-group">
        <button id="yesBtn" class="btn yes-btn">Yes</button>
        <button id="noBtn" class="btn no-btn">No</button>
      </div>
    </div>
  </div>

  <!-- Screen 2: Garden View (If Yes is chosen) -->
  <div id="flowerContainer" class="hidden">
    <div class="garden-message">
      <h1>I coded you a whole garden! 💐</h1>
      <p class="subtitle">Because you deserve all the flowers in the world.</p>
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

  <!-- Screen 3: Sad View (If No shrinks all the way down) -->
  <div id="sadContainer" class="hidden">
    <div class="sad-message">
      <h1>Im sorry... 💔</h1>
      <p class="subtitle">ill leave you alone now but i will still listen...</p>
    </div>
  </div>

  <!-- ==================== FRONTEND CONTROLLER LOGIC ==================== -->
  <script>
    const noBtn = document.getElementById("noBtn");
    const yesBtn = document.getElementById("yesBtn");
    const background = document.getElementById("background");
    const flowerContainer = document.getElementById("flowerContainer");
    const sadContainer = document.getElementById("sadContainer");

    let clickCount = 0;
    const clicksToReject = 6; // Total clicks on No before final rejection trigger

    if (noBtn && yesBtn && background) {
      noBtn.addEventListener("click", (event) => {
        event.preventDefault();
        clickCount++;

        if (clickCount >= clicksToReject) {
          // Final rejection screen transition
          background.classList.add("fade-out");
          setTimeout(() => {
            background.style.display = "none";
            sadContainer.classList.add("show-screen");
          }, 600);
        } else {
          // Progressively calculate shrinking size values
          const scaleFactor = 1 - (clickCount * 0.15); // Progressively shrinks step-by-step
          const originalPaddingX = 32;
          const originalPaddingY = 12;
          const originalFontSize = 0.95;

          // Apply shrinking text size and box properties to the No button
          noBtn.style.transform = `scale(${scaleFactor})`;
          noBtn.style.fontSize = `${originalFontSize * scaleFactor}rem`;
          noBtn.style.padding = `${originalPaddingY * scaleFactor}px ${originalPaddingX * scaleFactor}px`;
          
          // Simultaneously scale up the Yes button options right alongside it
          const yesScaleFactor = 1 + (clickCount * 0.25);
          yesBtn.style.transform = `scale(${yesScaleFactor})`;
        }
      });
    }

    if (yesBtn && background && flowerContainer) {
      yesBtn.addEventListener("click", () => {
        background.classList.add("fade-out");
        setTimeout(() => {
          background.style.display = "none";
          flowerContainer.classList.add("show-garden", "show-screen");
        }, 600); 
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
