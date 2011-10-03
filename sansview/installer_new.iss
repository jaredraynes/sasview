
; Script generated by the Inno Setup Script Wizard

; and local_config.py located in this directory.
 ; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
[Setup]

ChangesAssociations=yes
AppName=SansView
AppVerName=SansView-1.9.2dev_oct
AppPublisher=(c) 2009, University of Tennessee
AppPublisherURL=http://danse.chem.utk.edu
AppSupportURL=http://danse.chem.utk.edu
AppUpdatesURL=http://danse.chem.utk.edu 
ChangesEnvironment=true 
DefaultDirName={pf}\SansView-Dev
DefaultGroupName=DANSE\SansView-1.9.2dev_oct
DisableProgramGroupPage=yes
LicenseFile=license.txt
OutputBaseFilename=setupSansView
SetupIconFile=images\ball.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=none


[Registry]
Root: HKCR;	Subkey: ".xml\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".txt\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".asc\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".dat\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".tif\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".abs\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".d1d\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR;	Subkey: ".sans\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCR; Subkey: "applications\SansView.exe\shell\open\command";	ValueType: string; ValueName: "";	ValueData: """{app}\SansView.exe""  ""%1"""; 	 Flags: uninsdeletevalue noerror
Root: HKCU;	Subkey: "Software\Classes\.xml\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.txt\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.asc\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.dat\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.tif\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.abs\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.d1d\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU;	Subkey: "Software\Classes\.sans\OpenWithList\SansView.exe";	 Flags: uninsdeletekey noerror
Root: HKCU; Subkey: "Software\Classes\applications\SansView.exe\shell\open\command";	ValueType: string; ValueName: "";	ValueData: """{app}\SansView.exe""  ""%1"""; 	 Flags: uninsdeletevalue noerror
Root: HKCR;	Subkey: ".svs";	ValueType: string;	ValueName: "";	ValueData: "{app}\SansView.exe";	 Flags: uninsdeletevalue
Root: HKCR;	Subkey: ".fitv";	ValueType: string;	ValueName: "";	ValueData: "{app}\SansView.exe";	 Flags: uninsdeletevalue
Root: HKCR;	Subkey: ".inv";	ValueType: string;	ValueName: "";	ValueData: "{app}\SansView.exe";	 Flags: uninsdeletevalue
Root: HKCR;	Subkey: ".prv";	ValueType: string;	ValueName: "";	ValueData: "{app}\SansView.exe";	 Flags: uninsdeletevalue
Root: HKCR; Subkey: "{app}\SansView.exe";	ValueType: string; ValueName: "";	ValueData: "{app}\SansView File";	 Flags: uninsdeletekey 	
Root: HKCR; Subkey: "{app}\SansView.exe\shell\open\command";	ValueType: string; ValueName: "";	ValueData: """{app}\SansView.exe""  ""%1""";	 Flags: uninsdeletevalue noerror 	
Root: HKCR; Subkey: "{app}\images\ball.ico";	ValueType: string; ValueName: "";	ValueData: "{app}\SansView.exe,0"
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment";	ValueType: expandsz; ValueName: "SANSVIEWPATH";	ValueData: "{app}";	 Flags: uninsdeletevalue
; Write to PATH (below) is disabled; need more tests
;Root: HKCU; Subkey: "Environment";	ValueType: expandsz; ValueName: "PATH";	ValueData: "%SANSVIEWPATH%;{olddata}";	 Check: NeedsAddPath()


[Languages]
Name: "english";	MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon";	Description: "{cm:CreateDesktopIcon}";	GroupDescription: "{cm:AdditionalIcons}";	Flags: unchecked


[Files]
Source: "dist\SansView.exe";	DestDir: "{app}";	Flags: ignoreversion
Source: "dist\*";	DestDir: "{app}";	Flags: ignoreversion recursesubdirs createallsubdirs
Source: "images\*";	DestDir: "{app}\images";	Flags: ignoreversion recursesubdirs createallsubdirs
Source: "test\*";	DestDir: "{app}\test";	Flags: ignoreversion recursesubdirs createallsubdirs
Source: "media\*";	DestDir: "{app}\media";	Flags: ignoreversion recursesubdirs createallsubdirs
;	NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\SansView";	Filename: "{app}\SansView.exe";	WorkingDir: "{app}" 
Name: "{group}\{cm:UninstallProgram, SansView}";	 Filename: "{uninstallexe}" 
Name: "{commondesktop}\SansView-1.9.2dev_oct";	Filename: "{app}\SansView.exe";	Tasks: desktopicon; WorkingDir: "{app}" 


[Run]
Filename: "{app}\SansView.exe";	Description: "{cm:LaunchProgram, SansView}";	Flags: nowait postinstall skipifsilent


[Code]
function NeedsAddPath(): boolean;
var
  oldpath: string;
  newpath: string;
  pathArr:    TArrayOfString;
  i:        Integer;
begin
  RegQueryStringValue(HKEY_CURRENT_USER,'Environment','PATH', oldpath)
  oldpath := oldpath + ';';
  newpath := '%SANSVIEWPATH%';
  i := 0;
  while (Pos(';', oldpath) > 0) do begin
    SetArrayLength(pathArr, i+1);
    pathArr[i] := Copy(oldpath, 0, Pos(';', oldpath)-1);
    oldpath := Copy(oldpath, Pos(';', oldpath)+1, Length(oldpath));
    i := i + 1;
    // Check if current directory matches app dir
    if newpath = pathArr[i-1] 
    then begin
      Result := False;
      exit;
    end;
  end;
  Result := True;
end;

