# Jideeh's `.blend` Files!

<p align="center">
  <img src="/.Media/Thumbnail.png">
</p>

> [!IMPORTANT]
> All other models require Goo Engine 4.1.1 or later.
> Script names must not be changed!

---

<p align="center">
    <a href="https://github.com/Jideeh1/Jideeh-.blend-Files-/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/Jideeh1/Jideeh-.blend-Files-?style=for-the-badge"></a>
    <a href="https://discord.gg/85rP9SpAkF"><img alt="Discord" src="https://img.shields.io/discord/894925535870865498?style=for-the-badge"></a>
    <a href="https://github.com/Jideeh1/Jideeh-.blend-Files-/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Jideeh1/Jideeh-.blend-Files-?style=for-the-badge"></a>
</p>

---

## How to Download

The Entire Repository:

1. Click the green **Code** button.
2. Click **Download ZIP**.
3. Extract the ZIP file.

A single File:

<p align="center">
  <img src="/.Media/Download Tutorial.gif">
</p>

# Setup your own models! 
FOLLOW THESE EXACT INSTRUCTIONS if you want to setup your own models using the new setup file.
1. You NEED to use models from <https://cdn.hoyotoon.com/s/assets>
2. Install BetterFBX (needs to be 5.2) and Expykit or download the addons in this repository.
3. Open the goo blend file `Setup File.blend`.
4. Under the item tab, there should be a panel called "Jideeh Script Runner" with exactly THREE  buttons. Click the **"Better FBX Importer"** and import your model. **THE FBX, MATERIALS, AND TEXTURE HAS TO BE IN THE SAME FOLDER.**
5. After importing the model, click the 2nd button **"Rig, Outline, Shaders."**
Check here to see what it does.
6. **Conditional:** if the model uses the wrong face lightmap/has no face lightmap, use the 2nd panel in the item tab called **"Face Lightmap Switcher"** (If you don't see it, check the scripting tab and run it.) This lets you add or switch lightmaps with one button.
7. **Optional:** Click **"Jideeh's Setup."**

Credits to the lovely people here who have made the ZZZ setup file. https://discord.com/channels/894925535870865498/1439443691142910077, and credits to @jrdan_ & @starriia for teaching me how to setup models. Give their repositories lots of love! [Star's Repository](<https://github.com/starriia/stars-blend-files>) | [Jordan's Repository](<https://mega.nz/folder/27hnRR6Q#JbVN0z1hKitbKq-6R0dOlg>).

## What the button does:
* **Better  FBX Importer:** Uses the betterFBX addon and allows you to import game models accurately while optimizing your model.
* **Rig, Outline, Shaders:** Is the same script that https://discord.com/channels/894925535870865498/1439443691142910077 uses. As the name suggests, this generates the rig, outline, and shaders of the model.
* **Jideeh's Setup:**  This button lets you setup your blend file for animation renders. This does the following:
  *  Hides All bone collections except for a few: Arms FK, Legs IK, Face, and Torso
  * IK-FK for both arms are toggled on
  * Frame rate is set to 24 fps
  * Render Region is enabled
  * Adds a camera with a 1920 x 1080 resolution
  * Camera Passepartout is set to `.850`

## Special Thanks

- [festivities](https://github.com/festivities) | Shaders
- [Melioli](https://github.com/Melioli) | HoyoToon CDN
- [Poke] | ZZZ Setup

> [!NOTE]
> You may want to use [DownGit](https://downgit.evecalm.com/#/home) to download individual files that you need instead of cloning the entire repository
