[Setup]
AppName=HSE Mine Manager
AppVersion=2.0.0
DefaultDirName={pf}\HSE Mine Manager
DefaultGroupName=HSE Mine Manager
OutputDir=dist
OutputBaseFilename=HSE_Mine_Manager_Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\HSE_Mine_Manager_V2.exe

[Files]
Source: "dist\HSE_Mine_Manager_V2.exe"; DestDir: "{app}"; Flags: ignoreversion
; We also want to include any necessary assets if not bundled inside the exe (pyinstaller --add-data includes them, but we add them just in case)
; Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commondesktop}\HSE Mine Manager"; Filename: "{app}\HSE_Mine_Manager_V2.exe"; Tasks: desktopicon
Name: "{group}\HSE Mine Manager"; Filename: "{app}\HSE_Mine_Manager_V2.exe"
Name: "{group}\Uninstall HSE Mine Manager"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\HSE_Mine_Manager_V2.exe"; Description: "{cm:LaunchProgram,HSE Mine Manager}"; Flags: nowait postinstall skipifsilent
