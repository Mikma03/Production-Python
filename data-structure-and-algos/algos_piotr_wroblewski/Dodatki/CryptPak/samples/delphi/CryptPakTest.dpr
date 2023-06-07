program CryptPakTest;

uses
  Forms,
  CryptPakDemoForm in 'CryptPakDemoForm.pas' {TestForm},
  CryptPak in 'CryptPak.pas',
  BasicTypes in 'BasicTypes.pas',
  CipherDef in 'CipherDef.pas';

{$R *.RES}

begin
  Application.Initialize;
  Application.CreateForm(TTestForm, TestForm);
  Application.Run;
end.
