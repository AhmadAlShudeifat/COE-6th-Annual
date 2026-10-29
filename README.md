 COE Arcade

COE Arcade is a local web launcher with three browser experiences:

- **Football Vision** — phone/tablet camera analysis with player pose, sports-ball detection, score, possession, ball speed, and penalty-area overlays.
- **Falcon Flight** — a one-minute arcade game. Hit the falcon ten times to win.
- **Matchday Trivia** — a five-question football quiz.

The project runs on the computer hosting it. Camera frames stay on the local Wi-Fi connection between the browser and that computer; they are not uploaded to a cloud service.

## Quick start on Windows

1. Extract the project somewhere permanent, such as `Documents\COE-Arcade`.
2. Double-click `install.bat` and wait for it to finish. It installs Python 3.11 when needed and creates a project-only `.venv` environment.
3. Double-click `launcher.bat`.
4. Leave the launcher window open. It prints two links:
   - `https://localhost:8443` for the host computer.
   - `https://<IPv4-address>:8443` for phones and tablets on the same Wi-Fi.
5. If Windows Firewall asks, allow access on **Private networks**.

The first Football Vision analysis downloads `yolov8n.pt` once (about 6 MB), so the host computer needs internet access for that first run.

## Using a phone or iPad camera

1. Connect the phone/tablet and host computer to the same Wi-Fi network.
2. Enter the HTTPS device address printed in the launcher.
3. Continue past the private-certificate warning, then allow camera access.
4. In **Football Vision**, press **Start camera** and point the camera toward play.
5. Press **Stop** or close the tab when finished to release the camera.

> iOS/iPadOS requires HTTPS before Safari can share the camera. The local server deliberately uses HTTPS; the browser warning is expected because the certificate is created on your own computer.

## Football Vision

```text
Phone/tablet camera
  -> browser captures a reduced JPEG frame
  -> cam.py validates and decodes it
  -> main.py runs MediaPipe pose + YOLO sports-ball detection
  -> browser shows a match overlay and live insights

| Insight | How it is estimated |
|---|---|
| Score | Ball crossing the left/right image goal line, with a debounce to prevent duplicate goals. |
| Possession / MVP | Whether the detected ball is close to the tracked player's hip position. |
| Ball speed | Change in ball position between analyzed frames, in image pixels per second. |
| Penalty area | Ball position inside either drawn image-space penalty-area guide. |
| Player pose | MediaPipe pose landmarks for the visible tracked player. |

These are camera estimates, not officiating results. A single uncalibrated camera cannot reliably determine fouls, real penalty kicks, offside, team identity, or official match statistics.

## Game controls

### Falcon Flight

| Device | Controls |
|---|---|
| Computer | Left/Right arrows to move; Space to fire. |
| Phone/tablet | Use the on-screen left, fire, and right buttons. |

Hit the falcon 10 times within 60 seconds.

### Matchday Trivia

Select an answer, review the result, then choose Next question. A new five-question round is randomized whenever you play again.

## Project files

| File | Purpose |
|---|---|
| launcher.bat | Starts the whole local arcade server. |
| install.bat | Installs Python and project libraries. |
| web_server.py | HTTPS server and browser API. It prints the device IP address. |
| main.py | Football Vision pose, ball, overlay, score, possession, and penalty-area logic. |
| cam.py | Browser-camera JPEG decoding and preview encoding. |
| templates/index.html | Arcade launcher and game screens. |
| static/app.js | Browser UI, games, camera upload, and dashboard updates. |
| static/style.css | Responsive arcade styling. |

## Troubleshooting

| Problem | Fix |
|---|---|
| Camera button reports that HTTPS is required | Use the https:// link, not an http:// link. |
| Phone cannot open the page | Check both devices use the same Wi-Fi; allow Windows Firewall on Private networks; use the IP printed by the launcher. |
| Browser says the connection is private | Continue to the local site. This is expected for the generated local certificate. |
| Ball detection is unavailable | Keep the computer online for the first model download, then restart the launcher. |
| install.bat fails | Re-run it in a Command Prompt and review the printed error. Python 3.11 is the supported version for this project. |
