import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Added 'r' right before the string to safely ignore path character escapes like \U
HTML_CODE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>console.exe</title>
  <style>
    /* ==================== TERMINAL GLOBAL STYLES ==================== */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Courier New', Courier, monospace;
    }

    body {
      background-color: #0c0c0c;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #00ff00;
      padding: 20px;
    }

    /* ==================== COMMAND PROMPT WINDOW ==================== */
    .terminal-window {
      background-color: #000000;
      border: 1px solid #333333;
      border-radius: 6px;
      width: 100%;
      max-width: 500px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
      overflow: hidden;
      transition: opacity 0.6s ease;
    }

    /* Terminal Title Bar */
    .terminal-header {
      background-color: #202020;
      padding: 8px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #333333;
      user-select: none;
    }

    .terminal-title {
      color: #cccccc;
      font-size: 0.8rem;
    }

    .terminal-controls {
      display: flex;
      gap: 8px;
    }

    .control-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background-color: #444444;
    }

    /* Terminal Input/Output Space */
    .terminal-body {
      padding: 30px;
      text-align: left;
    }

    .prompt-line {
      margin-bottom: 15px;
      color: #888888;
      font-size: 0.9rem;
    }

    h1 {
      color: #ffffff;
      font-size: 1.4rem;
      font-weight: normal;
      margin-bottom: 30px;
      line-height: 1.4;
    }

    /* ==================== BUTTON ACTIONS GROUP ==================== */
    .btn-group {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      gap: 15px;
      min-height: 100px;
    }

    .btn {
      font-family: 'Courier New', Courier, monospace;
      font-size: 1rem;
      border: 1px solid #00ff00;
      background-color: transparent;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      border-radius: 4px;
      transition: transform 0.2s ease, font-size 0.2s ease, padding 0.2s ease, background-color 0.2s ease;
    }

    /* Terminal Accent Theme Button */
    .yes-btn {
      color: #000000;
      background-color: #00ff00;
      padding: 10px 28px;
      font-weight: bold;
    }

    .yes-btn:hover {
      background-color: #00cc00;
      border-color: #00cc00;
    }

    /* Neutral Terminal Button */
    .no-btn {
      color: #ffffff;
      border-color: #ffffff;
      padding: 10px 28px;
    }

    .no-btn:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }

    .fade-out {
      opacity: 0;
      pointer-events: none;
    }

    /* ==================== SCREEN SWITCHERS ==================== */
    .hidden {
      display: none;
      opacity: 0;
      width: 100%;
    }

    .show-screen {
      display: block !important;
      opacity: 1;
    }

    .subtitle {
      color: #a9a9a9;
      font-size: 1rem;
      line-height: 1.5;
      margin-top: 15px;
    }

    /* ==================== MATRIX / MONO FLOWER ==================== */
    .flower {
      position: relative;
      width: 80px;
      height: 180px;
      margin: 40px auto 10px auto;
      animation: sway 4s ease-in-out infinite alternate;
    }

    .petal {
      position: absolute;
      background: #00ff00;
      border: 1px solid #000000;
      border-radius: 50%;
      width: 36px;
      height: 36px;
    }

    .petal-1 { top: 0; left: 22px; }
    .petal-2 { top: 22px; left: 44px; }
    .petal-3 { top: 44px; left: 22px; }
    .petal-4 { top: 22px; left: 0; }

    .center {
      position: absolute;
      top: 22px;
      left: 22px;
      background: #000000;
      border: 2px solid #00ff00;
      width: 36px;
      height: 36px;
      border-radius: 50%;
    }

    .stem {
      position: absolute;
      top: 80px;
      left: 39px;
      width: 2px;
      height: 100px;
      background: #00ff00;
    }

    .leaf {
      position: absolute;
      top: 110px;
      left: 40px;
      width: 24px;
      height: 12px;
      background: transparent;
      border: 1px solid #00ff00;
      border-radius: 0 12px 0 12px;
    }

    /* ==================== CORE ANIMATIONS ==================== */
    @keyframes sway {
      0% { transform: rotate(-3deg); transform-origin: bottom center; }
      100% { transform: rotate(3deg); transform-origin: bottom center; }
    }
  </style>
