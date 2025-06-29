# ManByVol
Python script that i have made to combine manga chpater into volumes for my kindle. Possible only thanks to Mangadex.org API.
Advice: Download with chapters HakuNeko. (For kindle users: convert combined volumes with KCC.)
Its a little buggy (a lot). Issue and i'll fix it. 

### Features:
- **Combining cbz manga chapter to volumes** (supports sub chapters: 1.5)
- **Donwloading and adding covers**

### Things you should know:
- Use `-h` for options and descriptions
- All **paths** have to be **with no spaces** (known isue. will fix. im lazy)


##### Requires python to be installed.

*******************
### Basic usage:
<ol>
  <li><strong>Download the latest release</strong>
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/e0170201-9543-45a7-9dc8-17130cc6ae31" width="400" alt="Download latest release">
        </td>
      </tr>
    </table>
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/27d89b3a-61af-462f-b2d4-4f003984f911" width="400" alt="Download python file">
        </td>
      </tr>
    </table>
  </li>

  <li><strong>Prepare your workspace</strong> in some easily accessible directory <strong>(!!Get rid of all spaces in the folder name!!)</strong> 
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/d55fee02-7d77-44ba-8b77-33697ee5d446" width="400" alt="Prepare workspace">
        </td>
      </tr>
    </table>
  </li>

  <li><strong>Find your manga on <a href="https://mangadex.org/" target="_blank" rel="noopener noreferrer">mangadex</a></strong>. Make sure that no chapters are missing.
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/cc57732c-44b1-4839-bc81-3fca0c598704" width="800" alt="MangaDex page">
        </td>
      </tr>
    </table>
  </li>

  <li><strong>Open PowerShell</strong> (Windows search or run with <code>Windows + R</code>, then type <code>powershell</code>) navigate to youre directory (type <code>cd</code> [path to youre dir]
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/0a568396-c352-4784-94a9-19fa499dff98" width="800" alt="MangaDex page">
        </td>
      </tr>
    </table>
  </li>

  <li><strong>Install all dependencies</strong> <code>pip install requests natsort colorama</code> 
  </li>

  <li> Run the script <code>pyhotn3 .\ManByVol.py -id [INSERTmANGAiD] -p [INSERTcHAPTERpREFIX] -f [INSERTtARGERfOLDER] -c </code> (If it doesnt work try using <code>py</code> or <code>py</code>) 
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/58626470-6fcd-4887-bbb6-7408a3482ce0" width="800" alt="MangaDex page">
        </td>
      </tr>
    </table>
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/515c52bb-81df-4d66-a0bd-aa938591a1a7" width="800" alt="MangaDex page">
        </td>
      </tr>
    </table>
    <table>
      <tr>
        <td style="border: 2px solid #999; padding: 4px;">
          <img src="https://github.com/user-attachments/assets/9c03fb55-ce6d-4b9c-b075-0962c9f96ac1" width="800" alt="MangaDex page">
        </td>
      </tr>
    </table>

  <li><strong>Done! (If there was some problem downloading and adding covers, check the help message bellow for <code>-cr</code><code>-ca</code></strong> 
  </li>

*******************

The help message (-h)
```
******************
HELP MESSAGE ===>
This tool automatically combines your manga chapters into volumes using mangadex.org API and if wanted even adds covers.

*** USAGE ***
1. Put all your chapters in one folder.
2. Find the manga on mangadex.org and get its ID from the URL. (https://mangadex.org/title/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/manga)
3. Run the script from command using:
    python3 app.py -id [ID] -f [FOLDER] -p [INPUT FILE PREFIX] <-cp [CREATED FILE PREFIX]> <-c> -<kc> <-l [LIMIT]>
    OR
    py app.py -id [ID] -f [FOLDER] -p [INPUT FILE PREFIX] <-cp [CREATED FILE PREFIX]> <-c> -<kc> <-l [LIMIT]>

*** ARGUMENTS ***
REQUIRED:
-f: Target folder to process.
-p: Prefix in input chapter files naming (to strip and read its number).
-id: UUID of manga dex manga (you can find it in url: https://mangadex.org/title/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/manga title).
OPTIONAL:
-h, -help: Print this message.
-cp: Prefix for created files.
-l: Request limit for API.
-cr: Cover version Explenation: (You can view covers on mangadex.org in 'art' tab of manga. They are sorted by 'volume'. If any 'volume' is there multiple times these are various 'versions'. These 'versions' are sorted from left to right.)
-ca: Cover variation Explenation: (You can view covers on mangadex.org in 'art' tab of manga. They are sorted by 'volume'. Some of them have decimal point '.' and number after it. These are variations.)
-cl: Cover locale (local cover) (on mangadex.org you can filter by locale) For language codes refere to https://api.mangadex.org/docs/3-enumerations/ ===> https://en.wikipedia.org/wiki/IETF_language_tag and https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes

*** SWITCHES ***
-c: Download and add covers.
-kc: Keep downloaded covers.
-pc: Log (print) API's cover response.

******************
```




### Dont hasitate to ask
