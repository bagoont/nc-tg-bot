### Files dialog text.

## Scrollgroup window.
file-info =  
    <b>File Info:</b>
    - Name: { $name }
    - Path: /{ $path }
    - Type: { $symbol } { $type ->
        [folder] folder
        *[other] { $type }
    }
    - Favorite: { $favorite ->
        [True] ⭐
        [False] ❌
        *[other] ❔
    }
        
    <b>Properties:</b>
    - Size: { $size }
    - Last modified: { $last_modified }
        
    <b>Owner Information:</b>
    - User: { $user }
    - Permissions: { $permissions }
download-btn = ⬇️ Download
delete-btn = 🗑️ Delete
create-btn = 🆕 Create

## Multiselect window.
multiselect-files = 
    Select multiple files from:
    <i>{ $path }</i>
multidownload-files = <i>Downloading file: { $name }</i>
multidelete-files = <i>Deleting file: { $name }</i>
multidownload-btn = ⬇️ Download selected
multedelete-btn = 🗑️ Delete selected

## Create window.
create-file = 
    Select which file you want to create in:
    <i>{ $path }</i>
folder-btn = 📁 Folder
upload-btn = ⬆️ Upload

## Create folder window.
create-folder = 
    Input folder name to create folder:
    <i>{ $path }/<your-folder></i>
incorrect-folder-name=Incorrect folder name.
folder-create-success=Папка <b>{ $name }</b> по пути <i>{ $path }</i> создана успешно.

## Process documents window.
upload-files-managment = 
    Send the files in the document format that you want to upload to the Nextcloud. 
    
    Click on the file to remove it from the download queue. 
    
    When you have sent all the files you want to download, click "Upload".

## Upload Docuemnts window.
upload-files = <i>Uploadindg { $name }</i>