</head>
<body>

  <!-- Main Terminal Wrapper Window Container -->
  <div id="terminalWindow" class="terminal-window">
    
    <!-- Window Head Bar Element -->
    <div class="terminal-header">
      <div class="terminal-title">C:\Users\admin\proposals\flowers.exe</div>
      <div class="terminal-controls">
        <div class="control-dot"></div>
        <div class="control-dot"></div>
        <div class="control-dot"></div>
      </div>
    </div>

    <!-- Window Internal Body -->
    <div class="terminal-body">
      
      <!-- SCREEN 1: Core Selection Logic Screen Interface -->
      <div id="proposalContent">
        <div class="prompt-line">Microsoft Windows [Version 10.0.22631]<br/>(c) Microsoft Corporation. All rights reserved.<br/><br/>\$ run heart_analysis.sh</div>
        <h1>> Flowers For You? [Y/N]_</h1>
        <div class="btn-group">
          <button id="yesBtn" class="btn yes-btn">Yes</button>
          <button id="noBtn" class="btn no-btn">No</button>
        </div>
      </div>

      <!-- SCREEN 2: Garden Compilation Complete Frame (If Yes is clicked) -->
      <div id="flowerContainer" class="hidden">
        <div class="prompt-line">\$ compilation status: SUCCESSFUL</div>
        <h1>> I coded you a whole garden! 💐</h1>
        <p class="subtitle">Because you deserve all the flowers in the world.</p>
        
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

      <!-- SCREEN 3: Rejection Failure Frame State (If No Shrinks to Limit) -->
      <div id="sadContainer" class="hidden">
        <div class="prompt-line" style="color: #ff3333;">\$ abort: process terminated by user decision.</div>
        <h1 style="color: #ff3333;">> Im sorry... 💔</h1>
        <p class="subtitle">ill leave you alone now but i will still listen...</p>
      </div>

    </div>
  </div>

  <!-- ==================== FRONTEND TERMINAL ACTIONS LOGIC ==================== -->
  <script>
    const noBtn = document.getElementById("noBtn");
    const yesBtn = document.getElementById("yesBtn");
    const terminalWindow = document.getElementById("terminalWindow");
    const proposalContent = document.getElementById("proposalContent");
    const flowerContainer = document.getElementById("flowerContainer");
    const sadContainer = document.getElementById("sadContainer");

    let clickCount = 0;
    const clicksToReject = 7; 

    if (noBtn && yesBtn && terminalWindow) {
      noBtn.addEventListener("click", (event) => {
        event.preventDefault();
        clickCount++;

        if (clickCount >= clicksToReject) {
          terminalWindow.classList.add("fade-out");
          setTimeout(() => {
            proposalContent.style.display = "none";
            sadContainer.classList.add("show-screen");
            terminalWindow.classList.remove("fade-out");
          }, 600);
        } else {
          const scaleFactor = Math.max(1 - (clickCount * 0.14), 0.05); 
          const originalPaddingX = 28;
          const originalPaddingY = 10;

          noBtn.style.transform = `scale(${scaleFactor})`;
          noBtn.style.fontSize = `${scaleFactor}rem`;
          noBtn.style.padding = `${originalPaddingY * scaleFactor}px ${originalPaddingX * scaleFactor}px`;
          
          const yesScaleFactor = 1 + (clickCount * 0.2);
          yesBtn.style.transform = `scale(${yesScaleFactor})`;
        }
      });
    }

    if (yesBtn && terminalWindow && flowerContainer) {
      yesBtn.addEventListener("click", () => {
        terminalWindow.classList.add("fade-out");
        setTimeout(() => {
          proposalContent.style.display = "none";
          flowerContainer.classList.add("show-screen");
          terminalWindow.classList.remove("fade-out");
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
