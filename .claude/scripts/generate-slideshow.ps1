# Generates tov_slideshow.html for a given lesson
# Usage: .\generate-slideshow.ps1 -LessonPath "ABSOLUTE\PATH\TO\LESSON"
# The LessonPath must contain digital-course-screenshots\ and digital-course-tts-scripts\

param(
    [string]$LessonPath
)

$slidesDir = Join-Path $LessonPath "digital-course-screenshots"
$slides = Get-ChildItem "$slidesDir\slide-*.png" | Sort-Object Name

if ($slides.Count -eq 0) {
    Write-Error "No slides found in $slidesDir"
    exit 1
}

# Build slide <img> tags
$slideImgTags = ""
$i = 1
foreach ($slide in $slides) {
    $path = $slide.FullName -replace '\\', '/'
    $display = if ($i -eq 1) { "block" } else { "none" }
    $slideImgTags += "  <img id='slide-$i' src='file:///$path' class='slide' style='display:$display' draggable='false'>`n"
    $i++
}

$total = $slides.Count

# Write lesson path for the TTS server to preload
[System.IO.File]::WriteAllText("$env:TEMP\tov_current_lesson.txt", $LessonPath, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText("$env:TEMP\tov_current_slide.txt",  "1",          [System.Text.Encoding]::UTF8)

$html = @"
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Tov-learn</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0d0d1a;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    overflow: hidden;
    user-select: none;
  }
  .slide-wrap {
    position: relative;
    width: min(95vw, calc(95vh * 1.6));
  }
  .slide {
    width: 100%;
    display: block;
    border-radius: 10px;
  }

  /* Transparent overlays on the baked-in nav buttons.
     From slide-01.png: nav bar spans ~35%-65% width at ~90%-97% height.
       next (הבא)   is on the VISUAL LEFT  (35%-52%)
       prev (הקודם) is on the VISUAL RIGHT (53%-65%) */
  .overlay {
    position: absolute;
    cursor: pointer;
    border-radius: 20px;
    /* debug: background: rgba(255,0,0,0.35); */
  }
  #btn-next-overlay {
    left: 35%;
    right: 53%;
    top: 90%;
    bottom: 3%;
  }
  #btn-prev-overlay {
    left: 53%;
    right: 35%;
    top: 90%;
    bottom: 3%;
  }

  .extra-controls {
    position: absolute;
    bottom: 3%;
    display: flex;
    gap: 8px;
    direction: ltr;
  }
  .extra-controls.left-side  { left:  1.5%; }
  .extra-controls.right-side { right: 1.5%; }
  .pill-btn {
    background: rgba(30, 30, 60, 0.92);
    color: #d0d0ff;
    border: 1px solid rgba(120, 120, 200, 0.35);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 13px;
    font-family: 'Heebo', 'Segoe UI', Arial, sans-serif;
    cursor: pointer;
    backdrop-filter: blur(4px);
    transition: background 0.15s, color 0.15s;
    white-space: nowrap;
  }
  .pill-btn:hover { background: rgba(60,60,120,0.95); color: #fff; }
  .pill-btn.paused {
    background: rgba(100,30,30,0.92);
    border-color: rgba(200,80,80,0.5);
    color: #ffaaaa;
  }
</style>
</head>
<body>
<div class="slide-wrap" id="wrap">

$slideImgTags
  <div class="overlay" id="btn-next-overlay" onclick="changeSlide(1)"></div>
  <div class="overlay" id="btn-prev-overlay" onclick="changeSlide(-1)"></div>

  <div class="extra-controls left-side">
    <button class="pill-btn" id="pause-btn" onclick="togglePause()">&#x23F8; &#x05D4;&#x05E9;&#x05D4;&#x05D4;</button>
  </div>
  <div class="extra-controls right-side">
    <button class="pill-btn" id="fs-btn" onclick="toggleFullscreen()">&#x26F6; &#x05DE;&#x05E1;&#x05DA; &#x05DE;&#x05DC;&#x05D0;</button>
  </div>
</div>

<script>
  let current = 1;
  const total = $total;
  let paused = false;

  function postSlide(num) {
    return fetch('http://localhost:7823/', { method: 'POST', body: String(num) }).catch(() => {});
  }

  function showSlide(n, triggerTts) {
    if (n < 1 || n > total) return;
    document.getElementById('slide-' + current).style.display = 'none';
    current = n;
    document.getElementById('slide-' + current).style.display = 'block';
    const prevO = document.getElementById('btn-prev-overlay');
    const nextO = document.getElementById('btn-next-overlay');
    prevO.style.opacity       = current === 1     ? '0.3' : '1';
    prevO.style.pointerEvents  = current === 1    ? 'none' : 'auto';
    nextO.style.opacity       = current === total ? '0.3' : '1';
    nextO.style.pointerEvents  = current === total ? 'none' : 'auto';
    if (triggerTts !== false) postSlide(current);
  }

  function changeSlide(dir) {
    if (paused) return;
    showSlide(current + dir);
  }

  function togglePause() {
    paused = !paused;
    const btn = document.getElementById('pause-btn');
    if (paused) {
      fetch('http://localhost:7823/', { method: 'POST', body: 'stop' }).catch(() => {});
      btn.innerHTML = '&#x25B6; &#x05D4;&#x05DE;&#x05E9;&#x05DA;';
      btn.classList.add('paused');
    } else {
      postSlide(current);
      btn.innerHTML = '&#x23F8; &#x05D4;&#x05E9;&#x05D4;&#x05D4;';
      btn.classList.remove('paused');
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      document.getElementById('fs-btn').innerHTML = '&#x2715; &#x05D9;&#x05E6;&#x05D9;&#x05D0;&#x05D4;';
    } else {
      document.exitFullscreen();
      document.getElementById('fs-btn').innerHTML = '&#x26F6; &#x05DE;&#x05E1;&#x05DA; &#x05DE;&#x05DC;&#x05D0;';
    }
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft'  && !paused) changeSlide(1);
    if (e.key === 'ArrowRight' && !paused) changeSlide(-1);
    if (e.key === 'p' || e.key === 'P')    togglePause();
    if (e.key === 'f' || e.key === 'F')    toggleFullscreen();
  });

  // Poll server for Claude-side advances
  setInterval(async () => {
    if (paused) return;
    try {
      const r = await fetch('http://localhost:7823/?t=' + Date.now());
      const n = parseInt(await r.text());
      if (!isNaN(n) && n !== current) showSlide(n, false);
    } catch (e) {}
  }, 500);

  showSlide(1);
</script>
</body>
</html>
"@

$outPath = "$env:TEMP\tov_slideshow.html"
[System.IO.File]::WriteAllText($outPath, $html, (New-Object System.Text.UTF8Encoding($true)))
Write-Host $outPath
